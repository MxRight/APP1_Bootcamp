def vector_mul():
    x1, y1, z1 = map(float, input().split())
    x2, y2, z2 = map(float, input().split())
    return x1 * x2 + y1 * y2 + z1 * z2


if __name__ == "__main__":
    print(vector_mul())
