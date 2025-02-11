from flask import Flask
from flask_jwt_extended import JWTManager, jwt_required
from config import JWT_SECRET_KEY
from flask_cors import CORS
from auth import auth_bp
from policyholders import create_policyholder, get_policyholders, update_policyholder, delete_policyholder
from policies import create_policy, get_policies, update_policy, delete_policy
from claims import create_claim, get_claims, update_claim, delete_claim
from flasgger import Swagger

app = Flask(__name__)
CORS(app)
swagger = Swagger(app)


# JWT Configuration
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
jwt = JWTManager(app)

# Register authentication routes
app.register_blueprint(auth_bp)

# ------------------------ ROUTES ------------------------
@app.route('/')
def home():
    return "Welcome to the Claims Management System!"

@app.route('/favicon.ico')
def favicon():
    return '', 204

# Policyholders Routes (Protected)
app.add_url_rule('/policyholders', 'create_policyholder', jwt_required()(create_policyholder), methods=['POST'])
app.add_url_rule('/policyholders', 'get_policyholders', jwt_required()(get_policyholders), methods=['GET'])
app.add_url_rule('/policyholders/<int:policyholder_id>', 'update_policyholder', jwt_required()(update_policyholder), methods=['PUT'])
app.add_url_rule('/policyholders/<int:policyholder_id>', 'delete_policyholder', jwt_required()(delete_policyholder), methods=['DELETE'])

# Policies Routes (Protected)
app.add_url_rule('/policies', 'create_policy', jwt_required()(create_policy), methods=['POST'])
app.add_url_rule('/policies', 'get_policies', jwt_required()(get_policies), methods=['GET'])
app.add_url_rule('/policies/<int:policy_id>', 'update_policy', jwt_required()(update_policy), methods=['PUT'])
app.add_url_rule('/policies/<int:policy_id>', 'delete_policy', jwt_required()(delete_policy), methods=['DELETE'])

# Claims Routes (Protected)
app.add_url_rule('/claims', 'create_claim', jwt_required()(create_claim), methods=['POST'])
app.add_url_rule('/claims', 'get_claims', jwt_required()(get_claims), methods=['GET'])
app.add_url_rule('/claims/<int:claim_id>', 'update_claim', jwt_required()(update_claim), methods=['PUT'])
app.add_url_rule('/claims/<int:claim_id>', 'delete_claim', jwt_required()(delete_claim), methods=['DELETE'])

if __name__ == '__main__':
    app.run(debug=True)
