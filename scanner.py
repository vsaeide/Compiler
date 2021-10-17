# saeede vahedi 96102664
# sabrineh mokhtari



class Scanner:

    keyword = ['if', 'else', 'void', 'int', 'repeat', 'break', 'until', 'return']
    # == symbol?
    symbol = [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-','<', '=', '*', '==']
    whitespace = [' ', '\n', '\r', '\t', '\v', '\f']
    error_types=['Invalid input','Unmatched comment' ,'Unclosed comment','Invalid number']
    symbol_table=[]
    tokens=""
    state ='0'


    def __init__(self, input):

        self.line_num = 1
        self.token = []
        self.lex_error = []
        self.program = open(input, 'r').read()+"\n"
        #self.comment_start_line=None
        self.token_start_loc=0
        self.curr_loc =0
        self.file_cap = len(self.program)

        for word in self.keyword:
            self.symbol_table.append(word)





    def get_next_token(self):

        while(self.curr_loc<self.file_cap):

            result=None # the token pair = ( token type , token string)
            
            if self.state == '0': # we have to recognize new token
                self.token_start_loc = self.curr_loc

            self.dfa_navigation(self.program[self.curr_loc])

            token = self.Ignore_whitespace(self.program[self.token_start_loc:self.curr_loc])

            if self.state == '2':

                if token in self.keyword:
                    result= ("KEYWORD", token )
                else:
                    result=("ID", token)

                if token not in self.symbol_table:
                    self.symbol_table.append(token)

                self.state = '0'

            elif self.state == '4':
                result = ("NUM", token)
                self.state = '0'

            elif self.state == '5' or self.state == '7':
                result = ("SYMBOL", self.program[self.token_start_loc:self.curr_loc + 1])
                self.state = '0'
                self.curr_loc += 1

            elif self.state == '9':
                result = ("SYMBOL", token)
                self.state = '0'
                self.curr_loc += 1

            elif self.state == 'c':
                self.state = '0'
                self.curr_loc += 1

            elif self.state == 'f':
                self.state = '0'
                self.curr_loc += 1

            elif self.state in self.error_types:
                if self.state == 'Unclosed comment':
                    self.lex_error.append(
                        [self.comment_start_line, self.program[self.token_start_loc:self.curr_loc + 1][0:7] + "...", self.state])
                else:
                    self.lex_error.append([self.line_num, self.program[self.token_start_loc:self.curr_loc + 1], self.state])
                self.state = '0'
                self.curr_loc += 1
            else:
                self.curr_loc += 1

            if self.program[self.curr_loc-1] == '\n':
                self.line_num += 1

            if not result==None:
                return result
            
            
            
    # functions

    def is_valid_char(self, chr):

        if self.is_digit(chr) or self.is_letter(chr) or self.is_whitespace(chr) or self.is_symbol(
                chr) or self.is_comment(chr):
            return True
        return False

    def is_symbol(self, chr):
        if chr in self.symbol:
            return True

    def is_whitespace(self, chr):
        if chr in self.whitespace:
            return True

    def is_digit(self, chr):
        if '0' <= chr <= '9':
            return True

    def is_letter(self, chr):
        if 'a' <= chr <= 'z' or 'A' <= chr <= 'Z':
            return True

    def is_comment(self, chr):
        if chr == '/':
            return True

    def Ignore_whitespace(self, input):  # for skipping white spaces

        for whitespace in self.whitespace[1:]:
            input = input.replace(whitespace, '')
        return input
    

    def dfa_navigation(self, chr):

        if self.state == '0':  # write if for every state after start, based on DFA
            if self.is_digit(chr):
                self.state = '3'
            elif self.is_letter(chr):
                self.state = '1'
            elif self.is_comment(chr):
                self.state = 'a'
            elif self.is_symbol(chr):
                if chr == "=":
                    self.state = '6'
                elif chr == '*':
                    self.state = '8'
                else:
                    self.state = '5'
            elif self.is_whitespace(chr):
                self.state = 'f'
            else:
                self.state = 'Invalid input'

        elif self.state == '1':

            if not (self.is_digit(chr) or self.is_letter(chr)):
                if not self.is_valid_char(chr):
                    self.state = 'Invalid input'
                else:
                    self.state = '2'
        elif self.state == '3':
            if self.is_letter(chr):
                self.state = 'Invalid number'
            if not (self.is_digit(chr) or self.is_letter(chr)):
                self.state = '4'
        elif self.state == '6':
            if chr == "=":
                self.state = '7'
            elif self.is_valid_char(chr):
                self.state = '9'
            else:
                self.state='Invalid input'

        elif self.state == '8':
            if not chr == '/':
                if self.is_valid_char(chr):
                    self.state = '9'
                else:
                    self.state = 'Invalid input'
            else:
                self.state = "Unmatched comment"

        elif self.state == 'a':
            if chr == "/":
                self.state = 'b'
                self.comment_start_line = self.line_num
            elif chr == "*":
                self.comment_start_line = self.line_num
                self.state = 'd'
            else:
                self.state = 'Invalid input'
        elif self.state == 'b':
            if chr == "\n":
                self.state = 'c'
        elif self.state == 'd':
            if chr == "*":
                self.state = 'e'
            elif self.curr_loc == self.file_cap - 1:
                self.state = 'Unclosed comment'
        elif self.state == 'e':
            if chr == "/":
                self.state = 'c'
            elif not chr == "*":
                self.state = 'd'


    def scan(self):

        temp_last_line=0
        while (self.curr_loc < self.file_cap):

            line_before_call_func=self.line_num
            next_token=self.get_next_token()


            if not next_token==None:
                temp_tokens = " "+str(next_token)
                if not self.line_num==temp_last_line:
                    self.tokens += "\n"+str(self.line_num) + ".\t" + temp_tokens.replace("'","")[1:]
                else:
                    self.tokens+=temp_tokens.replace("'","")
                temp_last_line=self.line_num


        # create files
        f1 = open("tokens.txt", "w")
        f1.write(self.tokens[1:])
        f1.close()
        #
        error_string=""
        last_line=0
        if len(self.lex_error):
            for error in self.lex_error:
                error[1]=self.Ignore_whitespace(error[1])
                if not error[0]==last_line:
                    if not last_line==0:
                        error_string+="\n"
                    error_string+=str(error[0])+".\t("+ error[1]+", "+error[2]+")"
                    last_line=error[0]
                else:
                    error_string+=" ("+ error[1]+", "+error[2]+")"


        else:
            error_string="There is no lexical error."
        f2 = open("lexical_errors.txt", "w")
        f2.write(error_string)
        f2.close()
        #
        table=""
        f3 = open("symbol_table.txt", "w")
        counter=1
        for symbol in self.symbol_table:
            table+=str(counter)+".\t"+symbol+"\n"
            counter+=1
        f3.write(table[:-1])
        f3.close()





