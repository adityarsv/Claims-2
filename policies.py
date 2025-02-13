from flask import request, jsonify
from flasgger import Swagger
from flasgger import swag_from
from models import policies_collection, policyholders_collection

# ------------------------ POLICY CRUD ------------------------
@swag_from({
    'tags': ['Policies'],
    'summary': 'Create a new policy',
    'description': 'This endpoint creates a new policy for a policyholder.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'policy_id': {'type': 'integer', 'example': 201},
                    'policyholder_id': {'type': 'integer', 'example': 101},
                    'policy_type': {'type': 'string', 'example': 'Health Insurance'}
                }
            }
        }
    ],
    'responses': {
        201: {'description': 'Policy created successfully'},
        400: {'description': 'Policy with this ID already exists'}
    }
})

def create_policy():
    data = request.json
    policy_id = data.get("policy_id")
    type = data.get("type")
    amount = data.get("amount")
    policyholder_id = data.get("policyholder_id")

    # Validate that policy_id, policyholder_id, and amount are numbers
    if not isinstance(policy_id, int):
        return jsonify({"error": "Policy ID must be a number"}), 400

    if not isinstance(policyholder_id, int):
        return jsonify({"error": "Policyholder ID must be a number"}), 400

    if not isinstance(amount, (int, float)):
        return jsonify({"error": "Amount must be a number"}), 400

    # Validate that type contains only letters
    if not type.isalpha():
        return jsonify({"error": "Policy type must contain only letters"}), 400
        
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

@swag_from({
    'tags': ['Policies'],
    'summary': 'Get all policies',
    'description': 'Retrieves a list of all policies.',
    'responses': {
        200: {
            'description': 'A list of policies',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'policy_id': {'type': 'integer'},
                        'policyholder_id': {'type': 'integer'},
                        'policy_type': {'type': 'string'}
                    }
                }
            }
        }
    }
})

def get_policies():
    policies = list(policies_collection.find({}, {"_id": 0}))
    for policy in policies:
        policyholder = policyholders_collection.find_one({"policyholder_id": policy["policyholder_id"]}, {"_id": 0})
        policy["policyholder_name"] = policyholder["name"] if policyholder else "Unknown"
    return jsonify(policies)

@swag_from({
    'tags': ['Policies'],
    'summary': 'Update a policy',
    'description': 'Updates the details of a policy by its ID.',
    'parameters': [
        {
            'name': 'policy_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'example': 201
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'policy_type': {'type': 'string', 'example': 'Auto Insurance'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Policy updated successfully'},
        404: {'description': 'Policy not found'}
    }
})

def update_policy(policy_id):
    data = request.json
    type = data.get("type")
    amount = data.get("amount")
    policyholder_id = data.get("policyholder_id")

    # Validate that type contains only letters
    if not type.isalpha():
        return jsonify({"error": "Policy type must contain only letters"}), 400

    # Validate that policyholder_id and amount are numbers
    if not isinstance(policyholder_id, int):
        return jsonify({"error": "Policyholder ID must be a number"}), 400

    if not isinstance(amount, (int, float)):
        return jsonify({"error": "Amount must be a number"}), 400
        
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

@swag_from({
    'tags': ['Policies'],
    'summary': 'Delete a policy',
    'description': 'Deletes a policy by its ID.',
    'parameters': [
        {
            'name': 'policy_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'example': 201
        }
    ],
    'responses': {
        200: {'description': 'Policy deleted successfully'},
        404: {'description': 'Policy not found'}
    }
})

def delete_policy(policy_id):
    # Ensure policy exists
    policy = policies_collection.find_one({"policy_id": policy_id})
    if not policy:
        return jsonify({"error": "Policy not found"}), 404

    # Delete policy
    policies_collection.delete_one({"policy_id": policy_id})
    return jsonify({"message": "Policy deleted successfully"}), 200
