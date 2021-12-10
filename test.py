# reading files
f1 = open("./parse_tree.txt", "r")
f2 = open("./parse_tree_or.txt", "r")

i = 0

for line1 in f1:
    i += 1

    for line2 in f2:

        # matching line1 from both files
        if line1 == line2:
            # print IDENTICAL if similar
            print("Line ", i, ": IDENTICAL")
        else:
            print("Line ", i, ":")
            # else print that line from both files
            print("\tFile 1:", line1, end='')
            print("\tFile 2:", line2, end='')
        break

# closing files
f1.close()
f2.close()

# f1 = open("./syntax_errors.txt", "r")
# f2 = open("./syntax_errors_or.txt", "r")
#
# i = 0
#
# for line1 in f1:
#     i += 1
#
#     for line2 in f2:
#
#         # matching line1 from both files
#         if line1 == line2:
#             # print IDENTICAL if similar
#             print("Line ", i, ": IDENTICAL")
#         else:
#             print("Line ", i, ":")
#             # else print that line from both files
#             print("\tFile 1:", line1, end='')
#             print("\tFile 2:", line2, end='')
#         break
#
# # closing files
# f1.close()
# f2.close()