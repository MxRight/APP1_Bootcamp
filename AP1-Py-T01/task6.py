import json


def json_union(path='task6/', filename='input.txt'):
    with open(path + filename, 'r', encoding='utf-8') as input_f:
        data = json.load(input_f)
        one = data['list1']
        two = data['list2']
    sorted_films = sorted(one + two, key=lambda x: x['year'])
    list1 = {"list1": sorted_films}
    json_final = json.dumps(list1, indent=4)
    return json_final


if __name__ == "__main__":
    print(json_union())
