from flask import Flask
from cart_routes import cart_routes
from user_routes import user_routes
import db_mapping

amazon_killer = Flask(__name__)

amazon_killer.register_blueprint(cart_routes, url_prefix='/carts')
amazon_killer.register_blueprint(user_routes, url_prefix='/users')

# routes
@amazon_killer.route('/db_clear', methods=["POST"])
def db_clear():
    db_mapping.USERS_TABLE, db_mapping.CARTS_TABLE = {}, {}

    db_mapping.user_counter, db_mapping.cart_counter = 1, 1
    print(db_mapping.USERS_TABLE)
    return {"status": "success"}, 200


if __name__ == '__main__':
    amazon_killer.run(debug=True)
