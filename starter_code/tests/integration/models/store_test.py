from ....models.item import ItemModel
from ....models.store import StoreModel
from ....tests.base_test import BaseTest

class StoreTest(BaseTest):
    def test_create_store_empty_items(self):
        store = StoreModel('test')

        self.assertListEqual(store.items.all, [])


    def test_crud(self):
        with self.app_context():
            store = StoreModel('test')

            self.assertIsNone(StoreModel.find_by_name('test'))

            store.save_to_db()

            self.assertIsNotNone(StoreModel.find_by_name('test'))

            store.delete_from_db()

            self.assertIsNone(StoreModel.find_by_name('test'))


    def test_relationship(self):
        with self.app_context():
            store = StoreModel('test_store')
            item = ItemModel('test_item', 10.55, 1)
            store.save_to_db()
            item.save_to_db()

            self.assertEqual(store.items.count(), 1)
            self.assertEqual(store.items.first().name, "test_item")


    def test_json(self):
        with self.app_context():
            store = StoreModel('test')
            item = ItemModel('test_item', 10.55, 1)

            store.save_to_db()
            item.save_to_db()

            expected = {
                'name': 'test',
                'items': [{'name': 'test_item', 'price': 10.55}]
            }

            self.assertEqual(store.json(), expected)


