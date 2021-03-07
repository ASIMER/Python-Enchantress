from flask import request
from datetime import datetime
from exceptions import NoSuchUser, NoSuchCart
import db_mapping
from flask_restful import Resource


class Cart(Resource):
    def post(self):
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

    def get(self, cart_id):
        try:
            cart = db_mapping.CARTS_TABLE[cart_id]
        except KeyError:
            raise NoSuchCart(cart_id)
        else:
            return cart

    def put(self, cart_id):
        if cart_id not in db_mapping.USERS_TABLE:
            raise NoSuchUser(cart_id)
        else:
            cart = request.json
            cart["creation_time"] = db_mapping.CARTS_TABLE[cart_id]["creation_time"]
            cart['cart_id'] = cart_id
            db_mapping.USERS_TABLE[cart_id] = cart

            return {"status": "success"}, 200

    def delete(self, cart_id):
        if cart_id not in db_mapping.CARTS_TABLE:
            raise NoSuchCart(cart_id)
        else:
            db_mapping.CARTS_TABLE.pop(cart_id)
            return {"status": "success"}, 200
