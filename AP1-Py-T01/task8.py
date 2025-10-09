def different_numbers():
    res = set()
    n = int(input())
    for i in range(n):
        res.add(int(input()))
    return len(res)


if __name__ == "__main__":
    print(different_numbers())
