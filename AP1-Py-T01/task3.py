#under construction!

def main():
    return figure_finder(read_file())


def read_file(path='task3/', filename='input.txt'):
    res = []
    with open(path + filename, 'r', encoding='utf-8') as input_f:
        for line in input_f:
            res.append(list(map(int, line.split())))
    return res


def figure_finder(matrix):
    square, circle = 0, 0
    visited = set()
    for i, row in enumerate(matrix):
        for j, element in enumerate(row):
            if element == 1:
                visited.add((i, j))
    return visited
    #return square, circle


if __name__ == "__main__":
    print(main())
    # main()
