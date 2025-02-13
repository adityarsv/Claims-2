from flask import request, jsonify
from flasgger import Swagger
from flasgger import swag_from
from models import claims_collection, policies_collection, policyholders_collection

# ------------------------ CLAIMS CRUD ------------------------

@swag_from({
    'tags': ['Claims'],
    'summary': 'Create a new claim',
    'description': 'This endpoint allows a policyholder to file a new claim.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'claim_id': {'type': 'integer', 'example': 301},
                    'policy_id': {'type': 'integer', 'example': 201},
                    'claim_amount': {'type': 'number', 'example': 5000.75},
                    'status': {'type': 'string', 'example': 'Pending'}
                }
            }
        }
    ],
    'responses': {
        201: {'description': 'Claim created successfully'},
        400: {'description': 'Claim with this ID already exists'}
    }
})

def create_claim():
    data = request.json
    claim_id = data.get("claim_id")
    amount = data.get("amount")
    status = data.get("status")
    policy_id = data.get("policy_id")
    policyholder_id = data.get("policyholder_id")

    # Validate that claim amount is non-negative
    #if amount < 0:
        #return jsonify({"error": "Claim amount cannot be negative"}), 400

    # Validate that claim_id, policy_id, policyholder_id, and amount are numbers
    if not isinstance(claim_id, int):
        return jsonify({"error": "Claim ID must be a number"}), 400

    if not isinstance(policy_id, int):
        return jsonify({"error": "Policy ID must be a number"}), 400

    if not isinstance(policyholder_id, int):
        return jsonify({"error": "Policyholder ID must be a number"}), 400

    if not isinstance(amount, (int, float)):
        return jsonify({"error": "Amount must be a number"}), 400

    # Validate that status contains only alphabets
    if not status.isalpha():
        return jsonify({"error": "Status must contain only alphabets"}), 400
        
    # Ensure policy exists
    policy = policies_collection.find_one({"policy_id": policy_id})
    if not policy:
        return jsonify({"error": "Policy not found"}), 400

    # Ensure policyholder exists
    policyholder = policyholders_collection.find_one({"policyholder_id": policyholder_id})
    if not policyholder:
        return jsonify({"error": "Policyholder not found"}), 400

    # Validate that claim amount does not exceed policy coverage amount
    #if amount > policy["amount"]:
        #return jsonify({"error": "Claim amount cannot exceed policy amount"}), 400

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

@swag_from({
    'tags': ['Claims'],
    'summary': 'Get all claims',
    'description': 'Retrieves a list of all claims.',
    'responses': {
        200: {
            'description': 'A list of claims',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'claim_id': {'type': 'integer'},
                        'policy_id': {'type': 'integer'},
                        'claim_amount': {'type': 'number'},
                        'status': {'type': 'string'}
                    }
                }
            }
        }
    }
})

def get_claims():
    claims = list(claims_collection.find({}, {"_id": 0}))
    for claim in claims:
        policy = policies_collection.find_one({"policy_id": claim["policy_id"]}, {"_id": 0})
        policyholder = policyholders_collection.find_one({"policyholder_id": claim["policyholder_id"]}, {"_id": 0})

        claim["policy_type"] = policy["type"] if policy else "Unknown"
        claim["policyholder_name"] = policyholder["name"] if policyholder else "Unknown"

    return jsonify(claims)

@swag_from({
    'tags': ['Claims'],
    'summary': 'Update a claim',
    'description': 'Updates the details of a claim by its ID.',
    'parameters': [
        {
            'name': 'claim_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'example': 301
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'claim_amount': {'type': 'number', 'example': 6000.50},
                    'status': {'type': 'string', 'example': 'Approved'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Claim updated successfully'},
        404: {'description': 'Claim not found'}
    }
})

def update_claim(claim_id):
    data = request.json
    amount = data.get("amount")
    status = data.get("status")
    policy_id = data.get("policy_id")
    policyholder_id = data.get("policyholder_id")

    # Validate that claim_id, policy_id, policyholder_id, and amount are numbers
    if not isinstance(amount, (int, float)):
        return jsonify({"error": "Amount must be a number"}), 400

    if not isinstance(policy_id, int):
        return jsonify({"error": "Policy ID must be a number"}), 400

    if not isinstance(policyholder_id, int):
        return jsonify({"error": "Policyholder ID must be a number"}), 400

    # Validate that status contains only alphabets
    if not status.isalpha():
        return jsonify({"error": "Status must contain only alphabets"}), 400
        
    # Ensure claim exists
    claim = claims_collection.find_one({"claim_id": claim_id})
    if not claim:
        return jsonify({"error": "Claim not found"}), 404

    # Ensure policy exists for the claim
    policy = policies_collection.find_one({"policy_id": policy_id})
    if not policy:
        return jsonify({"error": "Policy not found"}), 400

    # Validate claim amount does not exceed policy amount
    #if amount > policy["amount"]:
        #return jsonify({"error": "Claim amount cannot exceed policy amount"}), 400

    # Update claim data
    claims_collection.update_one(
        {"claim_id": claim_id},
        {"$set": {"amount": amount, "status": status, "policy_id": policy_id, "policyholder_id": policyholder_id}}
    )
    return jsonify({"message": "Claim updated successfully"}), 200

@swag_from({
    'tags': ['Claims'],
    'summary': 'Delete a claim',
    'description': 'Deletes a claim by its ID.',
    'parameters': [
        {
            'name': 'claim_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'example': 301
        }
    ],
    'responses': {
        200: {'description': 'Claim deleted successfully'},
        404: {'description': 'Claim not found'}
    }
})

def delete_claim(claim_id):
    # Ensure claim exists
    claim = claims_collection.find_one({"claim_id": claim_id})
    if not claim:
        return jsonify({"error": "Claim not found"}), 404

    # Delete claim
    claims_collection.delete_one({"claim_id": claim_id})
    return jsonify({"message": "Claim deleted successfully"}), 200
