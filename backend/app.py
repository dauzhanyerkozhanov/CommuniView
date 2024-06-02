from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_admin import Admin
from flask_mail import Mail, Message
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from models import User, Business, Review, SpecialOffer, Bookmark, TrendingTag, BusinessClaim
from routes import user_routes, review_routes, bookmark_routes, admin_routes, trending_tag_routes, special_offer_routes, business_claim_routes, business_update_routes, search_routes
from dotenv import load_dotenv
import os
import admin_views


load_dotenv()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False


db = SQLAlchemy(app)
migrate = Migrate(app, db)

#Create the database tables
#db.create_all()


CORS(app)
mail = Mail(app)
admin = Admin(app, name='myapp', template_mode='bootstrap3')
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app.register_blueprint(user_routes.user_bp)
app.register_blueprint(business_update_routes.business_bp)
app.register_blueprint(review_routes.review_bp)
app.register_blueprint(bookmark_routes.bookmark_bp)
app.register_blueprint(admin_routes.admin_bp)
app.register_blueprint(search_routes.search_bp)
app.register_blueprint(trending_tag_routes.trending_tag_bp)
app.register_blueprint(special_offer_routes.special_offer_bp)
app.register_blueprint(business_claim_routes.business_claim_bp)


if __name__ == '__main__':
    app.run(debug=True)
@app.errorhandler(400)
def bad_request(e):
    return "Bad request", 400


@app.errorhandler(403)
def forbidden(e):
    return "Forbidden", 403


@app.errorhandler(500)
def internal_server_error(e):
    return "Internal server error", 500
