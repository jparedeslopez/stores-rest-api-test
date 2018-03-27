from models.store import StoreModel
from tests.unit.unit_base_test import UnitBaseTest

# only the init method is unit testeble. ALl the other stuff depend on some kind of reation with the other dn
class StoreTest(UnitBaseTest):
    def test_create_store(self):
        store = StoreModel('test_store')

        self.assertEqual(store.name, 'test_store')

