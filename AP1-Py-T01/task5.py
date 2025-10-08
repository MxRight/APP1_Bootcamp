def my_float():
    num = input()
    point_flag = 0
    minus_flag = 0
    stop_flag = False
    allow_numbers_str = map(str, range(0, 10))
    result = []
    for i in num:
        if i == '-':
            minus_flag+=1
        elif i == '.':
            point_flag+=1
        elif i in allow_numbers_str:
            result.append(i)
        else:
            stop_flag = True
        if stop_flag or minus_flag > 1 or point_flag > 1:
            return 'Convertation error!'






if __name__ == "__main__":
    my_float()