def pascal_triangle():
    num = input()
    if num.isdigit() and int(num) > 0:
        num = int(num)
        for n in range(num):
            for k in range(n + 1):
                print(factorial(n) // (factorial(k) * factorial(n - k)), end=' ')
            print()
    else:
        print('Natural number was expected')


def factorial(num):
    res = 1
    for i in range(1, num + 1):
        res *= i
    return res


if __name__ == "__main__":
    pascal_triangle()
