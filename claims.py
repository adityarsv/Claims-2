from flask import request, jsonify
from models import claims_collection, policies_collection, policyholders_collection

# ------------------------ CLAIMS CRUD ------------------------

def create_claim():
    data = request.json
    claim_id = data.get("claim_id")
    amount = data.get("amount")
    status = data.get("status")
    policy_id = data.get("policy_id")
    policyholder_id = data.get("policyholder_id")

    # Validate that claim amount is non-negative
    if amount < 0:
        return jsonify({"error": "Claim amount cannot be negative"}), 400

    # Ensure policy exists
    policy = policies_collection.find_one({"policy_id": policy_id})
    if not policy:
        return jsonify({"error": "Policy not found"}), 400

    # Ensure policyholder exists
    policyholder = policyholders_collection.find_one({"policyholder_id": policyholder_id})
    if not policyholder:
        return jsonify({"error": "Policyholder not found"}), 400

    # Validate that claim amount does not exceed policy coverage amount
    if amount > policy["amount"]:
        return jsonify({"error": "Claim amount cannot exceed policy amount"}), 400

    # Validate that claim_id is unique
    existing_claim = claims_collection.find_one({"claim_id": claim_id})
    if existing_claim:
        return jsonify({"error": "Claim with this ID already exists"}), 400

    new_claim = {
        "claim_id": claim_id,
        "amount": amount,
        "status": status,
        "policy_id": policy_id,
        "policyholder_id": policyholder_id
    }

    claims_collection.insert_one(new_claim)
    return jsonify({"message": "Claim created successfully"}), 201

def get_claims():
    claims = list(claims_collection.find({}, {"_id": 0}))
    for claim in claims:
        policy = policies_collection.find_one({"policy_id": claim["policy_id"]}, {"_id": 0})
        policyholder = policyholders_collection.find_one({"policyholder_id": claim["policyholder_id"]}, {"_id": 0})

        claim["policy_type"] = policy["type"] if policy else "Unknown"
        claim["policyholder_name"] = policyholder["name"] if policyholder else "Unknown"

    return jsonify(claims)

def update_claim(claim_id):
    data = request.json
    amount = data.get("amount")
    status = data.get("status")
    policy_id = data.get("policy_id")
    policyholder_id = data.get("policyholder_id")

    # Ensure claim exists
    claim = claims_collection.find_one({"claim_id": claim_id})
    if not claim:
        return jsonify({"error": "Claim not found"}), 404

    # Ensure policy exists for the claim
    policy = policies_collection.find_one({"policy_id": policy_id})
    if not policy:
        return jsonify({"error": "Policy not found"}), 400

    # Validate claim amount does not exceed policy amount
    if amount > policy["amount"]:
        return jsonify({"error": "Claim amount cannot exceed policy amount"}), 400

    # Update claim data
    claims_collection.update_one(
        {"claim_id": claim_id},
        {"$set": {"amount": amount, "status": status, "policy_id": policy_id, "policyholder_id": policyholder_id}}
    )
    return jsonify({"message": "Claim updated successfully"}), 200

def delete_claim(claim_id):
    # Ensure claim exists
    claim = claims_collection.find_one({"claim_id": claim_id})
    if not claim:
        return jsonify({"error": "Claim not found"}), 404

    # Delete claim
    claims_collection.delete_one({"claim_id": claim_id})
    return jsonify({"message": "Claim deleted successfully"}), 200
