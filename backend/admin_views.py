from flask_admin.contrib.sqla import ModelView
from models import User, Business, Review, SpecialOffer, Bookmark, TrendingTag, BusinessClaim
from database import db
from app import admin


# Create admin views for each model
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Business, db.session))
admin.add_view(ModelView(Review, db.session))
admin.add_view(ModelView(SpecialOffer, db.session))
admin.add_view(ModelView(Bookmark, db.session))
admin.add_view(ModelView(TrendingTag, db.session))
admin.add_view(ModelView(BusinessClaim, db.session))
