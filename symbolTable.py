from symbol import Symbol

class SymbolTable:

    def __init__(self):
        self.symbols = []

    def add_symbol(self, name, address, scope, length, line_number, type):
        self.symbols.append(Symbol(name, address, scope, length, line_number, type))

    def find_symbol_by_name(self, name, scope):
        for symbol in self.symbols:
            if symbol.name == name and symbol.scope == scope:
                return symbol
        for symbol in self.symbols:
            if symbol.name == name and symbol.scope is None:
                return symbol
        return 'first'

    def find_symbol_by_address(self, address, scope):
        for symbol in self.symbols:
            if symbol.address == address and (symbol.scope == scope or symbol.scope is None):
                return symbol

    def find_function_parameters(self, function_name, number_of_parameter):
        output = []
        for i in range(len(self.symbols)):
            if self.symbols[i].scope == function_name and len(output) < number_of_parameter:
                output.append(self.symbols[i])
        return output

    def is_first_function(self, function_name):
        first_function = ''
        for i in range(len(self.symbols)):
            if self.symbols[i].type.endswith('function'):
                first_function = self.symbols[i].name
                break
        return first_function == function_name

    def __str__(self):
        output = ''
        for symbol in self.symbols:
            output += str(symbol)
        return output