class GreedyRobot:
    def __init__(self):
        self.coins = 0
        self.n = 0
        self.m = 0
        self.x = 0
        self.y = 0
        self.matrix = None

    def fill_matrix(self):
        self.n, self.m = map(int, input().split())
        self.matrix = [list(map(int, input().split())) for _ in range(self.n)]

    def start(self):
        self.fill_matrix()
        while True:
            self.coins += self.matrix[self.x][self.y]
            self.right_or_down()
            if self.is_finish():
                break
        return self.coins

    def right_or_down(self):
        at_bottom = self.x == self.n - 1
        at_right = self.y == self.m - 1

        if not at_bottom and (at_right or self.matrix[self.x + 1][self.y] >= self.matrix[self.x][self.y + 1]):
            self.x += 1
        elif not at_right:
            self.y += 1

    def is_finish(self):
        if self.x == self.n - 1 and self.y == self.m - 1:
            return True
        return False


if __name__ == "__main__":
    t800 = GreedyRobot()
    print(t800.start())
