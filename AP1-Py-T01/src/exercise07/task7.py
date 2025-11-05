class DynamicRobot:
    def __init__(self):
        self.n = 0
        self.m = 0
        self.matrix = None

    def fill_matrix(self):
        self.n, self.m = map(int, input().split())
        self.matrix = [list(map(int, input().split())) for _ in range(self.n)]

    def start(self):
        self.fill_matrix()
        dp = [[0] * self.m for _ in range(self.n)]
        dp[0][0] = self.matrix[0][0]
        for j in range(1, self.m):
            dp[0][j] = dp[0][j - 1] + self.matrix[0][j]
        for i in range(1, self.n):
            dp[i][0] = dp[i - 1][0] + self.matrix[i][0]
        for i in range(1, self.n):
            for j in range(1, self.m):
                dp[i][j] = self.matrix[i][j] + max(dp[i - 1][j], dp[i][j - 1])
        return dp[self.n - 1][self.m - 1]


if __name__ == "__main__":
    t800 = DynamicRobot()
    print(t800.start())
