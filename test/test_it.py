import unittest
import random
import string
from datetime import datetime

from main.item import Item
from main.service import Service, ParseError

class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.service = Service()

    def test_saves_and_responds_with_items(self):
        item1 = self.random_item()
        item2 = self.random_item()
        item3 = self.random_item()
        self.create_item(item1)
        self.create_item(item2)
        self.create_item(item3)

        response = self.get_all_items()
        self.assertIn(item1, response)
        self.assertIn(item2, response)
        self.assertIn(item3, response)

    def test_filter_items_based_on_equal_query_string(self):
        item1 = self.random_item()
        item2 = self.random_item()
        self.create_item(item1)
        self.create_item(item2)

        query = f'EQUAL(id,"{item2.id}")'
        response = self.get_items(query)
        self.assertEqual(response, [item2])

    def test_filter_items_based_on_not_query_string(self):
        item1 = self.random_item()
        item2 = self.random_item()
        self.create_item(item1)
        self.create_item(item2)

        query = f'NOT(EQUAL(id,"{item1.id}"))'
        response = self.get_items(query)
        self.assertEqual(response, [item2])

    def test_filter_items_based_on_greater_less_query_string(self):
        item1 = self.random_item()
        item1.views = 3
        item2 = self.random_item()
        item2.views = 10
        self.create_item(item1)
        self.create_item(item2)

        query = 'GREATER_THAN(views,5)'
        response = self.get_items(query)
        self.assertEqual(response, [item2])

        query = 'LESS_THAN(views,5)'
        response = self.get_items(query)
        self.assertEqual(response, [item1])

    def test_filter_items_based_on_the_or_and_query_string(self):
        item1 = self.random_item()
        item2 = self.random_item()
        item3 = self.random_item()
        self.create_item(item1)
        self.create_item(item2)
        self.create_item(item3)

        query = f'OR(EQUAL(id,"{item1.id}"),EQUAL(id,"{item2.id}"))'
        response = self.get_items(query)
        self.assertIn(item1, response)
        self.assertIn(item2, response)

    def test_return_error_when_invalid_query_passed(self):
        query = "INVALID"
        self.assertRaises(ParseError, self.get_items, query)

    def test_return_empty_when_no_item_found(self):
        query = "EQUAL(id,'no_such_id')"
        response = self.get_items(query)
        self.assertEqual(response, [])


    def create_item(self, item: Item):
        self.service.save(item)

    def get_all_items(self):
        return self.service.query()

    def get_items(self, query):
        return self.service.query(query)


    def random_string(self, length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    def random_int(self):
        return random.randint(1, 10)

    def random_timestamp(self):
        dt = datetime.now()
        return int(dt.strftime('%Y%m%d'))

    def random_item(self):
        id = self.random_string(10)
        title = self.random_string(20)
        content = self.random_string(30)
        views = self.random_int()
        timestamp = self.random_timestamp()
        return Item(id=id, title=title, content=content, views=views, timestamp=timestamp)

if __name__ == '__main__':
    unittest.main()
