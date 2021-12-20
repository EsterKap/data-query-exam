from main.item import Item

class Service():

    def query(self, query: str = None) -> [Item]:
        '''
        Your code should be here !
        Query function gets a query string and returns a list of items matching the query.
        '''
        pass


    def save(self, item: Item) -> None:
        '''
        Your code should be here !
        Save item object to your data store.
        '''
        pass


class ParseError(Exception):
    "Parse action not found"
    pass

