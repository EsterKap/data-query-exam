
class ParseError(Exception):

    def __init__(self, operation, message="operation got exception"):
        self.operation = operation
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.operation} -> {self.message}'
