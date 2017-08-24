import sys

def main():
    parameters = sys.argv
    basename = parameters[1]
    length = int(parameters[2])

    with open(basename + "_" + str(length) + ".txt", "w") as f:
        for i in range(1, length+1):
            if i == 0:
                i.write(basename + "\n")
            else:
                i.write(basename + "page" + str(i) + "/\n")
    f.close()

if __name__ == '__main__':
    main()