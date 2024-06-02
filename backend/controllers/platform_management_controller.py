from models import User, Business, Review
import dashboard as Dashboard
from database import db

# Controller for managing the platform
class PlatformManagementController:
    def __init__(self):
        # Initialize the dashboard
        self.dashboard = Dashboard()

    # Method to monitor the platform
    def monitor_platform(self):
        try:
            # Count the number of users, businesses, and reviews
            user_count = User.query.count()
            business_count = Business.query.count()
            review_count = Review.query.count()

            # Prepare the platform statistics
            platform_stats = {
                'users': user_count,
                'businesses': business_count,
                'reviews': review_count
            }

            # Return the platform statistics
            return platform_stats, 200
        except Exception as e:
            # Handle any exceptions that occur during the monitoring process
            return {'error': str(e)}, 500

    # Method to execute tasks
    def execute_tasks(self):
        try:
            # Monitor the platform and get the metrics
            platform_metrics, status = self.monitor_platform()
            if status == 200:
                # Update the dashboard with the latest metrics
                self.dashboard.update_metrics(platform_metrics)
                # Return a success message
                return {'message': 'Platform metrics updated successfully.'}, 200
            # If monitoring failed, return the error
            return platform_metrics, status
        except Exception as e:
            # Handle any exceptions that occur during the task execution process
            return {'error': str(e)}, 500
            
    # Method to get the dashboard data
    def dashboard_data(self):
        try:
            # Get the metrics from the dashboard
            dashboard_info = self.dashboard.get_metrics()
            # Return the dashboard metrics
            return dashboard_info, 200
        except Exception as e:
            # Handle any exceptions that occur during the data retrieval process
            return {'error': str(e)}, 500