import unittest
from datetime import datetime
from hw_functions import *
from random import randint

class DBTests(unittest.TestCase):
    def setUp(self) -> None:
        # save user info
        self.user_name = 'name' + str(randint(-99999, 99999))
        self.cart_user_name = 'cart_name' + str(randint(-99999, 99999))
        self.user_email = 'test@gmail.com'
        self.user_registration_time = datetime.today()

        # save cart info
        self.cart_creation_time = datetime.today()

        # save cart_details info
        self.cart_details_price = 22
        self.cart_details_product = 'test'

    def test_user(self):
        # save user info into dict
        user_info = {'name': self.user_name,
                     'email': self.user_email,
                     'registration_time': self.user_registration_time}
        update_user_info = {'name': self.user_name+'1',
                            'email': self.user_email}

        # create user
        create_user(user_info)
        self.user_id = get_user_id(user_info)[0][0]
        self.assertEqual(
            read_user_info(self.user_id)[0],
            (
            self.user_id,
            self.user_name,
            self.user_email,
            self.user_registration_time
            )
        )

        # update user
        update_user(update_user_info, self.user_id)
        self.assertEqual(
            read_user_info(self.user_id)[0],
            (
            self.user_id,
            update_user_info['name'],
            update_user_info['email'],
            self.user_registration_time
            )
        )

        # delete user
        delete_user(self.user_id)
        self.assertEqual(read_user_info(self.user_id), [])

    def test_cart(self):
        # save user info into dict
        user_info = {'name': self.cart_user_name,
                     'email': self.user_email,
                     'registration_time': self.user_registration_time}

        # create user
        create_user(user_info)
        self.user_id = get_user_id(user_info)[0][0]
        self.assertEqual(
            read_user_info(self.user_id)[0],
            (
            self.user_id,
            self.cart_user_name,
            self.user_email,
            self.user_registration_time
            )
        )

        # save cart info into dict
        cart_info = {
                'user_id': self.user_id,
                'creation_time': self.cart_creation_time,
                'cart_details': {
                        'price': self.cart_details_price,
                        'product': self.cart_details_product,
                        }
                }
        update_cart_info = {
                'user_id': self.user_id,
                'creation_time': datetime.today(),
                }

        # create cart
        create_cart(cart_info)
        self.cart_id = get_cart_id(cart_info)[0][0]
        self.assertEqual(
            read_cart(self.cart_id)[0],
            (
            self.cart_id,
            self.cart_creation_time,
            self.user_id
            )
        )

        # update cart
        update_cart_info['id'] = self.cart_id
        update_cart(update_cart_info)
        self.assertEqual(
            read_cart(self.cart_id)[0],
            (
            self.cart_id,
            update_cart_info['creation_time'],
            update_cart_info['user_id']
            )
        )

        # delete cart
        delete_cart(self.cart_id)
        self.assertEqual(read_cart(self.cart_id), [])

        # delete user
        print(self.user_id)
        delete_user(self.user_id)
        self.assertEqual(read_user_info(self.user_id), [])


if __name__ == '__main__':
    unittest.main()
