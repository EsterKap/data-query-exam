import re
from main.item import Item
from main.parser_error import ParseError


class MangeOperations:

    def equal_operation(self, query: str, items_list: [Item]) -> [Item]:
        property_val = split_field(query, "EQUAL")
        self.check_property(property_val, "EQUAL")
        if items_list:
            self.check_property_exists(items_list[0], property_val[0], "EQUAL")
        return [item for item in items_list if str(getattr(item, property_val[0])) == property_val[1].replace("\"", '')]

    def greater_than_operation(self, query: str, items_list: [Item]) -> [Item]:
        property_val = split_field(query, "GREATER_THAN")
        self.check_property(property_val, "GREATER_THAN")
        if items_list:
            self.check_property_exists(items_list[0], property_val[0], "GREATER_THAN")
            self.check_property_type_int(items_list[0], property_val[0], "GREATER_THAN")
            self.check_propery_value_int(property_val[1], "GREATER_THAN")
            return [item for item in items_list if getattr(item, property_val[0]) >= int(property_val[1])]
        return items_list

    def less_than_operation(self, query: str, items_list: [Item]) -> [Item]:
        property_val = split_field(query, "LESS_THAN")
        self.check_property(property_val, "LESS_THAN")
        if items_list:
            self.check_property_exists(items_list[0], property_val[0], "LESS_THAN")
            self.check_property_type_int(items_list[0], property_val[0], "LESS_THAN")
            self.check_propery_value_int(property_val[1], "LESS_THAN")
            return [item for item in items_list if getattr(item, property_val[0]) < int(property_val[1])]
        return items_list

    def and_operation(self, query: str, items_list: [Item]) -> [Item]:
        and_fields = re.match(r'AND\((.*\)),(.*)\)', query)
        if not and_fields or len(and_fields.groups()) > 2:
            raise ParseError("AND", "AND expecting two arguments")
        first_operation = self.get_operation(and_fields.group(1))
        first_operation_result = first_operation(and_fields.group(1), items_list)
        second_operation = self.get_operation(and_fields.group(2))
        return second_operation(and_fields.group(2), first_operation_result)

    def or_operation(self, query: str, items_list: [Item]) -> [Item]:
        or_fields = re.match(r'OR\((.*\)),(.*)\)', query)
        if not or_fields or len(or_fields.groups()) > 2:
            raise ParseError("OR", "OR expecting two arguments")
        first_operation = self.get_operation(or_fields.group(1))
        first_op_results = first_operation(or_fields.group(1), items_list)
        second_operation = self.get_operation(or_fields.group(2))
        second_opt_result = second_operation(or_fields.group(2), items_list)
        return first_op_results + second_opt_result

    def not_operation(self, query: str, items_list: [Item]) -> [Item]:
        not_fields = re.match(r'NOT\((.*)\)', query)
        operation = self.get_operation(not_fields.group(1))
        return_val_res = operation(not_fields.group(1), items_list)
        return [item for item in items_list if item not in return_val_res]

    def get_operation(self, query):
        if query.startswith("EQUAL("):
            return self.equal_operation
        if query.startswith("GREATER_THAN("):
            return self.greater_than_operation
        if query.startswith("LESS_THAN("):
            return self.less_than_operation
        if query.startswith("AND("):
            return self.and_operation
        if query.startswith("OR("):
            return self.or_operation
        if query.startswith("NOT("):
            return self.not_operation
        raise ParseError("operation", "can't execute query")

    def check_property_type_int(self, item: Item, feild: str, operation: str):
        if type(getattr(item, feild)) != int:
            raise ParseError(operation, "Valid only for int attributes.")

    def check_propery_value_int(self, property_val: str, operation: str):
        try:
            int(property_val)
        except ValueError:
            raise ParseError(operation, f"Can't convert value to int ")

    def check_property(self, property_val: [], operation: str):
        if len(property_val) != 2:
            raise ParseError(f"{operation}", f"{operation} expecting two arguments")

    def check_property_exists(self, item: Item, item_property: str, operation: str):
        if not hasattr(item, item_property):
            raise ParseError(f"{operation}", f"item doesn't have {item_property} attribute")


def split_field(query: str, operation: str) -> [str]:
    match_str = f'{operation}\((.*)\)'
    property_and_val = re.match(match_str, query)
    return property_and_val.group(1).split(",")
