from scanner import Scanner
from Package1.First import first
from Package1.Follow import follow
from anytree import Node
from anytree import RenderTree
from codegen import CodeGenerator


class parser:

    def __init__(self):
        self.scanner = Scanner('./input.txt')
        self.look_ahead = ""
        self.syn_err_l = list()
        self.state = 0
        self.root = Node("Program")
        self.next_token()
        self.code_generator = CodeGenerator()
        self.Program(self.root)

    def next_token(self):

        self.cpl_token = self.scanner.get_next_token()

        if self.cpl_token == '$':
            self.look_ahead = '$'
            self.token = '$'
        elif self.cpl_token[0] == 'NUM' or self.cpl_token[0] == 'ID':
            self.look_ahead = self.cpl_token[0]
            self.token = "(" + self.cpl_token[0] + ", " + self.cpl_token[1] + ")"
        else:
            self.look_ahead = self.cpl_token[1]
            self.token = "(" + self.cpl_token[0] + ", " + self.cpl_token[1] + ")"

    def EOF_error(self):
        if self.look_ahead == '$':
            error_msg = "#" + str(self.scanner.line_num - 1) + " : syntax error, Unexpected EOF"
            self.syn_err_l.append(error_msg)
            #self.output()
            #TODO
            return True
        return False

    def output(self):

        flag = False

        # with open("parse_tree.txt", 'w', encoding='utf-8') as file:  # parse_tree file
        #     for pre, _, node in RenderTree(self.root):
        #         if flag:
        #             file.write("\n%s%s" % (pre, node.name))
        #         else:
        #             file.write("%s%s" % (pre, node.name))
        #             flag = True
        #
        # with open("syntax_errors.txt", "w") as file:  # syntax errors file
        #     if len(self.syn_err_l) == 0:
        #         file.write("There is no syntax error.")
        #     else:
        #         for l in self.syn_err_l:
        #             file.write(l + "\n")

        with open("output.txt", 'w') as file:
            if len(self.code_generator.semantic_checker.errors) > 0:
                file.write('The code has not been generated.')
            else:
                for idx, l in enumerate(self.code_generator.pb):
                    if l != '':
                        file.write('{}\t{}\n'.format(idx, l))

        with open("semantic_errors.txt", "w") as file:  # semantic errors file
            for err in self.code_generator.semantic_checker.errors:
                # print(self.code_generator.semantic_checker.errors)
                file.write(err)

    ###################################################################3

    def Program(self, parent_node, state=0):

        if state == 0:
            if self.look_ahead in first["Declaration-list"] or self.look_ahead in follow["Declaration-list"]:
                node = Node("Declaration-list", parent_node)
                self.Declaration_list(node)
                state = 1
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                self.syn_err_l.append(error_msg)
                self.next_token()
                self.Program(parent_node, 0)

        if state == 1:
            if self.look_ahead == "$":
                node = Node('$', parent_node)
                self.code_generator.code_gen("jp_main")
                state = 2
            else:
                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                self.syn_err_l.append(error_msg)
                self.next_token()
                self.Program(parent_node, 0)

    def Declaration_list(self, parent_node, state=0):
        if state == 0:
            if self.look_ahead in first["Declaration"]:
                node = Node("Declaration", parent_node)
                self.Declaration(node)
                state = 1
            else:
                state = 2
                node = Node("epsilon", parent_node)

        if state == 1:
            if self.look_ahead in first["Declaration-list"] or self.look_ahead in follow["Declaration-list"]:
                node = Node("Declaration-list", parent_node)
                self.Declaration_list(node)
                state = 2
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                self.syn_err_l.append(error_msg)
                self.next_token()
                self.Declaration_list(parent_node, 1)

    def Declaration(self, parent_node, state=0):
        if state == 0:
            if self.look_ahead in first["Declaration-initial"]:
                node = Node("Declaration-initial", parent_node)
                self.Declaration_initial(node)
                state = 1
            else:
                if self.EOF_error():
                    exit()

                if self.look_ahead in follow["Declaration-initial"]:
                    error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + "Declaration-initial"
                    self.syn_err_l.append(error_msg)
                    state = 1
                else:
                    error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                    self.syn_err_l.append(error_msg)
                    self.next_token()
                    self.Declaration(parent_node, 0)

        if state == 1:
            if self.look_ahead in first["Declaration-prime"]:
                node = Node("Declaration-prime", parent_node)
                self.Declaration_prime(node)
                state = 2
            else:
                if self.EOF_error():
                    exit()

                if self.look_ahead in follow["Declaration-prime"]:
                    error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + "Declaration-prime"
                    self.syn_err_l.append(error_msg)
                    state = 2
                else:
                    error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                    self.syn_err_l.append(error_msg)
                    self.next_token()
                    self.Declaration(parent_node, 1)

    def Declaration_prime(self, parent_node, state=0):

        if self.look_ahead in first["Fun-declaration-prime"]:
            self.code_generator.code_gen("start_function")
            node = Node("Fun-declaration-prime", parent_node)
            self.Fun_declaration_prime(node)
        elif self.look_ahead in first["Var-declaration-prime"]:
            self.code_generator.code_gen(action_symbol="check_type", line_num=self.scanner.line_num)
            # TODO?
            node = Node("Var-declaration-prime", parent_node)
            self.Var_declaration_prime(node)
        else:
            if self.EOF_error():
                exit()

            if self.look_ahead in follow["Fun-declaration-prime"]:
                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + "Fun-declaration-prime"
                self.syn_err_l.append(error_msg)
                state = 1
            elif self.look_ahead in follow["Var-declaration-prime"]:
                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + "Var-declaration-prime"
                self.syn_err_l.append(error_msg)
                state = 1
            else:
                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                self.syn_err_l.append(error_msg)
                self.next_token()
                self.Declaration_prime(parent_node, 0)

    def Fun_declaration_prime(self, parent_node, state=0):
        if state == 0:
            if self.look_ahead == "(":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 1
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + "("
                self.syn_err_l.append(error_msg)
                state = 1

        if state == 1:
            if self.look_ahead in first["Params"]:
                node = Node("Params", parent_node)
                self.Params(node)
                self.code_generator.code_gen("define_function")
                state = 2
            else:
                if self.EOF_error():
                    exit()

                if self.look_ahead in follow["Params"]:
                    error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + "Params"
                    self.syn_err_l.append(error_msg)
                    state = 2
                else:
                    error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                    self.syn_err_l.append(error_msg)
                    self.next_token()
                    self.Fun_declaration_prime(parent_node, 1)

        if state == 2:
            if self.look_ahead == ")":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 3
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + ")"
                self.syn_err_l.append(error_msg)
                state = 3

        if state == 3:
            if self.look_ahead in first["Compound-stmt"]:
                node = Node("Compound-stmt", parent_node)
                self.Compound_stmt(node)
                self.code_generator.code_gen("end_function")
                state = 4
            else:
                if self.EOF_error():
                    exit()

                if self.look_ahead in follow["Compound-stmt"]:
                    error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + "Compound-stmt"
                    self.syn_err_l.append(error_msg)
                    state = 2
                else:
                    error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                    self.syn_err_l.append(error_msg)
                    self.next_token()
                    self.Fun_declaration_prime(parent_node, 3)

    def Params(self, parent_node, state=0):
        if state == 0:
            if self.look_ahead == "int":
                self.code_generator.code_gen("type", self.cpl_token[1])
                node = Node(self.token, parent_node)
                self.next_token()
                state = 1
            elif self.look_ahead == "void":
                self.code_generator.code_gen("type", self.cpl_token[1])
                node = Node(self.token, parent_node)
                self.next_token()
                state = 4
                self.code_generator.code_gen("pop")
                # TODO
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + "int"
                self.syn_err_l.append(error_msg)
                state = 1

        if state == 1:
            if self.look_ahead == "ID":
                self.code_generator.code_gen("define_id", self.cpl_token[1])
                node = Node(self.token, parent_node)
                self.next_token()
                state = 2
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + "ID"
                self.syn_err_l.append(error_msg)
                state = 2

        if state == 2:
            if self.look_ahead in first["Param-prime"] or self.look_ahead in follow["Param-prime"]:
                self.code_generator.code_gen("add_param")
                node = Node("Param-prime", parent_node)
                self.Param_prime(node)
                state = 3
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                self.syn_err_l.append(error_msg)
                self.next_token()
                self.Params(parent_node, 2)

        if state == 3:
            if self.look_ahead in first["Param-list"] or self.look_ahead in follow["Param-list"]:
                node = Node("Param-list", parent_node)
                self.Param_list(node)
                state = 4
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                self.syn_err_l.append(error_msg)
                self.next_token()
                self.Params(parent_node, 3)

    def Param_list(self, parent_node, state=0):

        if state == 0:
            if self.look_ahead == ",":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 1
            else:
                node = Node("epsilon", parent_node)
                state = 3

        if state == 1:
            if self.look_ahead in first["Param"]:
                node = Node("Param", parent_node)
                self.Param(node)
                self.code_generator.code_gen("add_param")
                state = 2
            else:
                if self.EOF_error():
                    exit()

                if self.look_ahead in follow["Param"]:
                    error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + "Param"
                    self.syn_err_l.append(error_msg)
                    state = 2
                else:
                    error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                    self.syn_err_l.append(error_msg)
                    self.next_token()
                    self.Param_list(parent_node, 1)

        if state == 2:
            if self.look_ahead in first["Param-list"] or self.look_ahead in follow["Param-list"]:
                node = Node("Param-list", parent_node)
                self.Param_list(node)
                state = 3
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                self.syn_err_l.append(error_msg)
                self.next_token()
                self.Param_list(parent_node, 2)

    def Param(self, parent_node, state=0):
        # state = 0
        if state == 0:
            if self.look_ahead in first["Declaration-initial"]:
                node = Node("Declaration-initial", parent_node)
                self.Declaration_initial(node)
                state = 1
            else:
                if self.EOF_error():
                    exit()

                if self.look_ahead in follow["Declaration-initial"]:
                    error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + "Declaration-initial"
                    self.syn_err_l.append(error_msg)
                    state = 1
                else:
                    error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                    self.syn_err_l.append(error_msg)
                    self.next_token()
                    self.Param(parent_node, 0)

        if state == 1:
            if self.look_ahead in first["Param-prime"] or self.look_ahead in follow["Param-prime"]:
                node = Node("Param-prime", parent_node)
                self.Param_prime(node)
                state = 2
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                self.syn_err_l.append(error_msg)
                self.next_token()
                self.Param(parent_node, 1)

    def Compound_stmt(self, parent_node, state=0):
        # state = 0
        if state == 0:
            if self.look_ahead == "{":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 1
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + "{"
                self.syn_err_l.append(error_msg)
                state = 1

        if state == 1:
            if self.look_ahead in first["Declaration-list"] or self.look_ahead in follow["Declaration-list"]:
                node = Node("Declaration-list", parent_node)
                self.Declaration_list(node)
                state = 2
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                self.syn_err_l.append(error_msg)
                self.next_token()
                self.Compound_stmt(parent_node, 1)

        if state == 2:
            if self.look_ahead in first["Statement-list"] or self.look_ahead in follow["Statement-list"]:
                node = Node("Statement-list", parent_node)
                self.Statement_list(node)
                state = 3
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                self.syn_err_l.append(error_msg)
                self.next_token()
                self.Compound_stmt(parent_node, 2)

        if state == 3:
            if self.look_ahead == "}":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 4
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + "}"
                self.syn_err_l.append(error_msg)
                state = 4

    def Statement_list(self, parent_node, state=0):
        # state = 0
        if state == 0:
            if self.look_ahead in first["Statement"]:
                node = Node("Statement", parent_node)
                self.Statement(node)
                state = 1
            else:
                node = Node("epsilon", parent_node)
                state = 2

        if state == 1:
            if self.look_ahead in first["Statement-list"] or self.look_ahead in follow["Statement-list"]:
                node = Node("Statement-list", parent_node)
                self.Statement_list(node)
                state = 3
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                self.syn_err_l.append(error_msg)
                self.next_token()
                self.Statement_list(parent_node, 1)

    def Statement(self, parent_node, state=0):
        # # state = 0
        # if state == 0:
        if self.look_ahead in first["Expression-stmt"]:
            node = Node("Expression-stmt", parent_node)
            self.Expression_stmt(node)
            state = 1
        elif self.look_ahead in first["Compound-stmt"]:
            node = Node("Compound-stmt", parent_node)
            self.Compound_stmt(node)
            state = 1
        elif self.look_ahead in first["Selection-stmt"]:
            node = Node("Selection-stmt", parent_node)
            self.Selection_stmt(node)
            state = 1
        elif self.look_ahead in first["Iteration-stmt"]:
            node = Node("Iteration-stmt", parent_node)
            self.Iteration_stmt(node)
            state = 1
        elif self.look_ahead in first["Return-stmt"]:
            node = Node("Return-stmt", parent_node)
            self.Return_stmt(node)
            state = 1
        else:
            if self.EOF_error():
                exit()

            if self.look_ahead in follow["Expression-stmt"]:
                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + "Expression-stmt"
                self.syn_err_l.append(error_msg)
                state = 1
            elif self.look_ahead in follow["Compound-stmt"]:
                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + "Compound-stmt"
                self.syn_err_l.append(error_msg)
                state = 1
            elif self.look_ahead in follow["Selection-stmt"]:
                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + "Selection-stmt"
                self.syn_err_l.append(error_msg)
                state = 1
            elif self.look_ahead in follow["Iteration-stmt"]:
                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + "Iteration-stmt"
                self.syn_err_l.append(error_msg)
                state = 1
            elif self.look_ahead in follow["Return-stmt"]:
                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + "Return-stmt"
                self.syn_err_l.append(error_msg)
                state = 1
            else:
                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                self.syn_err_l.append(error_msg)
                self.next_token()
                self.Statement(parent_node, 0)

    def Expression_stmt(self, parent_node, state=0):
        # state = 0
        if state == 0:
            if self.look_ahead in first["Expression"]:
                node = Node("Expression", parent_node)
                self.Expression(node)
                # bade : badesh
                self.code_generator.code_gen("pop")
                state = 1
            elif self.look_ahead == "break":
                node = Node(self.token, parent_node)
                self.code_generator.code_gen(action_symbol="break", line_num=self.scanner.line_num)
                self.next_token()
                state = 1
            elif self.look_ahead == ";":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 2

        if state == 1:
            if self.look_ahead == ";":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 2
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + ";"
                self.syn_err_l.append(error_msg)
                state = 2

    def Selection_stmt(self, parent_node, state=0):

        if state == 0:
            if self.look_ahead == "if":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 1
        if state == 1:
            if self.look_ahead == "(":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 2
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + "("
                self.syn_err_l.append(error_msg)
                state = 3
        if state == 2:
            if self.look_ahead in first["Expression"]:
                node = Node("Expression", parent_node)
                self.Expression(node)
                state = 3
            else:
                if self.EOF_error():
                    exit()

                if self.look_ahead in follow["Expression"]:
                    error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + "Expression"
                    self.syn_err_l.append(error_msg)
                    state = 3
                else:
                    error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                    self.syn_err_l.append(error_msg)
                    self.next_token()
                    self.Selection_stmt(parent_node, 2)

        if state == 3:
            if self.look_ahead == ")":
                node = Node(self.token, parent_node)
                self.code_generator.code_gen("save")
                self.next_token()
                state = 4
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + ")"
                self.syn_err_l.append(error_msg)
                state = 4

        if state == 4:
            if self.look_ahead in first["Statement"]:
                node = Node("Statement", parent_node)
                self.Statement(node)
                state = 5
            else:
                if self.EOF_error():
                    exit()

                if self.look_ahead in follow["Statement"]:
                    error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + "Statement"
                    self.syn_err_l.append(error_msg)
                    state = 5
                else:
                    error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                    self.syn_err_l.append(error_msg)
                    self.next_token()
                    self.Selection_stmt(parent_node, 4)

        if state == 5:
            if self.look_ahead in first["Else-stmt"]:
                node = Node("Else-stmt", parent_node)
                self.Else_stmt(node)
                state = 6
            else:
                if self.EOF_error():
                    exit()

                if self.look_ahead in follow["Else-stmt"]:
                    error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + "Else-stmt"
                    self.syn_err_l.append(error_msg)
                    state = 6
                else:
                    error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                    self.syn_err_l.append(error_msg)
                    self.next_token()
                    self.Selection_stmt(parent_node, 5)

    def Else_stmt(self, parent_node, state=0):

        if state == 0:
            if self.look_ahead == "endif":
                self.code_generator.code_gen("endif")
                node = Node(self.token, parent_node)
                self.next_token()
                state = 1
            elif self.look_ahead == "else":
                node = Node(self.token, parent_node)
                self.code_generator.code_gen("jpf")
                self.next_token()
                state = 2
        if state == 2:
            if self.look_ahead in first["Statement"]:
                node = Node("Statement", parent_node)
                self.Statement(node)
                self.code_generator.code_gen("jp")
                state = 3
            else:
                if self.EOF_error():
                    exit()

                if self.look_ahead in follow["Statement"]:
                    error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + "Statement"
                    self.syn_err_l.append(error_msg)
                    state = 3
                else:
                    error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                    self.syn_err_l.append(error_msg)
                    self.next_token()
                    self.Else_stmt(parent_node, 2)
        if state == 3:
            if self.look_ahead == "endif":
                # self.code_generator.code_gen("endif")
                node = Node(self.token, parent_node)
                self.next_token()
                state = 1
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(str(self.scanner.line_num)) + " : syntax error, missing " + "endif"
                self.syn_err_l.append(error_msg)
                state = 4

    def Iteration_stmt(self, parent_node, state=0):

        if state == 0:
            if self.look_ahead == "repeat":
                self.code_generator.code_gen("loop")
                node = Node(self.token, parent_node)
                self.code_generator.code_gen("label")
                self.next_token()
                state = 1
        if state == 1:
            if self.look_ahead in first["Statement"]:
                node = Node("Statement", parent_node)
                self.Statement(node)
                state = 2
            else:
                if self.EOF_error():
                    exit()

                if self.look_ahead in follow["Statement"]:
                    error_msg = "#" + str(str(self.scanner.line_num)) + " : syntax error, missing " + "Statement"
                    self.syn_err_l.append(error_msg)
                    state = 2
                else:
                    error_msg = "#" + str(str(self.scanner.line_num)) + " : syntax error, illegal " + self.look_ahead
                    self.syn_err_l.append(error_msg)
                    self.next_token()
                    self.Iteration_stmt(parent_node, 1)
        if state == 2:
            if self.look_ahead == "until":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 3
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(str(self.scanner.line_num)) + " : syntax error, missing " + "until"
                self.syn_err_l.append(error_msg)
                state = 3
        if state == 3:
            if self.look_ahead == "(":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 4
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(str(self.scanner.line_num)) + " : syntax error, missing " + "("
                self.syn_err_l.append(error_msg)
                state = 4
        if state == 4:
            if self.look_ahead in first["Expression"]:
                node = Node("Expression", parent_node)
                self.Expression(node)
                state = 5
            else:
                if self.EOF_error():
                    exit()

                if self.look_ahead in follow["Expression"]:
                    error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + "Expression"
                    self.syn_err_l.append(error_msg)
                    state = 5
                else:
                    error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                    self.syn_err_l.append(error_msg)
                    self.next_token()
                    self.Iteration_stmt(parent_node, 4)
        if state == 5:
            if self.look_ahead == ")":
                node = Node(self.token, parent_node)
                self.code_generator.code_gen("until")
                self.next_token()
                state = 6
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + ")"
                self.syn_err_l.append(error_msg)
                state = 6

    def Return_stmt(self, parent_node, state=0):
        # state = 0
        if state == 0:
            if self.look_ahead == "return":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 1
        if state == 1:
            if self.look_ahead in first["Return-stmt-prime"]:
                node = Node("Return-stmt-prime", parent_node)
                self.Return_stmt_prime(node)
                state = 2
            else:
                if self.EOF_error():
                    exit()

                if self.look_ahead in follow["Return-stmt-prime"]:
                    error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + "Return-stmt-prime"
                    self.syn_err_l.append(error_msg)
                    state = 2
                else:
                    error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                    self.syn_err_l.append(error_msg)
                    self.next_token()
                    self.Return_stmt(parent_node, 1)

    def Return_stmt_prime(self, parent_node, state=0):
        if state == 0:
            if self.look_ahead == ";":
                self.code_generator.code_gen("_return")
                node = Node(self.token, parent_node)
                self.next_token()
                state = 1
            elif self.look_ahead in first["Expression"]:
                node = Node("Expression", parent_node)
                self.Expression(node)
                self.code_generator.code_gen("return_value")
                state = 2

        if state == 2:
            if self.look_ahead == ";":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 1
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + ";"
                self.syn_err_l.append(error_msg)
                state = 1

    def Expression(self, parent_node, state=0):
        if state == 0:
            if self.look_ahead in first["Simple-expression-zegond"]:
                node = Node("Simple-expression-zegond", parent_node)
                self.Simple_expression_zegond(node)
                state = 1

            elif self.look_ahead == "ID":
                self.code_generator.code_gen("pid", self.cpl_token[1], self.scanner.line_num)
                node = Node(self.token, parent_node)
                self.next_token()
                state = 2

        if state == 2:
            if self.look_ahead in first["B"] or self.look_ahead in follow["B"]:
                node = Node("B", parent_node)
                self.B(node)
                state = 1
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                self.syn_err_l.append(error_msg)
                self.next_token()
                self.Expression(parent_node, 2)

    def B(self, parent_node, state=0):
        if state == 0:
            if self.look_ahead == "=":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 5
            elif self.look_ahead in first["Simple-expression-prime"] or self.look_ahead in follow[
                "Simple-expression-prime"]:
                node = Node("Simple-expression-prime", parent_node)
                self.Simple_expression_prime(node)
                state = 1
            elif self.look_ahead == "[":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 2

        if state == 2:
            if self.look_ahead in first["Expression"]:
                node = Node("Expression", parent_node)
                self.Expression(node)
                state = 3
            else:
                if self.EOF_error():
                    exit()

                if self.look_ahead in follow["Expression"]:
                    error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + "Expression"
                    self.syn_err_l.append(error_msg)
                    state = 3
                else:
                    error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                    self.syn_err_l.append(error_msg)
                    self.next_token()
                    self.B(parent_node, 2)

        if state == 3:
            if self.look_ahead == "]":
                node = Node(self.token, parent_node)
                self.code_generator.code_gen("address_array")
                self.next_token()
                state = 4
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + "]"
                self.syn_err_l.append(error_msg)
                state = 4

        if state == 4:
            if self.look_ahead in first["H"] or self.look_ahead in follow["H"]:
                node = Node("H", parent_node)
                self.H(node)
                state = 1
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                self.syn_err_l.append(error_msg)
                self.next_token()
                self.B(parent_node, 4)

        if state == 5:
            if self.look_ahead in first["Expression"]:
                node = Node("Expression", parent_node)
                self.Expression(node)
                self.code_generator.code_gen(action_symbol="assign", line_num=self.scanner.line_num)
                state = 1
            else:
                if self.EOF_error():
                    exit()

                if self.look_ahead in follow["Expression"]:
                    error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + "Expression"
                    self.syn_err_l.append(error_msg)
                    state = 1
                else:
                    error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                    self.syn_err_l.append(error_msg)
                    self.next_token()
                    self.B(parent_node, 5)

    def H(self, parent_node, state=0):

        if state == 0:
            if self.look_ahead == "=":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 4

            elif self.look_ahead in first["G"] or self.look_ahead in follow["G"]:
                node = Node("G", parent_node)
                self.G(node)
                state = 2
        if state == 2:
            if self.look_ahead in first["D"] or self.look_ahead in follow["D"]:
                node = Node("D", parent_node)
                self.D(node)
                state = 3
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                self.syn_err_l.append(error_msg)
                self.next_token()
                self.H(parent_node, 2)

        if state == 3:
            if self.look_ahead in first["C"] or self.look_ahead in follow["C"]:
                node = Node("C", parent_node)
                self.C(node)
                state = 1
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                self.syn_err_l.append(error_msg)
                self.next_token()
                self.H(parent_node, 3)

        if state == 4:
            if self.look_ahead in first["Expression"]:
                node = Node("Expression", parent_node)
                self.Expression(node)
                self.code_generator.code_gen(action_symbol="assign", line_num=self.scanner.line_num)
                state = 1
            else:
                if self.EOF_error():
                    exit()

                if self.look_ahead in follow["Expression"]:
                    error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + "Expression"
                    self.syn_err_l.append(error_msg)
                    state = 5
                else:
                    error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                    self.syn_err_l.append(error_msg)
                    self.next_token()
                    self.H(parent_node, 4)

    def Simple_expression_zegond(self, parent_node, state=0):
        if state == 0:
            if self.look_ahead in first["Additive-expression-zegond"]:
                node = Node("Additive-expression-zegond", parent_node)
                self.Additive_expression_zegond(node)
                state = 1
        if state == 1:
            if self.look_ahead in first["C"] or self.look_ahead in follow["C"]:
                node = Node("C", parent_node)
                self.C(node)
                state = 2
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                self.syn_err_l.append(error_msg)
                self.next_token()
                self.Simple_expression_zegond(parent_node, 1)

    def Simple_expression_prime(self, parent_node, state=0):
        if state == 0:
            if self.look_ahead in first["Additive-expression-prime"] or self.look_ahead in follow[
                "Additive-expression-prime"]:
                node = Node("Additive-expression-prime", parent_node)
                self.Additive_expression_prime(node)
                state = 1
        if state == 1:
            if self.look_ahead in first["C"] or self.look_ahead in follow["C"]:
                node = Node("C", parent_node)
                self.C(node)
                state = 2
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                self.syn_err_l.append(error_msg)
                self.next_token()
                self.Simple_expression_prime(parent_node, 1)

    def C(self, parent_node, state=0):
        if state == 0:
            if self.look_ahead in first["Relop"]:
                self.code_generator.code_gen('operator', self.cpl_token[1], self.scanner.line_num)  # az koja umad?
                node = Node("Relop", parent_node)
                self.Relop(node)
                state = 1
            else:
                node = Node("epsilon", parent_node)
                state = 2

        if state == 1:
            if self.look_ahead in first["Additive-expression"]:
                node = Node("Additive-expression", parent_node)
                self.Additive_expression(node)
                self.code_generator.code_gen(action_symbol="relop", line_num=self.scanner.line_num)
                state = 2
            else:
                if self.EOF_error():
                    exit()

                if self.look_ahead in follow["Additive-expression"]:
                    error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + "Additive-expression"
                    self.syn_err_l.append(error_msg)
                    state = 2
                else:
                    error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                    self.syn_err_l.append(error_msg)
                    self.next_token()
                    self.C(parent_node, 1)

    def Additive_expression(self, parent_node, state=0):
        if state == 0:
            if self.look_ahead in first["Term"]:
                node = Node("Term", parent_node)
                self.Term(node)
                state = 1

        if state == 1:
            if self.look_ahead in first["D"] or self.look_ahead in follow["D"]:
                node = Node("D", parent_node)
                self.D(node)
                state = 2
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                self.syn_err_l.append(error_msg)
                self.next_token()
                self.Additive_expression(parent_node, 1)

    def Additive_expression_prime(self, parent_node, state=0):
        if state == 0:
            if self.look_ahead in first["Term-prime"] or self.look_ahead in follow["Term-prime"]:
                node = Node("Term-prime", parent_node)
                self.Term_prime(node)
                state = 1

        if state == 1:
            if self.look_ahead in first["D"] or self.look_ahead in follow["D"]:
                node = Node("D", parent_node)
                self.D(node)
                state = 2
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                self.syn_err_l.append(error_msg)
                self.next_token()
                self.Additive_expression_prime(parent_node, 1)

    def Additive_expression_zegond(self, parent_node, state=0):
        if state == 0:
            if self.look_ahead in first["Term-zegond"]:
                node = Node("Term-zegond", parent_node)
                self.Term_zegond(node)
                state = 1

        if state == 1:
            if self.look_ahead in first["D"] or self.look_ahead in follow["D"]:
                node = Node("D", parent_node)
                self.D(node)
                state = 2
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                self.syn_err_l.append(error_msg)
                self.next_token()
                self.Additive_expression_zegond(parent_node, 1)

    def Term(self, parent_node, state=0):
        if state == 0:
            if self.look_ahead in first["Factor"]:
                node = Node("Factor", parent_node)
                self.Factor(node)
                state = 1

        if state == 1:
            if self.look_ahead in first["G"] or self.look_ahead in follow["G"]:
                node = Node("G", parent_node)
                self.G(node)
                state = 2
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                self.syn_err_l.append(error_msg)
                self.next_token()
                self.Term(parent_node, 1)

    def Term_prime(self, parent_node, state=0):
        if state == 0:
            if self.look_ahead in first["Factor-prime"] or self.look_ahead in follow["Factor-prime"]:
                node = Node("Factor-prime", parent_node)
                self.Factor_prime(node)
                state = 1

        if state == 1:
            if self.look_ahead in first["G"] or self.look_ahead in follow["G"]:
                node = Node("G", parent_node)
                self.G(node)
                state = 2
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                self.syn_err_l.append(error_msg)
                self.next_token()
                self.Term_prime(parent_node, 1)

    def Term_zegond(self, parent_node, state=0):
        if state == 0:
            if self.look_ahead in first["Factor-zegond"]:
                node = Node("Factor-zegond", parent_node)
                self.Factor_zegond(node)
                state = 1

        if state == 1:
            if self.look_ahead in first["G"] or self.look_ahead in follow["G"]:
                node = Node("G", parent_node)
                self.G(node)
                state = 2
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                self.syn_err_l.append(error_msg)
                self.next_token()
                self.Term_zegond(parent_node, 1)

    def G(self, parent_node, state=0):
        if state == 0:
            if self.look_ahead == "*":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 1
            # eps
            else:
                node = Node("epsilon", parent_node)
                state = 3
        if state == 1:
            if self.look_ahead in first["Factor"]:
                node = Node("Factor", parent_node)
                self.Factor(node)
                self.code_generator.code_gen(action_symbol="mult", line_num=self.scanner.line_num)
                state = 2
            else:
                if self.EOF_error():
                    exit()

                if self.look_ahead in follow["Factor"]:
                    error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + "Factor"
                    self.syn_err_l.append(error_msg)
                    state = 2
                else:
                    error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                    self.syn_err_l.append(error_msg)
                    self.next_token()
                    self.G(parent_node, 1)

        if state == 2:
            if self.look_ahead in first["G"] or self.look_ahead in follow["G"]:
                node = Node("G", parent_node)
                self.G(node)
                state = 3
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                self.syn_err_l.append(error_msg)
                self.next_token()
                self.G(parent_node, 2)

    def Factor(self, parent_node, state=0):

        if state == 0:
            if self.look_ahead == "(":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 1
            elif self.look_ahead == "NUM":
                self.code_generator.code_gen("pnum", self.cpl_token[1])
                node = Node(self.token, parent_node)
                self.next_token()
                state = 3
            elif self.look_ahead == "ID":
                self.code_generator.code_gen("pid", self.cpl_token[1], self.scanner.line_num)
                node = Node(self.token, parent_node)
                self.next_token()
                state = 4

        if state == 1:
            if self.look_ahead in first["Expression"]:
                node = Node("Expression", parent_node)
                self.Expression(node)
                state = 2
            else:
                if self.EOF_error():
                    exit()

                if self.look_ahead in follow["Expression"]:
                    error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + "Expression"
                    self.syn_err_l.append(error_msg)
                    state = 2
                else:
                    error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                    self.syn_err_l.append(error_msg)
                    self.next_token()
                    self.Factor(parent_node, 1)

        if state == 2:
            if self.look_ahead == ")":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 3
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + ")"
                self.syn_err_l.append(error_msg)
                state = 3

        if state == 4:
            if self.look_ahead in first["Var-call-prime"] or self.look_ahead in follow["Var-call-prime"]:
                node = Node("Var-call-prime", parent_node)
                self.Var_call_prime(node)
                state = 3
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                self.syn_err_l.append(error_msg)
                self.next_token()
                self.Factor(parent_node, 4)

    def Var_call_prime(self, parent_node, state=0):

        if state == 0:
            if self.look_ahead == "(":
                self.code_generator.code_gen("start_function_call", self.scanner.line_num)
                node = Node(self.token, parent_node)
                self.next_token()
                state = 1
            elif self.look_ahead in first["Var-prime"] or self.look_ahead in follow["Var-prime"]:
                node = Node("Var-prime", parent_node)
                self.Var_prime(node)
                state = 3

        if state == 1:
            if self.look_ahead in first["Args"] or self.look_ahead in follow["Args"]:
                node = Node("Args", parent_node)
                self.Args(node)
                state = 2
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                self.syn_err_l.append(error_msg)
                self.next_token()
                self.Var_call_prime(parent_node, 1)

        if state == 2:
            if self.look_ahead == ")":
                node = Node(self.token, parent_node)
                self.code_generator.code_gen(action_symbol="function_call", line_num=self.scanner.line_num)
                self.next_token()
                state = 3
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + ")"
                self.syn_err_l.append(error_msg)
                state = 3

    def Var_prime(self, parent_node, state=0):

        if state == 0:
            if self.look_ahead == "[":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 1
            else:
                state = 3
                node = Node("epsilon", parent_node)

        if state == 1:
            if self.look_ahead in first["Expression"]:
                node = Node("Expression", parent_node)
                self.Expression(node)
                state = 2
            else:
                if self.EOF_error():
                    exit()

                if self.look_ahead in follow["Expression"]:
                    error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + "Expression"
                    self.syn_err_l.append(error_msg)
                    state = 2
                else:
                    error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                    self.syn_err_l.append(error_msg)
                    self.next_token()
                    self.Var_prime(parent_node, 1)

        if state == 2:
            if self.look_ahead == "]":
                node = Node(self.token, parent_node)
                self.code_generator.code_gen("address_array")
                self.next_token()
                state = 3
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + "]"
                self.syn_err_l.append(error_msg)
                state = 3

    def Factor_prime(self, parent_node, state=0):
        if state == 0:
            if self.look_ahead == "(":
                self.code_generator.code_gen("start_function_call")
                node = Node(self.token, parent_node)
                self.next_token()
                state = 1
            else:
                state = 3
                node = Node("epsilon", parent_node)

        if state == 1:
            if self.look_ahead in first["Args"] or self.look_ahead in follow["Args"]:
                node = Node("Args", parent_node)
                self.Args(node)
                state = 2
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                self.syn_err_l.append(error_msg)
                self.next_token()
                self.Factor_prime(parent_node, 1)

        if state == 2:
            if self.look_ahead == ")":
                node = Node(self.token, parent_node)
                self.code_generator.code_gen(action_symbol="function_call", line_num=self.scanner.line_num)
                self.next_token()
                state = 3
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + ")"
                self.syn_err_l.append(error_msg)
                state = 3

    def Factor_zegond(self, parent_node, state=0):

        if state == 0:
            if self.look_ahead == "(":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 1
            elif self.look_ahead == "NUM":
                self.code_generator.code_gen("pnum", self.cpl_token[1])
                node = Node(self.token, parent_node)
                self.next_token()
                state = 3

        if state == 1:
            if self.look_ahead in first["Expression"]:
                node = Node("Expression", parent_node)
                self.Expression(node)
                state = 2
            else:
                if self.EOF_error():
                    exit()

                if self.look_ahead in follow["Expression"]:
                    error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + "Expression"
                    self.syn_err_l.append(error_msg)
                    state = 2
                else:
                    error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                    self.syn_err_l.append(error_msg)
                    self.next_token()
                    self.Factor_zegond(parent_node, 1)

        if state == 2:
            if self.look_ahead == ")":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 3
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + ")"
                self.syn_err_l.append(error_msg)
                state = 3

    def Args(self, parent_node, state=0):
        if state == 0:
            if self.look_ahead in first["Arg-list"]:
                node = Node("Arg-list", parent_node)
                self.Arg_list(node)
                state = 1
            else:
                state = 1
                node = Node("epsilon", parent_node)

    def Arg_list(self, parent_node, state=0):
        if state == 0:
            if self.look_ahead in first["Expression"]:
                node = Node("Expression", parent_node)
                self.Expression(node)
                state = 1
        if state == 1:
            if self.look_ahead in first["Arg-list-prime"] or self.look_ahead in follow["Arg-list-prime"]:
                node = Node("Arg-list-prime", parent_node)
                self.Arg_list_prime(node)
                state = 2
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                self.syn_err_l.append(error_msg)
                self.next_token()
                self.Arg_list(parent_node, 1)

    def Arg_list_prime(self, parent_node, state=0):
        # state = 0
        if state == 0:
            if self.look_ahead == ",":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 1
            # eps
            else:
                state = 3
                node = Node("epsilon", parent_node)

        if state == 1:
            if self.look_ahead in first["Expression"]:
                node = Node("Expression", parent_node)
                self.Expression(node)
                state = 2
            else:
                if self.EOF_error():
                    exit()

                if self.look_ahead in follow["Expression"]:
                    error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + "Expression"
                    self.syn_err_l.append(error_msg)
                    state = 2
                else:
                    error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                    self.syn_err_l.append(error_msg)
                    self.next_token()
                    self.Arg_list_prime(parent_node, 1)

        if state == 2:
            if self.look_ahead in first["Arg-list-prime"] or self.look_ahead in follow["Arg-list-prime"]:
                node = Node("Arg-list-prime", parent_node)
                self.Arg_list_prime(node)
                state = 3
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                self.syn_err_l.append(error_msg)
                self.next_token()
                self.Arg_list_prime(parent_node, 2)

    def D(self, parent_node, state=0):

        if state == 0:
            if self.look_ahead in first['Addop']:
                self.code_generator.code_gen('operator', self.cpl_token[1])
                node = Node('Addop', parent_node)
                self.Addop(node)
                state = 1
            else:
                state = 3
                node = Node("epsilon", parent_node)

        if state == 1:

            if self.look_ahead in first['Term']:
                node = Node('Term', parent_node)
                self.Term(node)
                self.code_generator.code_gen(action_symbol="add_or_sub", line_num=self.scanner.line_num)
                state = 2
            else:
                if self.EOF_error():
                    exit()

                if self.look_ahead in follow["Term"]:
                    error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + "Term"
                    self.syn_err_l.append(error_msg)
                    state = 2
                else:
                    error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                    self.syn_err_l.append(error_msg)
                    self.next_token()
                    self.D(parent_node, 1)

        if state == 2:
            if self.look_ahead in first['D'] or self.look_ahead in follow["D"]:
                node = Node('D', parent_node)
                self.D(node)
                state = 3
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, illegal " + self.look_ahead
                self.syn_err_l.append(error_msg)
                self.next_token()
                self.D(parent_node, 2)

    def Declaration_initial(self, parent_node, state=0):

        if state == 0:
            self.code_generator.code_gen("type", self.cpl_token[1])
            if self.look_ahead in first['Type-specifier']:
                node = Node('Type-specifier', parent_node)
                self.Type_specifier(node)
                state = 1

        if state == 1:

            self.code_generator.code_gen("define_id", self.cpl_token[1])

            if self.look_ahead == 'ID':
                node = Node(self.token, parent_node)
                self.next_token()
                state = 2
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + "ID"
                self.syn_err_l.append(error_msg)
                state = 2

    def Param_prime(self, parent_node, state=0):

        if state == 0:
            if self.look_ahead == '[':
                node = Node(self.token, parent_node)
                self.next_token()
                state = 1
            # eps
            else:
                state = 2
                node = Node("epsilon", parent_node)

        if state == 1:
            if self.look_ahead == ']':
                node = Node(self.token, parent_node)
                self.code_generator.code_gen("array_input")
                self.next_token()
                state = 2
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + "]"
                self.syn_err_l.append(error_msg)
                state = 2

    def Var_declaration_prime(self, parent_node, state=0):
        if state == 0:

            if self.look_ahead == ';':
                self.code_generator.code_gen(action_symbol='check_type', line_num=self.scanner.line_num)
                node = Node(self.token, parent_node)
                self.next_token()
                self.code_generator.code_gen("pop")
                state = 1
            elif self.look_ahead == '[':
                self.code_generator.code_gen(action_symbol='check_type', line_num=self.scanner.line_num)
                node = Node(self.token, parent_node)
                self.next_token()
                state = 2
        if state == 2:
            if self.look_ahead == 'NUM':
                self.code_generator.code_gen("pnum", self.cpl_token[1])
                node = Node(self.token, parent_node)
                self.next_token()
                state = 3
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + "NUM"
                self.syn_err_l.append(error_msg)
                state = 3

        if state == 3:
            if self.look_ahead == ']':
                node = Node(self.token, parent_node)
                self.code_generator.code_gen("save_array")
                self.next_token()
                state = 4
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + "]"
                self.syn_err_l.append(error_msg)
                state = 4

        if state == 4:
            if self.look_ahead == ';':
                node = Node(self.token, parent_node)
                self.next_token()
                state = 1
            else:
                if self.EOF_error():
                    exit()

                error_msg = "#" + str(self.scanner.line_num) + " : syntax error, missing " + ";"
                self.syn_err_l.append(error_msg)
                state = 5

    def Type_specifier(self, parent_node, state=0):
        if self.look_ahead == 'int' or self.look_ahead == 'void':
            node = Node(self.token, parent_node)
            self.next_token()

    def Relop(self, parent_node, state=0):

        if self.look_ahead == '<' or self.look_ahead == '==':
            node = Node(self.token, parent_node)
            self.next_token()

    def Addop(self, parent_node, state=0):

        if self.look_ahead == '-' or self.look_ahead == '+':
            node = Node(self.token, parent_node)
            self.next_token()
