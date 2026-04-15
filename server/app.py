#!/usr/bin/env python3

from flask import request, session, make_response
from flask_restful import Resource

from config import app, db, api
from models import User


with app.app_context():
    db.create_all()


class Signup(Resource):
    def post(self):
        data = request.get_json()

        try:
            user = User(username=data["username"])
            user.password_hash = data["password"]

            db.session.add(user)
            db.session.commit()

            session["user_id"] = user.id

            return make_response(user.to_dict(), 201)

        except Exception as e:
            return make_response({"error": str(e)}, 422)


class CheckSession(Resource):
    def get(self):
        user_id = session.get("user_id")

        if user_id:
            user = User.query.filter_by(id=user_id).first()
            if user:
                return make_response(user.to_dict(), 200)

        return make_response("", 204)


class Login(Resource):
    def post(self):
        data = request.get_json()

        user = User.query.filter_by(username=data["username"]).first()

        if user and user.authenticate(data["password"]):
            session["user_id"] = user.id
            return make_response(user.to_dict(), 200)

        return make_response({"error": "Unauthorized"}, 401)


class Logout(Resource):
    def delete(self):
        session.pop("user_id", None)
        return make_response({}, 204)


api.add_resource(Signup, "/signup")
api.add_resource(CheckSession, "/check_session")
api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")

if __name__ == "__main__":
    app.run(port=5555, debug=True) 