class Symbol:

    def __init__(self, name, address, scope, length, line_number, type):
        self.name = name
        self.address = address
        self.scope = scope
        self.length = length
        self.line_number = line_number
        self.type = type


class SymbolTable:
    def __init__(self):
        self.symbols = []

    def add_symbol(self, name, address, scope, length, starts_at, type):
        self.symbols.append(Symbol(name, address, scope, length, starts_at, type))

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

    def get_func_params(self, function_name, number_of_parameter):
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
