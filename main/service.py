from main.item import Item
from main.operations import MangeOperations
from main.parser_error import ParseError


class Service:
    itemList: [Item] = []

    def query(self, query: str = None) -> [Item]:
        if not query:
            return self.itemList
        operation_service = MangeOperations()
        operation = operation_service.get_operation(query)
        if operation:
            return operation(query, self.itemList)
        raise ParseError(query, "can't execute query")

    def save(self, item: Item) -> None:
        self.itemList.append(item)

    def clean_list(self):
        self.itemList = []



