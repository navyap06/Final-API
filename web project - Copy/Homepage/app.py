from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_restful import Api
from models import db
from api import (
    UserResource,
    LeaveRequestListResource, LeaveRequestResource
)
import routes

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///leave_app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'

db.init_app(app)
login_manager = LoginManager(app)
api = Api(app)


api.add_resource(UserResource, "/api/users/<int:user_id>")
api.add_resource(LeaveRequestListResource, "/api/leaves")
api.add_resource(LeaveRequestResource, "/api/leaves/<int:leave_id>")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
