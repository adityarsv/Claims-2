from flask import request, jsonify
from models import policyholders_collection

# ------------------------ POLICYHOLDER CRUD ------------------------

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

def get_policyholders():
    policyholders = list(policyholders_collection.find({}, {"_id": 0}))
    return jsonify(policyholders)

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

def delete_policyholder(policyholder_id):
    # Find policyholder by ID
    policyholder = policyholders_collection.find_one({"policyholder_id": policyholder_id})
    if not policyholder:
        return jsonify({"error": "Policyholder not found"}), 404

    # Delete policyholder
    policyholders_collection.delete_one({"policyholder_id": policyholder_id})
    return jsonify({"message": "Policyholder deleted successfully"}), 200
