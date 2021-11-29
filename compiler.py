# saeede vahedi 96102664
# sabrineh mokhtari 96110107

from parser import parser
from anytree import RenderTree

parser = parser()

# for pre, fill, node in RenderTree(parser.root):
#     print("%s%s" % (pre, node.name))

flag = False

with open("parse_tree.txt", 'w', encoding='utf-8') as file:  # parse_tree file
    for pre, _, node in RenderTree(parser.root):
        if flag:
            file.write("\n%s%s" % (pre, node.name))
        else:
            file.write("%s%s" % (pre, node.name))
            flag=True



# with open("parse_tree.txt", 'rb+') as file:
#     file.seek(-1, os.SEEK_END)
#     file.truncate()


with open("syntax_errors.txt", "w") as file:  # syntax errors file
    if len(parser.syn_err_l) == 0:
        file.write("There is no syntax error.")
    else:
        for l in parser.syn_err_l:
            file.write(l + "\n")
