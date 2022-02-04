class Symbol:

    def __init__(self, name, address, scope, length, line_number, type):
        self.name = name
        self.address = address
        self.scope = scope
        self.length = length
        self.line_number = line_number
        self.type = type

    def __str__(self):
        output = '{}\t{}\t{}\t{}\t{}\t{}\n'.format(self.name, self.address, self.scope, self.length, self.line_number, self.type)
        return output