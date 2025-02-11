from flask import request, jsonify
from flasgger import Swagger
from flasgger import swag_from
from models import policyholders_collection


# ------------------------ POLICYHOLDER CRUD ------------------------
@swag_from({
    'tags': ['Policyholders'],
    'summary': 'Create a new policyholder',
    'description': 'This endpoint creates a new policyholder.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'policyholder_id': {'type': 'integer', 'example': 101},
                    'name': {'type': 'string', 'example': 'John Doe'}
                }
            }
        }
    ],
    'responses': {
        201: {'description': 'Policyholder created successfully'},
        400: {'description': 'Policyholder with this ID already exists'}
    }
})

def create_policyholder():
    data = request.json
    policyholder_id = data.get("policyholder_id")
    name = data.get("name")

    # Validate that policyholder_id is unique
    existing_policyholder = policyholders_collection.find_one({"policyholder_id": policyholder_id})
    if existing_policyholder:
        return jsonify({"error": "Policyholder with this ID already exists"}), 400

    new_policyholder = {
        "policyholder_id": policyholder_id,
        "name": name
    }

    policyholders_collection.insert_one(new_policyholder)
    return jsonify({"message": "Policyholder created successfully"}), 201

@swag_from({
    'tags': ['Policyholders'],
    'summary': 'Get all policyholders',
    'description': 'Retrieves a list of all policyholders.',
    'responses': {
        200: {
            'description': 'A list of policyholders',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'policyholder_id': {'type': 'integer'},
                        'name': {'type': 'string'}
                    }
                }
            }
        }
    }
})

def get_policyholders():
    policyholders = list(policyholders_collection.find({}, {"_id": 0}))
    return jsonify(policyholders)

@swag_from({
    'tags': ['Policyholders'],
    'summary': 'Update a policyholder',
    'description': 'Updates the name of a policyholder by their ID.',
    'parameters': [
        {
            'name': 'policyholder_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'example': 101
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string', 'example': 'Jane Doe'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Policyholder updated successfully'},
        404: {'description': 'Policyholder not found'}
    }
})

def update_policyholder(policyholder_id):
    data = request.json
    name = data.get("name")

    # Find policyholder by ID
    policyholder = policyholders_collection.find_one({"policyholder_id": policyholder_id})
    if not policyholder:
        return jsonify({"error": "Policyholder not found"}), 404

    # Update policyholder data
    policyholders_collection.update_one(
        {"policyholder_id": policyholder_id},
        {"$set": {"name": name}}
    )
    return jsonify({"message": "Policyholder updated successfully"}), 200

@swag_from({
    'tags': ['Policyholders'],
    'summary': 'Delete a policyholder',
    'description': 'Deletes a policyholder by their ID.',
    'parameters': [
        {
            'name': 'policyholder_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'example': 101
        }
    ],
    'responses': {
        200: {'description': 'Policyholder deleted successfully'},
        404: {'description': 'Policyholder not found'}
    }
})

def delete_policyholder(policyholder_id):
    # Find policyholder by ID
    policyholder = policyholders_collection.find_one({"policyholder_id": policyholder_id})
    if not policyholder:
        return jsonify({"error": "Policyholder not found"}), 404

    # Delete policyholder
    policyholders_collection.delete_one({"policyholder_id": policyholder_id})
    return jsonify({"message": "Policyholder deleted successfully"}), 200
