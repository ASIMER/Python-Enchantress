import psycopg2
from datetime import datetime

db_info = {
    'database': 'root',
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'port': '5432'
}

# Create a cursor - this is a special object that makes
# queries and receives their results



# HERE WILL BE OUR DATABASE WORK CODE
# Do not forget to close the database connection
def get_user_id(user_info):
    conn = psycopg2.connect(**db_info)
    cursor = conn.cursor()

    query = 'SELECT id FROM users ' \
            'WHERE name=%(name)s and email=%(email)s'
    cursor.execute(query,
                   user_info)
    reuslt = cursor.fetchall()
    conn.close()
    return reuslt


def get_cart_id(cart):
    conn = psycopg2.connect(**db_info)
    cursor = conn.cursor()

    query = 'SELECT id from cart ' \
            'WHERE user_id=%(user_id)s and creation_time=%(creation_time)s'
    cursor.execute(query, cart)
    reuslt = cursor.fetchall()
    conn.close()
    return reuslt


def create_user(user_info: dict):
    conn = psycopg2.connect(**db_info)
    cursor = conn.cursor()

    query = 'INSERT INTO users (name, email, registration_time) ' \
            'VALUES (%(name)s, %(email)s, %(registration_time)s)'
    reuslt = cursor.execute(query, user_info)
    conn.commit()

    conn.close()


def read_user_info(_id: int):
    conn = psycopg2.connect(**db_info)
    cursor = conn.cursor()

    query = 'SELECT * FROM users ' \
            'WHERE id=%(id)s'
    cursor.execute(query,
                  {"id": _id})
    reuslt = cursor.fetchall()
    conn.close()
    return reuslt


def update_user(new_info: dict, _id: int):
    conn = psycopg2.connect(**db_info)
    cursor = conn.cursor()

    new_info['id'] = _id
    query = 'UPDATE users ' \
            'SET name=%(name)s, email=%(email)s' \
            'WHERE id=%(id)s'
    cursor.execute(query, new_info)
    conn.commit()

    conn.close()


def delete_user(_id: int):
    conn = psycopg2.connect(**db_info)
    cursor = conn.cursor()

    query = 'DELETE FROM users ' \
            'WHERE id=%(id)s'
    cursor.execute(query, {'id': _id})
    conn.commit()

    conn.close()


def create_cart(cart: dict):
    conn = psycopg2.connect(**db_info)
    cursor = conn.cursor()

    # create cart
    query = 'INSERT INTO cart (user_id, creation_time) ' \
            'VALUES (%(user_id)s, %(creation_time)s)'
    cursor.execute(query, cart)
    conn.commit()

    # find cart id
    cart['cart_details']['cart_id'] = get_cart_id(cart)[0]
    # create cart_details
    query = 'INSERT INTO cart_details (cart_id, price, product) ' \
            'VALUES (%(cart_id)s, %(price)s, %(product)s)'

    cursor.execute(query, cart['cart_details'])
    conn.commit()

    conn.close()


def update_cart(cart: dict):
    conn = psycopg2.connect(**db_info)
    cursor = conn.cursor()

    query = 'UPDATE cart ' \
            'SET user_id=%(user_id)s, creation_time=%(creation_time)s ' \
            'WHERE id=%(id)s'
    cursor.execute(query, cart)
    conn.commit()

    conn.close()


def read_cart(_id: int):
    conn = psycopg2.connect(**db_info)
    cursor = conn.cursor()

    query = 'SELECT * FROM cart ' \
            'WHERE id=%(id)s'
    cursor.execute(query,
                   {"id": _id})
    reuslt = cursor.fetchall()
    conn.close()
    return reuslt


def delete_cart(_id: int):
    conn = psycopg2.connect(**db_info)
    cursor = conn.cursor()

    # delete cart_details
    query = 'DELETE FROM cart_details ' \
            'WHERE cart_id=%(id)s'
    cursor.execute(query, {'id': _id})

    # delete cart
    query = 'DELETE FROM cart ' \
            'WHERE id=%(id)s'
    cursor.execute(query, {'id': _id})
    conn.commit()

    conn.close()

# create_user({'name': "user", 'email': "test@gmail.com", datetime.today()})
# read_user_info(2)
# update_user({'name':'user', 'email':'test1@gmail.com'}, 19)
# delete_user(19)
# get_user_id({'name': "user", 'email': "test@gmail.com"})
"""create_cart({'user_id': "22",
             'creation_time': datetime.today(),
             'cart_details': {
                 'price': 22,
                 'product': 'test',
             }
})"""
#update_cart({'user_id': "22", "id": get_cart_id({})})
