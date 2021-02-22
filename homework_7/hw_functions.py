import psycopg2

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
def conn_mgr(func):
    # connection manager decorator
    def wrapper(*args, **kwargs):
        conn = psycopg2.connect(**db_info)
        cursor = conn.cursor()
        try:
            if 'conn' in func.__code__.co_varnames:
                # check function parameter names, for conn parameter
                result = func(*args, cursor=cursor, conn=conn, **kwargs)
            else:
                result = func(*args, cursor=cursor, **kwargs)

            conn.commit()
        finally:
            conn.close()
        return result
    return wrapper


@conn_mgr
def get_user_id(user_info, cursor):

    query = 'SELECT id FROM users ' \
            'WHERE name=%(name)s and email=%(email)s'
    cursor.execute(query,
                   user_info)
    reuslt = cursor.fetchall()
    return reuslt


@conn_mgr
def get_cart_id(cart, cursor):
    query = 'SELECT id from cart ' \
            'WHERE user_id=%(user_id)s and creation_time=%(creation_time)s'
    cursor.execute(query, cart)
    reuslt = cursor.fetchall()
    return reuslt


@conn_mgr
def create_user(user_info: dict, cursor):
    query = 'INSERT INTO users (name, email, registration_time) ' \
            'VALUES (%(name)s, %(email)s, %(registration_time)s)'
    cursor.execute(query, user_info)


@conn_mgr
def read_user_info(_id: int, cursor):
    query = 'SELECT * FROM users ' \
            'WHERE id=%(id)s'
    cursor.execute(query,
                   {"id": _id})
    reuslt = cursor.fetchall()
    return reuslt


@conn_mgr
def update_user(new_info: dict, _id: int, cursor):
    new_info['id'] = _id
    query = 'UPDATE users ' \
            'SET name=%(name)s, email=%(email)s' \
            'WHERE id=%(id)s'
    cursor.execute(query, new_info)


@conn_mgr
def delete_user(_id: int, cursor):
    query = 'DELETE FROM users ' \
            'WHERE id=%(id)s'
    cursor.execute(query, {'id': _id})


@conn_mgr
def create_cart(cart: dict, cursor, conn):
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


@conn_mgr
def update_cart(cart: dict, cursor):
    query = 'UPDATE cart ' \
            'SET user_id=%(user_id)s, creation_time=%(creation_time)s ' \
            'WHERE id=%(id)s'
    cursor.execute(query, cart)


@conn_mgr
def read_cart(_id: int, cursor):
    query = 'SELECT * FROM cart ' \
            'WHERE id=%(id)s'
    cursor.execute(query,
                   {"id": _id})
    reuslt = cursor.fetchall()
    return reuslt


@conn_mgr
def delete_cart(_id: int, cursor):
    # delete cart_details
    query = 'DELETE FROM cart_details ' \
            'WHERE cart_id=%(id)s'
    cursor.execute(query, {'id': _id})

    # delete cart
    query = 'DELETE FROM cart ' \
            'WHERE id=%(id)s'
    cursor.execute(query, {'id': _id})
