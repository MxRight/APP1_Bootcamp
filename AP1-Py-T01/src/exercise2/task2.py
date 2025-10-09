def palindrome():
    num = int(input())
    if num < 0:
        return False
    else:
        original = num
        reversed_num = 0
        while num > 0:
            digit = num % 10
            reversed_num = reversed_num * 10 + digit
            num //= 10
        return original == reversed_num

if __name__ == "__main__":
    print(palindrome())
