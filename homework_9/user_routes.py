from flask import request
from datetime import datetime
from exceptions import NoSuchUser
import db_mapping
from flask_restful import Resource


class User(Resource):
    def post(self):
        user = request.json
        user['user_id'] = db_mapping.user_counter
        response = {
                "registration_timestamp": datetime.now().isoformat(),
                "user_id": db_mapping.user_counter
                }
        user["registration_timestamp"] = response['registration_timestamp']
        db_mapping.USERS_TABLE[db_mapping.user_counter] = user

        db_mapping.user_counter += 1

        return response, 201

    def get(self, user_id):
        try:
            user = db_mapping.USERS_TABLE[user_id]
        except KeyError:
            raise NoSuchUser(user_id)
        else:
            return user

    def put(self, user_id):
        if user_id not in db_mapping.USERS_TABLE:
            raise NoSuchUser(user_id)
        else:
            user = request.json
            user["registration_timestamp"] = db_mapping.USERS_TABLE[user_id]["registration_timestamp"]
            user['user_id'] = user_id
            db_mapping.USERS_TABLE[user_id] = user

            return {"status": "success"}

    def delete(self, user_id):
        if user_id not in db_mapping.USERS_TABLE:
            raise NoSuchUser(user_id)
        else:
            db_mapping.USERS_TABLE.pop(user_id)
            return {"status": "success"}, 200
