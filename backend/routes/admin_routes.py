from flask import Blueprint, jsonify
from flask_login import login_required
from controllers.platform_management_controller import PlatformManagementController
from controllers.user_authentication_controller import UserAuthenticationController

# Blueprint for admin related routes
admin_bp = Blueprint('admin_bp', __name__)

# Initialize controllers
platform_management_controller = PlatformManagementController()
user_authentication_controller = UserAuthenticationController()

# Route to monitor platform stats
@admin_bp.route('/monitor', methods=['GET'])
@login_required
def monitor():
    platform_stats, status = platform_management_controller.monitor_platform()
    return jsonify(platform_stats), status

# Route to access dashboard data
@admin_bp.route('/dashboard', methods=['GET'])
@login_required
def access_dashboard():
    dashboard, status = platform_management_controller.dashboard_data() 
    return jsonify(dashboard), status

# Route to execute tasks
@admin_bp.route('/execute', methods=['POST'])
@login_required
def execute_tasks():
    result, status = platform_management_controller.execute_tasks()
    return jsonify(result), status

# Route to logout
@admin_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    response, status = user_authentication_controller.logout()
    return jsonify(response), status