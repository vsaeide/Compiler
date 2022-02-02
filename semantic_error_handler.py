class SemanticChecker:
    def __init__(self):
        self.errors = []

    def error(self, error_type, line_number, *args):
        # print(line_number)

        if error_type == 'type_1':
            self.errors.append('#' + str(line_number) +
                               ' : Semantic Error! \'{}\' is not defined.\n'.format(args[0]))
        elif error_type == 'type_2':
            self.errors.append('#' + str(line_number) +
                               ' : Semantic Error! Illegal type of void for \'{}\'.\n'.format(args[0]))
        elif error_type == 'type_3':
            self.errors.append('#' + str(line_number) +
                               ' : Semantic Error! Mismatch in numbers of arguments of \'{}\'.\n'.format(args[0]))
        elif error_type == 'type_4':
            self.errors.append('#' + str(line_number) +
                               ' : Semantic Error! No \'repeat ... until\' found for \'break\'.\n')
        elif error_type == 'type_5':
            self.errors.append('#' + str(line_number) +
                               ' : Semantic Error! Type mismatch in operands, Got {} instead of {}.\n'
                               .format(args[0], args[1]))
        elif error_type == 'type_6':
            self.errors.append('#' + str(line_number) +
                               ' : Semantic Error! Mismatch in type of argument {} for \'{}\'. Expected \'{}\' '
                               'but got \'{}\' instead.\n'.format(args[0], args[1], args[2], args[3]))
