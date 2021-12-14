#usage: python $0 <input> <out>

import sys

def rc(sequence):
    read_rc = sequence[::-1]
    out = []
    for i in range(len(read_rc)):
        if read_rc[i] == "A" or read_rc[i] == "a":
            out.append("T")
        elif read_rc[i] == "T" or read_rc[i] == "t":
            out.append("A")
        elif read_rc[i] == "C" or read_rc[i] == "c":
            out.append("G")
        elif read_rc[i] == "G" or read_rc[i] == "g":
            out.append("C")
        elif read_rc[i] == "N" or read_rc[i] == "n":
            out.append("N")
        else:
            try:
                os.exit(1)
            except:
                print("序列含有异常字符")
    return "".join(out)

f1 = open(sys.argv[1], "r")
f2 = open(sys.argv[2], "w")
for i in f1.readlines():
    #print(rc(i.strip()))
    f2.write(rc(i.strip()) + "\n")
f1.close()
f2.close()

