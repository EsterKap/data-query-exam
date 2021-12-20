import unittest
import random
import string
from datetime import datetime

from main.item import Item
from main.parser_error import ParseError
from main.service import Service


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.service = Service()

    def test_saves_and_responds_with_items(self):
        self.clean_items()
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
        self.clean_items()
        item1 = self.random_item()
        item2 = self.random_item()
        self.create_item(item1)
        self.create_item(item2)

        query = f'EQUAL(id,"{item2.id}")'
        response = self.get_items(query)
        self.assertEqual(response, [item2])

    def test_filter_items_based_on_not_query_string(self):
        self.clean_items()
        item1 = self.random_item()
        item2 = self.random_item()
        self.create_item(item1)
        self.create_item(item2)

        query = f'NOT(EQUAL(id,"{item1.id}"))'
        response = self.get_items(query)
        self.assertEqual(response, [item2])

    def test_filter_items_based_on_greater_less_query_string(self):
        self.clean_items()
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
        self.clean_items()
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
        self.clean_items()
        query = "INVALID"
        self.assertRaises(ParseError, self.get_items, query)

    def test_return_empty_when_no_item_found(self):
        self.clean_items()
        query = "EQUAL(id,'no_such_id')"
        response = self.get_items(query)
        self.assertEqual(response, [])

    def test_filter_items_with_equal_query_string(self):
        self.clean_items()
        item1 = self.random_item()
        item2 = self.random_item()
        self.create_item(item1)
        self.create_item(item2)
        item1.title = item2.title

        query = f'EQUAL(title,"{item2.title}")'
        response = self.get_items(query)
        self.assertIn(item2, response)
        self.assertIn(item1, response)

    def test_return_error_when_equal_invalid_string(self):
        self.clean_items()
        query = "EQUAL(INVALID)"
        self.assertRaises(ParseError, self.get_items, query)

    def test_return_error_when_less_than_invalid_string(self):
        self.clean_items()
        query = "LESS_THAN(INVALID)"
        self.assertRaises(ParseError, self.get_items, query)

    def test_return_error_when_greater_than_invalid_string(self):
        self.clean_items()
        query = "GREATER_THAN(INVALID)"
        self.assertRaises(ParseError, self.get_items, query)

    def test_return_error_when_equal_invalid_property_string(self):
        self.clean_items()
        item1 = self.random_item()
        self.create_item(item1)
        query = "EQUAL(total_views,5)"
        self.assertRaises(ParseError, self.get_items, query)

    def test_return_error_when_greater_than_invalid_property_string(self):
        self.clean_items()
        item1 = self.random_item()
        self.create_item(item1)
        query = "GREATER_THAN(total_views,5)"
        self.assertRaises(ParseError, self.get_items, query)

    def test_return_error_when_less_than_invalid_property_string(self):
        self.clean_items()
        item1 = self.random_item()
        self.create_item(item1)
        query = "LESS_THAN(total_views,5)"
        self.assertRaises(ParseError, self.get_items, query)

    def test_return_empty_when_list_empty_equal(self):
        self.clean_items()
        query = "EQUAL(views,5)"
        response = self.get_items(query)
        self.assertEqual(response, [])

    def test_return_empty_when_list_empty_greater_than(self):
        self.clean_items()
        query = "GREATER_THAN(views,5)"
        response = self.get_items(query)
        self.assertEqual(response, [])

    def test_return_empty_when_list_empty_less_than(self):
        self.clean_items()
        query = "LESS_THAN(views,5)"
        response = self.get_items(query)
        self.assertEqual(response, [])

    def test_return_error_when_invalid_property_value_type_less_than(self):
        self.clean_items()
        item1 = self.random_item()
        self.create_item(item1)
        item1.views = 1
        query = "LESS_THAN(views,'2')"
        self.assertRaises(ParseError, self.get_items, query)

        query = "LESS_THAN(views,'aaaaa')"
        self.assertRaises(ParseError, self.get_items, query)

    def test_return_error_when_invalid_property_value_type_greater_than(self):
        self.clean_items()
        item1 = self.random_item()
        self.create_item(item1)
        item1.views = 5
        query = "GREATER_THAN(views,'2')"
        self.assertRaises(ParseError, self.get_items, query)

        query = "GREATER_THAN(views,'aaaa')"
        self.assertRaises(ParseError, self.get_items, query)

    def test_filter_items_based_on_the_and_equal_query_string(self):
        self.clean_items()
        item1 = self.random_item()
        item2 = self.random_item()
        self.create_item(item1)
        self.create_item(item2)

        item1.views = 3
        query = f'AND(EQUAL(id,"{item1.id}"),EQUAL(views,3))'
        response = self.get_items(query)
        self.assertEqual(response, [item1])

        item2.views = 3
        query = f'AND(EQUAL(views,3),EQUAL(id,"{item1.id}"))'
        response = self.get_items(query)
        self.assertEqual(response, [item1])

    def test_filter_items_based_on_the_and_greater_less_than_query_string(self):
        self.clean_items()
        item1 = self.random_item()
        item2 = self.random_item()
        item3 = self.random_item()
        self.create_item(item1)
        self.create_item(item2)
        self.create_item(item3)
        item1.views = 3
        item2.views = 10
        item3.views = 5
        query = f'AND(GREATER_THAN(views,2),LESS_THAN(views,7))'
        response = self.get_items(query)
        self.assertIn(item1, response)
        self.assertIn(item3, response)

        query = f'AND(GREATER_THAN(views,6),LESS_THAN(views,11))'
        response = self.get_items(query)
        self.assertEqual(response, [item2])

    def test_filter_items_based_on_the_and_greater_less_than_not_query_string(self):
        self.clean_items()
        item1 = self.random_item()
        item2 = self.random_item()
        item3 = self.random_item()
        self.create_item(item1)
        self.create_item(item2)
        self.create_item(item3)
        item1.views = 3
        item2.views = 10
        item3.views = 5

        query = f'AND(NOT(GREATER_THAN(views,6)),LESS_THAN(views,11))'
        response = self.get_items(query)
        self.assertIn(item3, response)
        self.assertIn(item1, response)

        query = f'AND(NOT(GREATER_THAN(views,6)),NOT(LESS_THAN(views,11)))'
        response = self.get_items(query)
        self.assertEqual(response, [])

    def test_return_error_when_and_receive_invalid_operation_string(self):
        self.clean_items()
        query = f'AND(NOT1(GREATER_THAN(views,6)),LESS_THAN(views,11))'
        self.assertRaises(ParseError, self.get_items, query)
        query = f'AND(NOT(GREATER_THAN(views,6)))'
        self.assertRaises(ParseError, self.get_items, query)
        query = f'AND(NOT(GREATER_THAN(views,6)),LESS_THAN1(views,11))'
        self.assertRaises(ParseError, self.get_items, query)
        query = f'AND(INVALID)'
        self.assertRaises(ParseError, self.get_items, query)

    def test_return_error_when_or_receive_invalid_operation_string(self):
        self.clean_items()
        query = f'OR(NOT1(GREATER_THAN(views,6)),LESS_THAN(views,11))'
        self.assertRaises(ParseError, self.get_items, query)
        query = f'OR(NOT(GREATER_THAN(views,6)))'
        self.assertRaises(ParseError, self.get_items, query)
        query = f'OR(NOT(GREATER_THAN(views,6)),LESS_THAN1(views,11))'
        self.assertRaises(ParseError, self.get_items, query)
        query = f'OR(INVALID)'
        self.assertRaises(ParseError, self.get_items, query)

    def test_filter_items_based_on_not_greater_than_query_string(self):
        self.clean_items()
        item1 = self.random_item()
        item2 = self.random_item()
        self.create_item(item1)
        self.create_item(item2)
        item1.views = 10
        item2.views = 4

        query = f'NOT(GREATER_THAN(views,5))'
        response = self.get_items(query)
        self.assertEqual(response, [item2])

    def test_filter_items_based_on_not_less_than_query_string(self):
        self.clean_items()
        item1 = self.random_item()
        item2 = self.random_item()
        self.create_item(item1)
        self.create_item(item2)
        item1.views = 10
        item2.views = 4

        query = f'NOT(LESS_THAN(views,5))'
        response = self.get_items(query)
        self.assertEqual(response, [item1])

    def create_item(self, item: Item):
        self.service.save(item)

    def clean_items(self):
        self.service.clean_list()

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
