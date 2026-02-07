# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
# # Ensure .env is loaded from the project root (not from an `instance/` folder).
# # The app does not rely on Flask's `instance` folder, so `instance/` is not required.
# from dotenv import load_dotenv
# import os

# # Prefer explicit .env in the project root next to this file. Falls back to
# # default `load_dotenv()` behavior if that file is missing.
# dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
# if os.path.exists(dotenv_path):
#     load_dotenv(dotenv_path)
# else:
#     load_dotenv()

# USER = os.getenv("user")
# PASSWORD = os.getenv("password")
# HOST = os.getenv("host")
# PORT = os.getenv("port")
# DBNAME = os.getenv("dbname")

# app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = (
#     f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"
# )
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# db = SQLAlchemy(app)
# api = Api(app)


# class UserModel(db.Model):
#     __tablename__ = "users"

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(80), unique=True, nullable=False)

#     def __repr__(self):
#         return f"User(name={self.name}, email={self.email})"



# class EquipmentModel(db.Model):
#     __tablename__ = "equipment"

#     id = db.Column(db.Integer, primary_key=True)
#     id_no = db.Column(db.String(120), unique=True, nullable=False)
#     maker_model_type = db.Column(db.String(255), nullable=False)
#     category = db.Column(db.String(120), nullable=False)
#     condition = db.Column(db.String(120), nullable=False)
#     deployment = db.Column(db.String(120), nullable=False)
#     quantity = db.Column(db.Integer, nullable=False)
#     location = db.Column(db.String(255), nullable=False)
#     date_received = db.Column(db.String(50), nullable=False)
#     description = db.Column(db.Text, nullable=True)

#     def __repr__(self):
#         return (
#             f"Equipment(id_no={self.id_no}, maker_model_type={self.maker_model_type}, "
#             f"category={self.category})"
#         )


# user_args = reqparse.RequestParser()
# user_args.add_argument("name", type=str, required=True, help="Name cannot be blank")
# user_args.add_argument("email", type=str, required=True, help="Email cannot be blank")


# equipment_args = reqparse.RequestParser()
# equipment_args.add_argument("id_no", type=str, required=True, help="ID No. cannot be blank")
# equipment_args.add_argument("maker_model_type", type=str, required=True, help="Maker/Model cannot be blank")
# equipment_args.add_argument("category", type=str, required=True, help="Category cannot be blank")
# equipment_args.add_argument("condition", type=str, required=True, help="Condition cannot be blank")
# equipment_args.add_argument("deployment", type=str, required=True, help="Deployment cannot be blank")
# equipment_args.add_argument("quantity", type=int, required=True, help="Quantity cannot be blank")
# equipment_args.add_argument("location", type=str, required=True, help="Location cannot be blank")
# equipment_args.add_argument("date_received", type=str, required=True, help="Date Received cannot be blank")
# equipment_args.add_argument("description", type=str, required=False)


# userFields = {
#     "id": fields.Integer,
#     "name": fields.String,
#     "email": fields.String,
# }


# equipmentFields = {
#     "id": fields.Integer,
#     "ID No.": fields.String(attribute="id_no"),
#     "Maker,Model & Type": fields.String(attribute="maker_model_type"),
#     "Category": fields.String(attribute="category"),
#     "Condition": fields.String(attribute="condition"),
#     "Deployment": fields.String(attribute="deployment"),
#     "Quantity": fields.Integer(attribute="quantity"),
#     "Location": fields.String(attribute="location"),
#     "Date Received": fields.String(attribute="date_received"),
#     "Description": fields.String(attribute="description"),
# }

# class Users(Resource):
#     @marshal_with(userFields)
#     def get(self):
#         return UserModel.query.all()

#     @marshal_with(userFields)
#     def post(self):
#         args = user_args.parse_args()
#         user = UserModel(name=args["name"], email=args["email"])
#         db.session.add(user)
#         db.session.commit()
#         return user, 201


# class User(Resource):
#     @marshal_with(userFields)
#     def get(self, id):
#         user = UserModel.query.get(id)
#         if not user:
#             abort(404, message="User not found")
#         return user

#     @marshal_with(userFields)
#     def patch(self, id):
#         args = user_args.parse_args()
#         user = UserModel.query.get(id)
#         if not user:
#             abort(404, message="User not found")

#         user.name = args["name"]
#         user.email = args["email"]
#         db.session.commit()
#         return user

#     def delete(self, id):
#         user = UserModel.query.get(id)
#         if not user:
#             abort(404, message="User not found")

#         db.session.delete(user)
#         db.session.commit()
#         return {"message": "User deleted"}, 200


# class Equipments(Resource):
#     @marshal_with(equipmentFields)
#     def get(self):
#         return EquipmentModel.query.all()

#     @marshal_with(equipmentFields)
#     def post(self):
#         args = equipment_args.parse_args()
#         equipment = EquipmentModel(
#             id_no=args["id_no"],
#             maker_model_type=args["maker_model_type"],
#             category=args["category"],
#             condition=args["condition"],
#             deployment=args["deployment"],
#             quantity=args["quantity"],
#             location=args["location"],
#             date_received=args["date_received"],
#             description=args.get("description"),
#         )
#         db.session.add(equipment)
#         db.session.commit()
#         return equipment, 201


# class Equipment(Resource):
#     @marshal_with(equipmentFields)
#     def get(self, id):
#         equipment = EquipmentModel.query.get(id)
#         if not equipment:
#             abort(404, message="Equipment not found")
#         return equipment

#     @marshal_with(equipmentFields)
#     def patch(self, id):
#         args = equipment_args.parse_args()
#         equipment = EquipmentModel.query.get(id)
#         if not equipment:
#             abort(404, message="Equipment not found")

#         equipment.id_no = args["id_no"]
#         equipment.maker_model_type = args["maker_model_type"]
#         equipment.category = args["category"]
#         equipment.condition = args["condition"]
#         equipment.deployment = args["deployment"]
#         equipment.quantity = args["quantity"]
#         equipment.location = args["location"]
#         equipment.date_received = args["date_received"]
#         equipment.description = args.get("description")
#         db.session.commit()
#         return equipment

#     def delete(self, id):
#         equipment = EquipmentModel.query.get(id)
#         if not equipment:
#             abort(404, message="Equipment not found")

#         db.session.delete(equipment)
#         db.session.commit()
#         return {"message": "Equipment deleted"}, 200

# api.add_resource(Users, "/api/users/")
# api.add_resource(User, "/api/users/<int:id>")
# api.add_resource(Equipments, "/api/equipment/")
# api.add_resource(Equipment, "/api/equipment/<int:id>")

# @app.route("/")
# def home():
#     return "<h1>Flask REST API</h1>"


# if __name__ == "__main__":
#     with app.app_context():
#         db.create_all() 
#     app.run(debug=True)
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from dotenv import load_dotenv
import os

# Load .env
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    load_dotenv()

USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

app = Flask(__name__)

# Postgres config
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
api = Api(app)

# ====================== Models ======================
class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)

class EquipmentModel(db.Model):
    __tablename__ = "equipment"
    id = db.Column(db.Integer, primary_key=True)
    id_no = db.Column(db.String(120), unique=True, nullable=False)
    maker_model_type = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(120), nullable=False)
    condition = db.Column(db.String(120), nullable=False)
    deployment = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    date_received = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)

# ====================== Request Parsers ======================
user_args = reqparse.RequestParser()
user_args.add_argument("name", type=str, required=True, help="Name cannot be blank")
user_args.add_argument("email", type=str, required=True, help="Email cannot be blank")

equipment_args = reqparse.RequestParser()
equipment_args.add_argument("id_no", type=str, required=True)
equipment_args.add_argument("maker_model_type", type=str, required=True)
equipment_args.add_argument("category", type=str, required=True)
equipment_args.add_argument("condition", type=str, required=True)
equipment_args.add_argument("deployment", type=str, required=True)
equipment_args.add_argument("quantity", type=int, required=True)
equipment_args.add_argument("location", type=str, required=True)
equipment_args.add_argument("date_received", type=str, required=True)
equipment_args.add_argument("description", type=str, required=False)

# ====================== Fields ======================
userFields = {"id": fields.Integer, "name": fields.String, "email": fields.String}
equipmentFields = {
    "id": fields.Integer,
    "ID No.": fields.String(attribute="id_no"),
    "Maker,Model & Type": fields.String(attribute="maker_model_type"),
    "Category": fields.String(attribute="category"),
    "Condition": fields.String(attribute="condition"),
    "Deployment": fields.String(attribute="deployment"),
    "Quantity": fields.Integer(attribute="quantity"),
    "Location": fields.String(attribute="location"),
    "Date Received": fields.String(attribute="date_received"),
    "Description": fields.String(attribute="description"),
}

# ====================== Resources ======================
class Users(Resource):
    @marshal_with(userFields)
    def get(self):
        return UserModel.query.all()

    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(name=args["name"], email=args["email"])
        db.session.add(user)
        db.session.commit()
        return user, 201

class User(Resource):
    @marshal_with(userFields)
    def get(self, id):
        user = UserModel.query.get(id)
        if not user:
            abort(404, message="User not found")
        return user

    @marshal_with(userFields)
    def patch(self, id):
        args = user_args.parse_args()
        user = UserModel.query.get(id)
        if not user:
            abort(404, message="User not found")
        user.name = args["name"]
        user.email = args["email"]
        db.session.commit()
        return user

    def delete(self, id):
        user = UserModel.query.get(id)
        if not user:
            abort(404, message="User not found")
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}, 200

class Equipments(Resource):
    @marshal_with(equipmentFields)
    def get(self):
        return EquipmentModel.query.all()

    @marshal_with(equipmentFields)
    def post(self):
        args = equipment_args.parse_args()
        equipment = EquipmentModel(**args)
        db.session.add(equipment)
        db.session.commit()
        return equipment, 201

class Equipment(Resource):
    @marshal_with(equipmentFields)
    def get(self, id):
        equipment = EquipmentModel.query.get(id)
        if not equipment:
            abort(404, message="Equipment not found")
        return equipment

    @marshal_with(equipmentFields)
    def patch(self, id):
        args = equipment_args.parse_args()
        equipment = EquipmentModel.query.get(id)
        if not equipment:
            abort(404, message="Equipment not found")
        for key, value in args.items():
            setattr(equipment, key, value)
        db.session.commit()
        return equipment

    def delete(self, id):
        equipment = EquipmentModel.query.get(id)
        if not equipment:
            abort(404, message="Equipment not found")
        db.session.delete(equipment)
        db.session.commit()
        return {"message": "Equipment deleted"}, 200

# ====================== API Routes ======================
api.add_resource(Users, "/api/users/")
api.add_resource(User, "/api/users/<int:id>")
api.add_resource(Equipments, "/api/equipment/")
api.add_resource(Equipment, "/api/equipment/<int:id>")

@app.route("/")
def home():
    return "<h1>Flask REST API</h1>"

# ====================== Run for Local Dev ======================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT",8000))
    app.run(host="0.0.0.0", port=8000, debug=True)
