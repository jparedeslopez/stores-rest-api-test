from models.item import ItemModel
from models.store import StoreModel
from models.user import UserModel
from tests.base_test import BaseTest
import json


class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel('javier', '123').save_to_db()
                auth_request = client.post('/auth',
                                                data=json.dumps({'username': 'javier', 'password': '123'}),
                                                headers={'Content-type': 'application/json'})
                auth_token = json.loads(auth_request.data)['access_token']
                self.access_token = f'JWT {auth_token}'

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/test', headers = {'Authorization': self.access_token})

                self.assertEqual(resp.status_code, 404)

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store')
                ItemModel('test', 0.99, 1).save_to_db()
                resp = client.get('/item/test', headers = {'Authorization': self.access_token})

                self.assertEqual(resp.status_code, 200)

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                ItemModel('test', 0.99, 1).save_to_db()

                resp = client.delete('item/test')
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'message': 'Item deleted'},
                                     json.loads(resp.data))

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()

                resp = client.post('item/test', data = {'price': 17.00, 'store_id': '1'})
                self.assertEqual(resp.status_code, 201)
                self.assertDictEqual({'name': 'test', 'price': 17.00},
                                    json.loads(resp.data))

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()

                client.post('item/test', data = {'price': 17.00, 'store_id': '1'})
                resp = client.post('item/test', data={'price': 17.00, 'store_id': '1'})

                self.assertDictEqual({'message': "An item with name 'test' already exists."},
                                     json.loads(resp.data))

    def test_put_item(self):
            with self.app() as client:
                with self.app_context():
                    StoreModel('test_store').save_to_db()
                    resp = client.put('item/test', data={'price': 18.00, 'store_id': '1'})
                    self.assertDictEqual({'name': 'test', 'price': 18.0},
                                         json.loads(resp.data))

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()

                client.post('item/test', data={'price': 17.00, 'store_id': '1'})
                resp = client.put('item/test', data={'price': 18.00, 'store_id': '1'})
                self.assertDictEqual({'name': 'test', 'price': 18.0},
                                     json.loads(resp.data))

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                ItemModel('test', 9.22, 1).save_to_db()

                resp = client.get('/items')

                self.assertDictEqual({'items': [{'name': 'test', 'price': 9.22}]},
                                     json.loads(resp.data))
