from flask import Flask, request
from datetime import datetime
from exceptions import NoSuchUser, NoSuchCart

amazon_killer = Flask(__name__)

# temporary variables to replace real database
USERS_TABLE, CARTS_TABLE = {}, {}

user_counter, cart_counter = 1, 1


# error handlers
@amazon_killer.errorhandler(NoSuchUser)
def no_such_user_handler(e):
    return {"error": "no such user with id 1"}, 404


@amazon_killer.errorhandler(NoSuchCart)
def no_such_cart_handler(e):
    return {"error": "no such cart with id 1"}, 404


# routes
@amazon_killer.route('/db_clear', methods=["POST"])
def db_clear():
    global user_counter, create_user, USERS_TABLE, CARTS_TABLE
    USERS_TABLE, CARTS_TABLE = {}, {}

    user_counter, cart_counter = 1, 1

    return {"status": "success"}, 200


# routes
@amazon_killer.route('/users', methods=["POST"])
def create_user():
    global user_counter
    user = request.json
    user['user_id'] = user_counter
    response = {
            "registration_timestamp": datetime.now().isoformat(),
            "user_id": user_counter
            }
    user["registration_timestamp"] = response['registration_timestamp']
    USERS_TABLE[user_counter] = user

    user_counter += 1

    return response, 201


@amazon_killer.route('/users/<int:user_id>', methods=["GET"])
def get_user(user_id):
    try:
        user = USERS_TABLE[user_id]
    except KeyError:
        raise NoSuchUser(user_id)
    else:
        return user


@amazon_killer.route('/users/<int:user_id>', methods=["PUT"])
def put_user(user_id):
    if user_id not in USERS_TABLE:
        raise NoSuchUser(user_id)
    else:
        user = request.json
        user["registration_timestamp"] = USERS_TABLE[user_id]["registration_timestamp"]
        user['user_id'] = user_id
        USERS_TABLE[user_id] = user

        return {"status": "success"}


@amazon_killer.route('/users/<int:user_id>', methods=["DELETE"])
def delete_user(user_id):
    if user_id not in USERS_TABLE:
        raise NoSuchUser(user_id)
    else:
        USERS_TABLE.pop(user_id)
        return {"status": "success"}, 200


@amazon_killer.route('/carts', methods=["POST"])
def create_cart():
    global cart_counter
    cart = request.json
    if cart['user_id'] not in USERS_TABLE:
        raise NoSuchUser(cart['user_id'])

    cart['cart_id'] = cart_counter
    response = {
            "cart_id": cart_counter,
            "creation_time": datetime.now().isoformat()
            }
    cart["creation_time"] = response['creation_time']
    CARTS_TABLE[cart_counter] = cart

    cart_counter += 1

    return response, 201


@amazon_killer.route('/carts/<int:cart_id>', methods=["GET"])
def get_cart(cart_id):
    try:
        cart = CARTS_TABLE[cart_id]
    except KeyError:
        raise NoSuchCart(cart_id)
    else:
        return cart


@amazon_killer.route('/carts/<int:cart_id>', methods=["PUT"])
def put_cart(cart_id):
    if cart_id not in USERS_TABLE:
        raise NoSuchUser(cart_id)
    else:
        cart = request.json
        cart["creation_time"] = CARTS_TABLE[cart_id]["creation_time"]
        cart['cart_id'] = cart_id
        USERS_TABLE[cart_id] = cart

        return {"status": "success"}, 200


@amazon_killer.route('/carts/<int:cart_id>', methods=["DELETE"])
def delete_cart(cart_id):
    if cart_id not in CARTS_TABLE:
        raise NoSuchCart(cart_id)
    else:
        CARTS_TABLE.pop(cart_id)
        return {"status": "success"}, 200


if __name__ == '__main__':
    amazon_killer.run(debug=True)
