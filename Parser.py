from scanner import Scanner
from First import first
from Follow import follow
from Predict_set import predict_set
from anytree import Node, RenderTree


class Parser:

    illigal_error = 'illegal lookahead on line N'
    missing_error = 'missing Statement on line N'
    syn_err_l = []


    def __init__(self, input):
        self.scanner = Scanner('./input.txt')
        self.look_ahead=""
        self.state = 0
        self.root = Node("Program")
        self.next_token()

    def next_token(self):
        self.cpl_token = self.scanner.get_next_token()

        if not self.cpl_token==None:
            if self.cpl_token[0]=='NUM' or self.cpl_token[0]=='ID':
                self.look_ahead=self.cpl_token[0]
            elif self.cpl_token == '$':
                self.look_ahead = '$'
            else:
                self.look_ahead = self.cpl_token[1]



    def pars(self):


        return



    def Program(self):
        return

    def D(self,parent_node):
        if self.look_ahead in first['Addop']:
            node=Node('Addop',parent_node)
            self.Addop(node)

            if self.look_ahead in first['Term']:
                node = Node('Term', parent_node)
                self.Term(node)

                if self.look_ahead in first['D']:
                    node = Node('D', parent_node)
                    self.D(node)

        elif self.look_ahead=="epsilon":
            print("waht to do")
            #TODO
        else:
            print('error')


    def Declaration_initial(self,parent_node):

        if self.look_ahead in first['Type-specifier']:
            node=Node('Type-specifier',parent_node)
            self.Type_specifier(node)

            if self.look_ahead=='ID':
                node = Node(self.look_ahead, parent_node)



    def Param_prime(self,parent_node):
        if self.look_ahead=='[':
            node=Node(self.look_ahead,parent_node)
            self.next_token()
            if self.look_ahead==']':
                node = Node(self.look_ahead, parent_node)
            else:
                print("error")
        elif self.look_ahead=='epsilon':
            print("what to do")
            #TODO epsilon
        else:
            print("erro")

    def Var_declaration_prime(self,parent_node):
        if self.look_ahead==';':
            node=Node(self.look_ahead,parent_node)
        elif self.look_ahead=='[':
            node=Node(self.look_ahead,parent_node)
            self.next_token()
            if self.look_ahead=='NUM':
                node = Node(self.look_ahead, parent_node)
                self.next_token()
                if self.look_ahead==']':
                    node = Node(self.look_ahead, parent_node)
                    self.next_token()
                    if self.look_ahead==';':
                        node = Node(self.look_ahead, parent_node)
                    else:
                        print("error")
                else:
                    print("error")
            else:
                print("error")

        else:
            print("error")


    def Type_specifier(self,parent_node):
        if self.look_ahead=='int' or self.look_ahead=='void':
            node=Node(self.look_ahead,parent_node)
        else:
            print("error")


    def Relop(self,parent_node):
        if self.look_ahead=='<' or self.look_ahead=='==':
            node=Node(self.look_ahead,parent_node)
        else:
            print("error")

    def Addop(self,parent_node):

        if self.look_ahead=='-' or self.look_ahead=='+':
            node=Node(self.look_ahead,parent_node)
        else:
            print("error")
