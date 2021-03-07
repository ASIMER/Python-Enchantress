from flask import Flask
from flask_restful import Resource, Api
from cart_routes import Cart
from user_routes import User
from exceptions import NoSuchUser, NoSuchCart
import db_mapping

amazon_killer = Flask(__name__)
api = Api(amazon_killer)


@amazon_killer.errorhandler(NoSuchCart)
def no_such_cart_handler(e):
    return {"error": "no such cart with id 1"}, 404


# error handlers
@amazon_killer.errorhandler(NoSuchUser)
def no_such_user_handler(e):
    return {"error": "no such user with id 1"}, 404


# routes
class DbClear(Resource):
    def post(self):
        db_mapping.USERS_TABLE, db_mapping.CARTS_TABLE = {}, {}

        db_mapping.user_counter, db_mapping.cart_counter = 1, 1
        return {"status": "success"}, 200

api.add_resource(DbClear, '/db_clear')
api.add_resource(Cart, '/carts', '/carts/<int:cart_id>')
api.add_resource(User, '/users', '/users/<int:user_id>')

if __name__ == '__main__':
    amazon_killer.run(debug=True)
