from scanner import Scanner
from Package1.First import first
from Package1.Follow import follow
from anytree import Node


class parser:

    #illigal_error = 'illegal lookahead on line N'
    #missing_error = 'missing Statement on line N'

    syn_err_l = []

    def __init__(self):
        self.scanner = Scanner('./input.txt')
        self.look_ahead = ""
        self.state = 0
        self.root = Node("Program")
        self.next_token()
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




    ###################################################################3

    def Program(self, parent_node):

        state = 0

        if state == 0:
            if self.look_ahead in first["Declaration-list"] or self.look_ahead in follow["Declaration-list"]:
                node = Node("Declaration-list", parent_node)
                self.Declaration_list(node)
                state =1
            # eps

        if state == 1:
            if self.look_ahead == "$":
                node = Node('$', parent_node)
                state = 2

    def Declaration_list(self, parent_node):
        state = 0

        if state == 0:
            if self.look_ahead in first["Declaration"]:
                node = Node("Declaration", parent_node)
                self.Declaration(node)
                state = 1
            # eps
            else:
                state = 2
                node = Node("epsilon", parent_node)

        if state == 1:
            if self.look_ahead in first["Declaration-list"] or self.look_ahead in follow["Declaration-list"]:
                node = Node("Declaration-list", parent_node)
                self.Declaration_list(node)
                state = 2


    def Declaration(self, parent_node):
        state = 0
        if state == 0:
            if self.look_ahead in first["Declaration-initial"]:
                node = Node("Declaration-initial", parent_node)
                self.Declaration_initial(node)
                state = 1

        if state == 1:
            if self.look_ahead in first["Declaration-prime"]:
                node = Node("Declaration-prime", parent_node)
                self.Declaration_prime(node)
                state = 2

    def Declaration_prime(self, parent_node):
        # state =0

        if self.look_ahead in first["Fun-declaration-prime"]:
            node = Node("Fun-declaration-prime", parent_node)
            self.Fun_declaration_prime(node)
        elif self.look_ahead in first["Var-declaration-prime"]:
            node = Node("Var-declaration-prime", parent_node)
            self.Var_declaration_prime(node)

    def Fun_declaration_prime(self, parent_node):
        state = 0
        if state == 0:
            if self.look_ahead == "(":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 1

        if state == 1:
            if self.look_ahead in first["Params"]:
                node = Node("Params", parent_node)
                self.Params(node)
                state = 2

        if state == 2:
            if self.look_ahead == ")":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 3

        if state == 3:
            if self.look_ahead in first["Compound-stmt"]:
                node = Node("Compound-stmt", parent_node)
                self.Compound_stmt(node)
                state = 4

    def Params(self, parent_node):
        state = 0
        if state == 0:
            if self.look_ahead == "int":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 1
            elif self.look_ahead == "void":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 4

        if state == 1:
            if self.look_ahead == "ID":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 2

        if state == 2:
            if self.look_ahead in first["Param-prime"] or self.look_ahead in follow["Param-prime"]:
                node = Node("Param-prime", parent_node)
                self.Param_prime(node)
                state = 3

        if state == 3:
            if self.look_ahead in first["Param-list"] or self.look_ahead in follow["Param-list"]:
                node = Node("Param-list", parent_node)
                self.Param_prime(node)
                state = 4


    def Param_list(self, parent_node):

        state = 0
        if state == 0:
            if self.look_ahead == ",":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 1
            # else epsil
            else:
                node = Node("epsilon", parent_node)
                state = 3

        if state == 1:
            if self.look_ahead in first["Param"]:
                node = Node("Param", parent_node)
                self.Param(node)
                state = 2

        if state == 2:
            if self.look_ahead in first["Param-list"] or self.look_ahead in follow["Param-list"]:
                node = Node("Param-list", parent_node)
                self.Param_list(node)
                state = 3


    def Param(self, parent_node):
        state = 0
        if state == 0:
            if self.look_ahead in first["Declaration-initial"]:
                node = Node("Declaration-initial", parent_node)
                self.Param_list(node)
                state = 1

        if state == 1:
            if self.look_ahead in first["Param-prime"] or self.look_ahead in follow["Param-prime"]:
                node = Node("Param-prime", parent_node)
                self.Param_list(node)
                state = 2


    def Compound_stmt(self, parent_node):
        state = 0
        if state == 0:
            if self.look_ahead == "{":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 1

        if state == 1:
            if self.look_ahead in first["Declaration-list"] or self.look_ahead in follow["Declaration-list"]:
                node = Node("Declaration-list", parent_node)
                self.Declaration_list(node)
                state = 2

        if state == 2:
            if self.look_ahead in first["Statement-list"] or self.look_ahead in follow["Statement-list"]:
                node = Node("Statement-list", parent_node)
                self.Statement_list(node)
                state = 3


        if state == 3:
            if self.look_ahead == "}":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 4

    def Statement_list(self, parent_node):
        state = 0
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


    def Statement(self, parent_node):
        # state = 0
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

    def Expression_stmt(self, parent_node):
        state = 0
        if state == 0:
            if self.look_ahead in first["Expression"]:
                node = Node("Expression", parent_node)
                self.Expression(node)
                state = 1
            elif self.look_ahead == "break":
                node = Node(self.token, parent_node)
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

    def Selection_stmt(self, parent_node):
        state = 0
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
        if state == 2:
            if self.look_ahead in first["Expression"]:
                node = Node("Expression", parent_node)
                self.Expression(node)
                state = 3

        if state == 3:
            if self.look_ahead == ")":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 4
        if state == 4:
            if self.look_ahead in first["Statement"]:
                node = Node("Statement", parent_node)
                self.Statement(node)
                state = 5
        if state == 5:
            if self.look_ahead in first["Else-stmt"]:
                node = Node("Else-stmt", parent_node)
                self.Else_stmt(node)
                state = 6

    def Else_stmt(self, parent_node):
        state = 0
        if state == 0:
            if self.look_ahead == "endif":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 1
            elif self.look_ahead == "else":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 2
        if state == 2:
            if self.look_ahead in first["Statement"]:
                node = Node("Statement", parent_node)
                self.Statement(node)
                state = 3
        if state == 3:
            if self.look_ahead == "endif":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 1

    def Iteration_stmt(self, parent_node):

        state = 0
        if state == 0:
            if self.look_ahead == "repeat":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 1
        if state == 1:
            if self.look_ahead in first["Statement"]:
                node = Node("Statement", parent_node)
                self.Statement(node)
                state = 2
        if state == 2:
            if self.look_ahead == "until":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 3
        if state == 3:
            if self.look_ahead == "(":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 4
        if state == 4:
            if self.look_ahead in first["Expression"]:
                node = Node("Expression", parent_node)
                self.Expression(node)
                state = 5

        if state == 5:
            if self.look_ahead == ")":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 6

    def Return_stmt(self, parent_node):
        state = 0
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

    def Return_stmt_prime(self, parent_node):
        state = 0
        if state == 0:
            if self.look_ahead == ";":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 1
            elif self.look_ahead in first["Expression"]:
                node = Node("Expression", parent_node)
                self.Expression(node)
                state = 2

        if state == 2:
            if self.look_ahead == ";":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 1

    def Expression(self, parent_node):
        state = 0
        if state == 0:
            if self.look_ahead in first["Simple-expression-zegond"]:
                node = Node("Simple-expression-zegond", parent_node)
                self.Simple_expression_zegond(node)
                state = 1

            elif self.look_ahead == "ID":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 2

        if state == 2:
            if self.look_ahead in first["B"] or self.look_ahead in follow["B"]:
                node = Node("B", parent_node)
                self.B(node)
                state = 1


    def B(self, parent_node):
        state = 0
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
        if state == 3:
            if self.look_ahead == "]":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 4
        if state == 4:
            if self.look_ahead in first["H"] or self.look_ahead in follow["H"]:
                node = Node("H", parent_node)
                self.H(node)
                state = 1

        if state == 5:
            #print("expresisin ", self.look_ahead , self.scanner.line_num , self.token)
            if self.look_ahead in first["Expression"]:
                node = Node("Expression", parent_node)
                #print("node added")
                self.Expression(node)
                state = 1

    def H(self, parent_node):
        state = 0
        if state == 0:
            if state == 3:
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

        if state == 3:
            if self.look_ahead in first["C"] or self.look_ahead in follow["C"]:
                node = Node("C", parent_node)
                self.C(node)
                state = 1
        if state == 4:
            if self.look_ahead in first["Expression"]:
                node = Node("Expression", parent_node)
                self.Expression(node)
                state = 1

    def Simple_expression_zegond(self, parent_node):
        state = 0
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

    def Simple_expression_prime(self, parent_node):
        state = 0
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

    def C(self, parent_node):
        state = 0
        if state == 0:
            if self.look_ahead in first["Relop"]:
                node = Node("Relop", parent_node)
                self.Relop(node)
                state = 1
            else:
                node = Node("epsilon", parent_node)
                state = 2
            # elif epsilon

        if state == 1:
            if self.look_ahead in first["Additive-expression"]:
                node = Node("Additive-expression", parent_node)
                self.Additive_expression(node)
                state = 2

    def Additive_expression(self, parent_node):
        state = 0
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

    def Additive_expression_prime(self, parent_node):
        state = 0
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

    def Additive_expression_zegond(self, parent_node):
        state = 0
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

    def Term(self, parent_node):
        state = 0
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

    def Term_prime(self, parent_node):
        state = 0
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

    def Term_zegond(self, parent_node):
        state = 0
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

    def G(self, parent_node):
        state = 0
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
                state = 2
        if state == 2:
            if self.look_ahead in first["G"] or self.look_ahead in follow["G"]:
                node = Node("G", parent_node)
                self.G(node)
                state = 3

    def Factor(self, parent_node):
        state = 0
        if state == 0:
            if self.look_ahead == "(":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 1
            elif self.look_ahead == "NUM":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 3
            elif self.look_ahead == "ID":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 4

        if state == 1:
            if self.look_ahead in first["Expression"]:
                node = Node("Expression", parent_node)
                self.Expression(node)
                state = 2
        if state == 2:
            if self.look_ahead == ")":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 3
        if state == 4:
            if self.look_ahead in first["Var-call-prime"] or self.look_ahead in follow["Var-call-prime"]:
                node = Node("Var-call-prime", parent_node)
                self.Var_call_prime(node)
                state = 3

    def Var_call_prime(self, parent_node):
        state = 0
        if state == 0:
            if self.look_ahead == "(":
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
        if state == 2:
            if self.look_ahead == ")":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 3

    def Var_prime(self, parent_node):
        state = 0
        if state == 0:
            if self.look_ahead == "[":
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
        if state == 2:
            if self.look_ahead == "]":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 3

    def Factor_prime(self, parent_node):
        state = 0
        if state == 0:
            if self.look_ahead == "(":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 1
            # eps
            else:
                state=3
                node = Node("epsilon", parent_node)


        if state == 1:
            if self.look_ahead in first["Args"] or self.look_ahead in follow["Args"]:
                node = Node("Args", parent_node)
                self.Args(node)
                state = 2
        if state == 2:
            if self.look_ahead == ")":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 3

    def Factor_zegond(self, parent_node):
        state = 0
        if state == 0:
            if self.look_ahead == "(":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 1
            elif self.look_ahead == "NUM":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 3

        if state == 1:
            if self.look_ahead in first["Expression"]:
                node = Node("Expression", parent_node)
                self.Expression(node)
                state = 2
        if state == 2:
            if self.look_ahead == ")":
                node = Node(self.token, parent_node)
                self.next_token()
                state = 3

    def Args(self, parent_node):
        state = 0
        if state == 0:
            if self.look_ahead in first["Arg-list"]:
                node = Node("Arg-list", parent_node)
                self.Arg_list(node)
                state = 1
            else:
                state = 1
                node = Node("epsilon", parent_node)

            # 3ps

    def Arg_list(self, parent_node):
        state = 0
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

    def Arg_list_prime(self, parent_node):
        state = 0
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

        if state == 2:
            if self.look_ahead in first["Arg-list-prime"] or self.look_ahead in follow["Arg-list-prime"]:
                node = Node("Arg-list-prime", parent_node)
                self.Arg_list_prime(node)
                state = 3

    def D(self, parent_node):

        state = 0
        if state == 0:
            if self.look_ahead in first['Addop']:
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
                state = 2
        if state == 2:
            if self.look_ahead in first['D'] or self.look_ahead in follow["D"]:
                node = Node('D', parent_node)
                self.D(node)
                state = 3

    def Declaration_initial(self, parent_node):

        state = 0
        if state == 0:
            if self.look_ahead in first['Type-specifier']:
                node = Node('Type-specifier', parent_node)
                self.Type_specifier(node)
                state = 1

        if state == 1:
            if self.look_ahead == 'ID':
                node = Node(self.token, parent_node)
                self.next_token()
                state = 2

    def Param_prime(self, parent_node):

        state = 0
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
                self.next_token()
                state = 2

    def Var_declaration_prime(self, parent_node):
        state = 0
        if state == 0:

            if self.look_ahead == ';':
                node = Node(self.token, parent_node)
                self.next_token()
                state = 1
            elif self.look_ahead == '[':
                node = Node(self.token, parent_node)
                self.next_token()
                state = 2
        if state == 2:
            if self.look_ahead == 'NUM':
                node = Node(self.token, parent_node)
                self.next_token()
                state = 3
        if state == 3:
            if self.look_ahead == ']':
                node = Node(self.token, parent_node)
                self.next_token()
                state = 4
        if state == 4:
            if self.look_ahead == ';':
                node = Node(self.token, parent_node)
                self.next_token()
                state = 1

    def Type_specifier(self, parent_node):
        # state = 0
        # if state == 0:
        if self.look_ahead == 'int' or self.look_ahead == 'void':
            node = Node(self.token, parent_node)
            self.next_token()

    def Relop(self, parent_node):
        # state = 0
        # if state == 0:
        if self.look_ahead == '<' or self.look_ahead == '==':
            node = Node(self.token, parent_node)
            self.next_token()

    def Addop(self, parent_node):
        # state = 0
        # if state == 0:

        if self.look_ahead == '-' or self.look_ahead == '+':
            node = Node(self.token, parent_node)
            self.next_token()
