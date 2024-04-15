#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Plants(Resource):

    def get(self):
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(jsonify(plants), 200)

    def post(self):
        data = request.get_json()

        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price'],
        )

        db.session.add(new_plant)
        db.session.commit()

        return make_response(new_plant.to_dict(), 201)

api.add_resource(Plants, '/plants')


class PlantByID(Resource):

    def get(self,id):
        plant = Plant.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(plant),200)

    def patch(self, id):
        patch_plant = Plant.query.filter_by(id=id).first()
        
        data = request.get_json()

        for attr in data:
            setattr(patch_plant, attr, data[attr])

            db.session.add(patch_plant)
            db.session.commit()

            patch_plant_dict = patch_plant.to_dict()

            response = make_response(jsonify(patch_plant_dict), 200)
            return response
        
    def delete(self,id):
        
        delete = Plant.query.filter_by(id=id).first()

        db.session.delete(delete)
        db.session.commit()

        delete_dict = {
            "message": "Plant has been deleted"
        }

        response = make_response(delete_dict,204)
        return response

api.add_resource(PlantByID, '/plants/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)