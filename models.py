from config import get_db

db = get_db()

# Define collections
policyholders_collection = db.policyholders
policies_collection = db.policies
claims_collection = db.claims
users_collection = db.users