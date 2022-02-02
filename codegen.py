from stack import Stack
from symbol import *
from semantic_error_handler import *


class CodeGenerator:
    def __init__(self):

        self.index = 0
        self.semantic_stack = Stack()
        self.symbol_table = SymbolTable()
        self.semantic_checker = SemanticChecker()

        self.symbol_table.add_symbol('output', 500, None, 1, 0, 'void')
        self.symbol_table.add_symbol('temp', 504, None, 1, 0, 'int')
        #TODO

        self.break_stack = Stack()
        self.current_scope = None
        self.pb = [''] * 500
        self.pb[0] = '(ASSIGN, #0, 500, )'
        self.data_index = 508
        self.temp_index = 2000
        self.main_index = 1


    def code_gen(self, action_symbol, token=None, line_num=None):

        if action_symbol == 'pid':
            self.pid(token, line_num)
        elif action_symbol == 'pnum':
            self.pnum(token)
        elif action_symbol == 'operator':
            self.operator(token)
        elif action_symbol == 'type':
            self.type(token)
        elif action_symbol == 'function_call':
            self.function_call(line_num)
        elif action_symbol == 'break':
            self._break(line_num)
        elif action_symbol == 'assign':
            self.assign(line_num)
        elif action_symbol == 'mult':
            self.mult(line_num)
        elif action_symbol == 'check_type':
            self.check_type(line_num)
        elif action_symbol == 'relop':
            self.relop(line_num)
        elif action_symbol == 'add_or_sub':
            self.add_or_sub(line_num)
        elif action_symbol == 'define_id':
            self.define_id(token)
        else:
            method_to_call = getattr(self, action_symbol)
            method_to_call() #without input param


    def get_temp(self):
        temp = self.temp_index
        self.temp_index += 4
        return temp


    def jp_main(self):

        line_num = self.symbol_table.find_symbol_by_name('main', None).line_number
        temp = self.pb[self.main_index - 1]
        self.pb[self.main_index - 1] = '(JP, {}, , )'.format(line_num - 2)
        self.pb[self.main_index] = temp

    def start_function(self):

        function = self.symbol_table.symbols[-1]
        function.type = function.type + '_function'

        if self.symbol_table.is_first_function(function.name):
            self.main_index = self.index
            self.index += 1
        #TODO
        self.current_scope = function.name
        self.symbol_table.add_symbol('return_' + function.name, function.address + 4, None, 0, self.index,
                                     function.type)
        self.pb[self.index] = '(ASSIGN, #0, {}, )'.format(self.data_index)
        self.data_index += 4
        self.index += 1

    def define_function(self):
        function = self.symbol_table.find_symbol_by_name(self.current_scope, None)
        function.line_number = self.index

    def loop(self):
        self.break_stack.push(self.index)
        self.index += 2

    def end_function(self):
        if self.current_scope == 'main':
            function_return = self.symbol_table.find_symbol_by_name('return_' + self.current_scope, None)
            self.pb[self.index] = '(ASSIGN, #{}, {}, )'.format(self.index + 2, function_return.address)
            self.index += 1
        function_return = self.symbol_table.find_symbol_by_name('return_' + self.current_scope, None)
        self.pb[self.index] = '(JP, @{}, , )'.format(function_return.address)
        self.index += 1
        self.current_scope = None
        self.semantic_stack.empty()

    def add_param(self):
        function = self.symbol_table.find_symbol_by_name(self.current_scope, None)
        function.length += 1

    def array_input(self):
        self.symbol_table.symbols[-1].type = self.symbol_table.symbols[-1].type + '_array_input'

    def _break(self, line_num):
        if self.break_stack.size > 0:
            self.pb[self.index] = '(JP, {}, , )'.format(self.break_stack.top() + 1)
            self.index += 1
        else:
            self.semantic_checker.error('type_4', line_num)


    def _return(self):
        function_return = self.symbol_table.find_symbol_by_name('return_' + self.current_scope, None)
        self.pb[self.index] = '(JP, @{}, , )'.format(function_return.address)
        self.index += 1

    def return_value(self):
        function = self.symbol_table.find_symbol_by_name(self.current_scope, None)
        self.pb[self.index] = '(ASSIGN, {}, {}, )'.format(self.semantic_stack.top(), function.address)
        self.semantic_stack.pop(1)
        self.index += 1
        function_return = self.symbol_table.find_symbol_by_name('return_' + self.current_scope, None)
        self.pb[self.index] = '(JP, @{}, , )'.format(function_return.address)
        self.index += 1

    def start_function_call(self):
        function = self.symbol_table.find_symbol_by_address(self.semantic_stack.top(), None)
        self.semantic_stack.pop(1)
        if function.name != 'output':
            self.semantic_stack.push(function.name)
        else:
            self.semantic_stack.push('output')

    def function_call(self, line_num):
        n_params = 0
        while not isinstance(self.semantic_stack.get_from_top(n_params), str) or \
                (isinstance(self.semantic_stack.get_from_top(n_params), str) and
                 self.semantic_stack.get_from_top(n_params).startswith('#')) or \
                (isinstance(self.semantic_stack.get_from_top(n_params), str) and
                 self.semantic_stack.get_from_top(n_params).startswith('@')):
            n_params += 1

        function = self.symbol_table.find_symbol_by_name(self.semantic_stack.get_from_top(n_params), None)
        if function.length != n_params:
            # print("error")
            self.semantic_checker.error('type_3', line_num, function.name)
            self.semantic_stack.pop(n_params + 1)
            temp = self.get_temp()
            self.semantic_stack.push(temp)
            return

        else:
            if function.name != 'output':
                params = self.symbol_table.get_func_params(function.name, function.length)
                params.reverse()
                for param in params:
                    if param.type.endswith('_array_input'):
                        if isinstance(self.semantic_stack.top(), str):
                            # print("error")
                            self.semantic_checker.error('type_6', line_num, function.length - params.index(param), function.name, 'array', 'int')
                            self.semantic_stack.pop(n_params - params.index(param) + 1)
                            temp = self.get_temp()
                            self.semantic_stack.push(temp)
                            return

                        else:
                            array = self.symbol_table.find_symbol_by_address(self.semantic_stack.top(),
                                                                             self.current_scope)
                            if array.type.endswith('_array') or array.type.endswith('_array_input'):
                                #TODO
                                start=self.semantic_stack.top()

                                self.pb[self.index] = '(ASSIGN, {}, {}, )'.format("#"+str(start), param.address)
                            else:
                                # print("error")
                                self.semantic_checker.error('type_6', line_num, function.length - params.index(param), function.name, 'array', 'int')
                                self.semantic_stack.pop(n_params - params.index(param) + 1)
                                temp = self.get_temp()
                                self.semantic_stack.push(temp)
                                return
                    else:
                        if not isinstance(self.semantic_stack.top(), str) and self.semantic_stack.top() < 1000:
                            var = self.symbol_table.find_symbol_by_address(self.semantic_stack.top(),
                                                                           self.current_scope)
                        elif (not isinstance(self.semantic_stack.top(), str) and self.semantic_stack.top() >= 1000) \
                                or isinstance(self.semantic_stack.top(), str):
                            var = self.semantic_stack.top()
                        else:
                            var = None

                        if (isinstance(var, Symbol) and var.type == 'int') or (isinstance(var, int)) or \
                                (isinstance(var, str) and var[1:].isdigit()):
                            self.pb[self.index] = '(ASSIGN, {}, {}, )'.format(self.semantic_stack.top(), param.address)
                        else:
                            # print("error")
                            self.semantic_checker.error('type_6', line_num,function.length - params.index(param), function.name, 'int', 'array')
                            self.semantic_stack.pop(n_params - params.index(param) + 1)
                            temp = self.get_temp()
                            self.semantic_stack.push(temp)
                            return


                    self.index += 1
                    self.semantic_stack.pop(1)

                self.pb[self.index] = '(ASSIGN, #{}, {}, )'.format(self.index + 2, function.address + 4)
                self.index += 1
                self.pb[self.index] = '(JP, {}, , )'.format(function.line_number)
                self.index += 1
                self.semantic_stack.pop(1)
                if function.type == 'int_function':
                    t = self.get_temp()
                    self.pb[self.index] = '(ASSIGN, {}, {}, )'.format(function.address, t)
                    self.index += 1
                    self.semantic_stack.push(t)
                else:
                    t = self.get_temp()
                    self.semantic_stack.push(t)
            else:
                self.output()

    def type(self, token):
        self.semantic_stack.push(token)

    def define_id(self, token):
        t = self.semantic_stack.top()
        self.semantic_stack.pop(1)
        self.symbol_table.add_symbol(token, self.data_index, self.current_scope, 0, self.index, t)
        self.data_index += 4
        self.semantic_stack.push(self.symbol_table.symbols[-1].address)
        self.pb[self.index] = '(ASSIGN, #0, {}, )'.format(self.semantic_stack.top())
        self.index += 1

    def check_type(self, line_num):
        symbol = self.symbol_table.symbols[-1]
        if symbol.type == 'void':
            # print("error")
            self.semantic_checker.error('type_2', line_num, symbol.name)
            symbol.type = 'int'


    def pid(self, token, line_num):
        p = self.symbol_table.find_symbol_by_name(token, self.current_scope)
        if p != 'first':
            self.semantic_stack.push(p.address)
        else:
            # print("error")
            self.semantic_checker.error('type_1', line_num, token)
            self.semantic_stack.push(self.symbol_table.symbols[1].address)

    def pop(self):
        self.semantic_stack.pop()

    def pnum(self, token):
        self.semantic_stack.push('#{}'.format(token))

    def save_array(self):
        array_size = self.semantic_stack.get_from_top(0)
        array_size = int(array_size.replace('#', ''))
        symbol = self.symbol_table.symbols[-1]
        symbol.length = array_size
        symbol.type = symbol.type + '_array'
        for i in range(array_size - 1):
            self.pb[self.index] = '(ASSIGN, #{}, {}, )'.format(0, self.data_index)
            self.index += 1
            self.data_index += 4
        self.pb[self.index] = '(ASSIGN, #{}, {}, )'.format(symbol.address, self.data_index)
        self.data_index += 4
        self.index += 1
        self.semantic_stack.pop(2)

    def save(self):
        self.semantic_stack.push(self.index)
        self.index += 1

    def jpf(self):

        self.pb[self.semantic_stack.top()] = '(JPF, {}, {}, )'.format(self.semantic_stack.get_from_top(1),self.index + 1)
        self.semantic_stack.pop(2)
        self.semantic_stack.push(self.index)
        self.index += 1

    def endif(self):
        self.pb[self.semantic_stack.top()] = '(JPF, {}, {}, )'.format(self.semantic_stack.get_from_top(1),self.index)
        self.semantic_stack.pop(2)


    def jp(self):
        self.pb[self.semantic_stack.top()] = '(JP, {}, , )'.format(self.index)
        self.semantic_stack.pop()

    def label(self):
        self.semantic_stack.push(self.index)

    def until(self):
        self.pb[self.index]='(JPF, {}, {}, )'.format(self.semantic_stack.get_from_top(0),
                                                                      self.semantic_stack.get_from_top(1))
        self.index += 1
        self.semantic_stack.pop(2)
        start = self.break_stack.top()
        self.break_stack.pop(1)
        self.pb[start] = '(JP, {}, , )'.format(start + 2)
        self.pb[start + 1] = '(JP, {}, , )'.format(self.index)


    def assign(self, line_num):
        type_1 = self.get_type(self.semantic_stack.top())
        type_2 = self.get_type(self.semantic_stack.get_from_top(1))
        if type_1 == 'array' or type_2 == 'array':
            self.semantic_checker.error('type_5', line_num, 'array', 'int')
        elif type_1 == 'function' or type_2 == 'function':
            self.semantic_checker.error('type_5', line_num, 'function', 'int')
        self.pb[self.index] = '(ASSIGN, {}, {}, )'.format(self.semantic_stack.top(),
                                                          self.semantic_stack.get_from_top(1))
        temp = self.semantic_stack.top()
        self.index += 1
        self.semantic_stack.pop(2)
        self.semantic_stack.push(temp)

    def address_array(self):
        t = self.get_temp()
        self.pb[self.index] = '(MULT, {}, #4, {})'.format(self.semantic_stack.top(), t)
        self.semantic_stack.pop()
        self.index += 1
        symbol = self.symbol_table.find_symbol_by_address(self.semantic_stack.top(), self.current_scope)
        if symbol.type.endswith('_array_input'):
            self.pb[self.index] = '(ADD, {}, {}, {})'.format(self.semantic_stack.top(), t, t)
        else:
            self.pb[self.index] = '(ADD, #{}, {}, {})'.format(self.semantic_stack.top(), t, t)
        self.semantic_stack.pop()
        self.index += 1
        self.semantic_stack.push('@' + str(t))

    def relop(self, line_num):
        type_1 = self.get_type(self.semantic_stack.top())
        type_2 = self.get_type(self.semantic_stack.get_from_top(2))
        if type_1 == 'array' or type_2 == 'array':
            self.semantic_checker.error('type_5', line_num, 'array', 'int')
        elif type_1 == 'function' or type_2 == 'function':
            self.semantic_checker.error('type_5', line_num, 'function', 'int')
        addr = self.get_temp()
        if self.semantic_stack.get_from_top(1) == '<':
            self.pb[self.index] = '(LT, {}, {}, {})'.format(self.semantic_stack.get_from_top(2),
                                                            self.semantic_stack.top(), addr)
        elif self.semantic_stack.get_from_top(1) == '==':
            self.pb[self.index] = '(EQ, {}, {}, {})'.format(self.semantic_stack.top(),
                                                            self.semantic_stack.get_from_top(2), addr)
        self.index += 1
        self.semantic_stack.pop(3)
        self.semantic_stack.push(addr)


    def operator(self, token):
        self.semantic_stack.push(token)

    def add_or_sub(self, line_num):
        type_1 = self.get_type(self.semantic_stack.top())
        type_2 = self.get_type(self.semantic_stack.get_from_top(2))
        if type_1 == 'array' or type_2 == 'array':
            self.semantic_checker.error('type_5', line_num, 'array', 'int')
        elif type_1 == 'function' or type_2 == 'function':
            self.semantic_checker.error('type_5', line_num, 'function', 'int')
        t = self.get_temp()
        if self.semantic_stack.get_from_top(1) == '+':
            self.pb[self.index] = '(ADD, {}, {}, {})'.format(self.semantic_stack.top(),
                                                             self.semantic_stack.get_from_top(2), t)
        if self.semantic_stack.get_from_top(1) == '-':
            self.pb[self.index] = '(SUB, {}, {}, {})'.format(self.semantic_stack.get_from_top(2),
                                                             self.semantic_stack.top(), t)
        self.index += 1
        self.semantic_stack.pop(3)
        self.semantic_stack.push(t)

    def mult(self, line_num):
        type_1 = self.get_type(self.semantic_stack.top())
        type_2 = self.get_type(self.semantic_stack.get_from_top(1))
        if type_1 == 'array' or type_2 == 'array':
            self.semantic_checker.error('type_5', line_num, 'array', 'int')
        elif type_1 == 'function' or type_2 == 'function':
            self.semantic_checker.error('type_5', line_num, 'function', 'int')
        t = self.get_temp()
        self.pb[self.index] = '(MULT, {}, {}, {})'.format(self.semantic_stack.top(),
                                                          self.semantic_stack.get_from_top(1), t)
        self.index += 1
        self.semantic_stack.pop(2)
        self.semantic_stack.push(t)



    def output(self):
        self.pb[self.index] = '(PRINT, {}, , )'.format(self.semantic_stack.top())
        self.index += 1
        self.semantic_stack.pop(1)

    def get_type(self, param):
        if isinstance(param, str):
            return 'int'
        else:
            if param >= 1000:
                return 'int'
            else:
                par_symbol = self.symbol_table.find_symbol_by_address(param, self.current_scope)
                if par_symbol.type == 'int':
                    return 'int'
                elif par_symbol.type == 'int_function':
                    return 'function'
                else:
                    return 'array'

