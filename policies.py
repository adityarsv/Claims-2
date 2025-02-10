from flask import request, jsonify
from models import policies_collection, policyholders_collection

# ------------------------ POLICY CRUD ------------------------

def create_policy():
    data = request.json
    policy_id = data.get("policy_id")
    type = data.get("type")
    amount = data.get("amount")
    policyholder_id = data.get("policyholder_id")

    # Ensure policyholder exists
    policyholder = policyholders_collection.find_one({"policyholder_id": policyholder_id})
    if not policyholder:
        return jsonify({"error": "Policyholder not found"}), 400

    # Validate that policy_id is unique
    existing_policy = policies_collection.find_one({"policy_id": policy_id})
    if existing_policy:
        return jsonify({"error": "Policy with this ID already exists"}), 400

    new_policy = {
        "policy_id": policy_id,
        "type": type,
        "amount": amount,
        "policyholder_id": policyholder_id
    }

    policies_collection.insert_one(new_policy)
    return jsonify({"message": "Policy created successfully"}), 201

def get_policies():
    policies = list(policies_collection.find({}, {"_id": 0}))
    for policy in policies:
        policyholder = policyholders_collection.find_one({"policyholder_id": policy["policyholder_id"]}, {"_id": 0})
        policy["policyholder_name"] = policyholder["name"] if policyholder else "Unknown"
    return jsonify(policies)

def update_policy(policy_id):
    data = request.json
    type = data.get("type")
    amount = data.get("amount")
    policyholder_id = data.get("policyholder_id")

    # Ensure policy exists
    policy = policies_collection.find_one({"policy_id": policy_id})
    if not policy:
        return jsonify({"error": "Policy not found"}), 404

    # Update policy data
    policies_collection.update_one(
        {"policy_id": policy_id},
        {"$set": {"type": type, "amount": amount, "policyholder_id": policyholder_id}}
    )
    return jsonify({"message": "Policy updated successfully"}), 200

def delete_policy(policy_id):
    # Ensure policy exists
    policy = policies_collection.find_one({"policy_id": policy_id})
    if not policy:
        return jsonify({"error": "Policy not found"}), 404

    # Delete policy
    policies_collection.delete_one({"policy_id": policy_id})
    return jsonify({"message": "Policy deleted successfully"}), 200
