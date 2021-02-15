from flask import request, Blueprint
from datetime import datetime
from exceptions import NoSuchUser
import db_mapping

user_routes = Blueprint('users', __name__)

# error handlers
@user_routes.errorhandler(NoSuchUser)
def no_such_user_handler(e):
    return {"error": "no such user with id 1"}, 404


# routes
@user_routes.route('', methods=["POST"])
def create_user():
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


@user_routes.route('/<int:user_id>', methods=["GET"])
def get_user(user_id):
    try:
        user = db_mapping.USERS_TABLE[user_id]
    except KeyError:
        raise NoSuchUser(user_id)
    else:
        return user


@user_routes.route('/<int:user_id>', methods=["PUT"])
def put_user(user_id):
    if user_id not in db_mapping.USERS_TABLE:
        raise NoSuchUser(user_id)
    else:
        user = request.json
        user["registration_timestamp"] = db_mapping.USERS_TABLE[user_id]["registration_timestamp"]
        user['user_id'] = user_id
        db_mapping.USERS_TABLE[user_id] = user

        return {"status": "success"}


@user_routes.route('/<int:user_id>', methods=["DELETE"])
def delete_user(user_id):
    if user_id not in db_mapping.USERS_TABLE:
        raise NoSuchUser(user_id)
    else:
        db_mapping.USERS_TABLE.pop(user_id)
        return {"status": "success"}, 200
