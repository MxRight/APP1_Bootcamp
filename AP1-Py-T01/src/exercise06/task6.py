import json


def json_union(filename='input.txt'):
    try:
        with open(filename, 'r', encoding='utf-8') as input_f:
            data = json.load(input_f)

        one = data['list1']
        two = data['list2']

    except FileNotFoundError:
        return "Ошибка: файл не найден!"
    except json.JSONDecodeError:
        return "Ошибка: файл пустой или содержит некорректный JSON!"
    except KeyError as e:
        return f"Ошибка: отсутствует ключ {e.args[0]} в JSON!"

    if not isinstance(one, list) or not isinstance(two, list):
        return "Ошибка: оба поля 'list1' и 'list2' должны быть списками."

    sorted_films = sorted(one + two, key=lambda x: x['year'])
    list1 = {"list0": sorted_films}
    json_final = json.dumps(list1, indent=4)
    return json_final


if __name__ == "__main__":
    print(json_union())
