from math import pow


def derivative_at_the_point():
    n, point = input().split()
    n = int(n)
    point = float(point)
    k = []
    for i in range(n + 1):
        k.append(float(input()))
    res = 0
    for i in range(1, n + 1):
        print(k[-i], pow(point, i))
        res += i * k[n - i] * pow(point, i - 1)
    return round(res, 3)


if __name__ == "__main__":
    print(f'{derivative_at_the_point():.3f}')
