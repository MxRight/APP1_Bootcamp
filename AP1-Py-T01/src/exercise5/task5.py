from math import pow


def validation():
    num = input()
    len_of_num = len(num)
    error_msg = 'Conversion error!'
    if len_of_num == 0:
        return error_msg
    is_valid = True
    point_flag = False
    minus_flag = False
    numbers_of_elements = 0
    numbers_after_point = 0
    allow_numbers_str = list(map(str, range(0, 10)))
    str_integer_lst = []
    for i in num:
        if i == '-' and minus_flag == False and numbers_of_elements == 0:
            minus_flag = True
        elif i == '-' and (minus_flag == True or numbers_of_elements > 0):
            is_valid = False
            break
        elif i == '.' and point_flag == True:
            is_valid = False
            break
        elif i == '.' and point_flag == False:
            point_flag = True
        elif i in allow_numbers_str:
            str_integer_lst.append(i)
            if point_flag:
                numbers_after_point += 1
        else:
            is_valid = False
            break
        numbers_of_elements += 1
    if point_flag and numbers_after_point == 0:
        is_valid = False
    if is_valid:
        return calculation(str_integer_lst, numbers_after_point, minus_flag)
    else:
        return error_msg


def calculation(str_integer_lst, numbers_after_point, minus=False):
    result = 0
    for k, v in enumerate(str_integer_lst[::-1]):
        result += int(v) * pow(10, k)
    if numbers_after_point > 0:
        result /= pow(10, numbers_after_point)
    if minus:
        result *= -1
    return result * 2


if __name__ == "__main__":
    res = validation()
    print(res if isinstance(res, str) else f"{res:.3f}")
