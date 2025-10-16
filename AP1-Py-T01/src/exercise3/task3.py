class FigureDetector:
    def __init__(self):
        self.square = 0
        self.circle = 0
        self.n = 0
        self.m = 0
        self.matrix = []

    def read_file(self, filename='input.txt'):
        with open(filename, 'r', encoding='utf-8') as input_f:
            for line in input_f:
                input_lst = list(map(int, line.split()))
                self.matrix.append(input_lst)
                self.m += 1
        self.n = len(input_lst)

    def scanner(self):
        for i, row in enumerate(self.matrix):
            for j, element in enumerate(row):
                if element == 1:
                    self.fill_number_one_zone(i, j)

    def circle_or_square(self, visited):
        """
        сделаем допущение, что у нас идеальные фигуры,
        которые отличаются только наличием или отсутствием "углов"
        и введем проверку по одному из них (верхний левый угол)
        """
        if len(visited) > 1:
            xs = [x for x, _ in visited]
            ys = [y for _, y in visited]
            min_x, max_x = min(xs), max(xs)
            min_y, max_y = min(ys), max(ys)
            corner = (min_x, min_y)
            if corner in visited:
                self.square += 1
            else:
                self.circle += 1

    def fill_number_one_zone(self, x, y):
        stack = [(x, y)]
        visited = {(x, y)}
        self.matrix[x][y] = 0

        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        while stack:
            cx, cy = stack.pop()
            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.m and 0 <= ny < self.n and self.matrix[nx][ny] == 1:
                    self.matrix[nx][ny] = 0
                    visited.add((nx, ny))
                    stack.append((nx, ny))
        self.circle_or_square(visited)

    def start(self):
        self.read_file()
        self.scanner()
        print(f'{self.square} {self.circle}')


if __name__ == "__main__":
    figure_detector = FigureDetector()
    figure_detector.start()
