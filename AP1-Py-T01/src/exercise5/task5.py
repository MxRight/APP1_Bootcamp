def my_float():
    num = input()
    len_of_num = len(num)
    if len_of_num > 0:
        return validation(num)
    else:
        return 'Conversion error!'


def validation(num: str):
    """
    Не пустая.
    Может содержать только: цифры, один минус (только в начале), и не более одной точки.
    После минуса должно быть хотя бы одна цифра или точка с цифрами.
    После точки тоже должна быть хотя бы одна цифра, если она есть.

    """

    point_flag = 0
    minus_flag = 0
    numbers_after_point = None
    stop_flag = False
    allow_numbers_str = map(str, range(0, 10))
    integer_part, fractional_part = [], []
    result = []
    for i in num:
        if i == '-':
            minus_flag += 1
        elif i == '.':
            point_flag += 1
            numbers_after_point = 0
        elif i in allow_numbers_str:
            result.append(i)
            if point_flag == 1:
                numbers_after_point+=1
        else:
            stop_flag = True
        if stop_flag or minus_flag > 1 or point_flag > 1 or numbers_after_point == 0:
            return 'Conversion error!'



if __name__ == "__main__":
    my_float()