import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_restful import Api, Resource, abort, fields, marshal_with, reqparse

from auth import auth_bp
from extensions import db, jwt


dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    load_dotenv()


api = Api()


def get_env_value(key, default=None):
    value = os.getenv(key, default)
    if isinstance(value, str):
        return value.strip()
    return value


def build_database_uri():
    user = get_env_value("user")
    password = get_env_value("password")
    host = get_env_value("host")
    port = get_env_value("port")
    dbname = get_env_value("dbname")
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
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

equipment_fields = {
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


class Equipments(Resource):
    @marshal_with(equipment_fields)
    def get(self):
        return EquipmentModel.query.all()

    @marshal_with(equipment_fields)
    def post(self):
        args = equipment_args.parse_args()
        equipment = EquipmentModel(**args)
        db.session.add(equipment)
        db.session.commit()
        return equipment, 201


class Equipment(Resource):
    @marshal_with(equipment_fields)
    def get(self, id):
        equipment = EquipmentModel.query.get(id)
        if not equipment:
            abort(404, message="Equipment not found")
        return equipment

    @marshal_with(equipment_fields)
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


api.add_resource(Equipments, "/api/equipments")
api.add_resource(Equipment, "/api/equipments/<int:id>")


def create_app(test_config=None):
    app = Flask(__name__)

    CORS(app)

    app.config["SQLALCHEMY_DATABASE_URI"] = build_database_uri()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = get_env_value("JWT_SECRET_KEY", "change-me-in-production")

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    jwt.init_app(app)
    api.init_app(app)
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    @app.route("/")
    def home():
        return "<h1>Flask REST API</h1>"

    return app


app = create_app()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    port = int(get_env_value("APP_PORT", 8000))
    app.run(host="127.0.0.1", port=port, debug=True, use_reloader=False)
