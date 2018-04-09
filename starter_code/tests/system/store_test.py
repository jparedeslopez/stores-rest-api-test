from ...models.item import ItemModel
from ...resources.store import StoreList
from ...tests.base_test import BaseTest
from ...models.store import StoreModel
import json

class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                request = client.post('/store/javi_store')

                self.assertIsNotNone(StoreModel.find_by_name('javi_store'))
                self.assertEqual(request.status_code, 201)
                self.assertDictEqual({'name': 'javi_store', 'items': []}, json.loads(request.data))


    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                request = client.post('/store/javi_store')
                self.assertIsNotNone(StoreModel.find_by_name('javi_store'))
                self.assertEqual(request.status_code, 201)

                request_two = client.post('/store/javi_store')
                self.assertDictEqual({'message': "A store with name 'javi_store' already exists."}, json.loads(request_two.data))
                self.assertEqual(request_two.status_code, 400)

    def test_remove_store(self):
        with self.app() as client:
            with self.app_context():
                create = client.post('store/javi_store')
                self.assertIsNotNone(StoreModel.find_by_name('javi_store'))
                self.assertEqual(create.status_code, 201)

                remove = client.delete('store/javi_store')
                self.assertIsNone(StoreModel.find_by_name('javi_store'))
                self.assertDictEqual({'message': 'Store deleted'}, json.loads(remove.data))


    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/javi_store')
                request = client.get('store/javi_store')

                self.assertEqual(request.status_code, 200)
                self.assertDictEqual({'name': 'javi_store', 'items': []}, json.loads(request.data))


    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                requesting = client.get('store/javi_store')

                self.assertEqual(requesting.status_code, 404)
                self.assertDictEqual({'message': 'Store not found'}, json.loads(requesting.data))

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('javi_store').save_to_db()
                ItemModel('test_item', 0.99, 1).save_to_db()

                store = client.get('/store/javi_store')
                #store_list = StoreList.get('/store/javi_store')
                self.assertDictEqual({'name': 'javi_store', 'items': [{'name': 'test_item', 'price': 0.99}]},
                                     json.loads(store.data))


    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('javi_store').save_to_db()

                store_list = client.get('/stores')
                self.assertDictEqual({'stores': [{'name': 'javi_store', 'items': []}]}, json.loads(store_list.data))


    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('javi_store').save_to_db()
                ItemModel('test_item', 0.99, 1).save_to_db()

                store = client.get('/stores')
                self.assertDictEqual({'stores': [{'name': 'javi_store', 'items': [{'name': 'test_item', 'price': 0.99}]}]},
                                                  json.loads(store.data))
