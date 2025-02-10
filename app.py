from flask import Flask
from policyholders import create_policyholder, get_policyholders, update_policyholder, delete_policyholder
from policies import create_policy, get_policies, update_policy, delete_policy
from claims import create_claim, get_claims, update_claim, delete_claim

app = Flask(__name__)

# ------------------------ ROUTES ------------------------
@app.route('/')
def home():
    return "Welcome to the Claims Management System!"

@app.route('/favicon.ico')
def favicon():
    return '', 204  # Return a 204 No Content status

# Policyholders Routes
app.add_url_rule('/policyholders', 'create_policyholder', create_policyholder, methods=['POST'])
app.add_url_rule('/policyholders', 'get_policyholders', get_policyholders, methods=['GET'])
app.add_url_rule('/policyholders/<int:policyholder_id>', 'update_policyholder', update_policyholder, methods=['PUT'])
app.add_url_rule('/policyholders/<int:policyholder_id>', 'delete_policyholder', delete_policyholder, methods=['DELETE'])

# Policies Routes
app.add_url_rule('/policies', 'create_policy', create_policy, methods=['POST'])
app.add_url_rule('/policies', 'get_policies', get_policies, methods=['GET'])
app.add_url_rule('/policies/<int:policy_id>', 'update_policy', update_policy, methods=['PUT'])
app.add_url_rule('/policies/<int:policy_id>', 'delete_policy', delete_policy, methods=['DELETE'])

# Claims Routes
app.add_url_rule('/claims', 'create_claim', create_claim, methods=['POST'])
app.add_url_rule('/claims', 'get_claims', get_claims, methods=['GET'])
app.add_url_rule('/claims/<int:claim_id>', 'update_claim', update_claim, methods=['PUT'])
app.add_url_rule('/claims/<int:claim_id>', 'delete_claim', delete_claim, methods=['DELETE'])

if __name__ == '__main__':
    app.run(debug=True)
