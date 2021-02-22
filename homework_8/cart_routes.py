from flask import request, Blueprint
from datetime import datetime
from exceptions import NoSuchUser, NoSuchCart
import db_mapping

cart_routes = Blueprint('carts', __name__)
@cart_routes.errorhandler(NoSuchCart)
def no_such_cart_handler(e):
    return {"error": "no such cart with id 1"}, 404

# error handlers
@cart_routes.errorhandler(NoSuchUser)
def no_such_user_handler(e):
    return {"error": "no such user with id 1"}, 404


@cart_routes.route('', methods=["POST"])
def create_cart():
    cart = request.json
    if cart['user_id'] not in db_mapping.USERS_TABLE:
        raise NoSuchUser(cart['user_id'])

    cart['cart_id'] = db_mapping.cart_counter
    response = {
            "cart_id": db_mapping.cart_counter,
            "creation_time": datetime.now().isoformat()
            }
    cart["creation_time"] = response['creation_time']
    db_mapping.CARTS_TABLE[db_mapping.cart_counter] = cart

    db_mapping.cart_counter += 1

    return response, 201


@cart_routes.route('/<int:cart_id>', methods=["GET"])
def get_cart(cart_id):
    try:
        cart = db_mapping.CARTS_TABLE[cart_id]
    except KeyError:
        raise NoSuchCart(cart_id)
    else:
        return cart


@cart_routes.route('/<int:cart_id>', methods=["PUT"])
def put_cart(cart_id):
    if cart_id not in db_mapping.USERS_TABLE:
        raise NoSuchUser(cart_id)
    else:
        cart = request.json
        cart["creation_time"] = db_mapping.CARTS_TABLE[cart_id]["creation_time"]
        cart['cart_id'] = cart_id
        db_mapping.USERS_TABLE[cart_id] = cart

        return {"status": "success"}, 200


@cart_routes.route('/<int:cart_id>', methods=["DELETE"])
def delete_cart(cart_id):
    if cart_id not in db_mapping.CARTS_TABLE:
        raise NoSuchCart(cart_id)
    else:
        db_mapping.CARTS_TABLE.pop(cart_id)
        return {"status": "success"}, 200
