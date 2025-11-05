def device_selection():
    error = "\nError: incorrect input"
    try:
        n, t = map(int, input().split())
    except ValueError:
        return error

    devices = {}
    min_cost = None

    for _ in range(n):
        try:
            year, cost, worktime = map(int, input().split())
        except ValueError:
            return error

        if year not in devices:
            devices[year] = {}
        if (t - worktime) in devices[year]:
            new_cost = cost + devices[year][t - worktime]
            if min_cost is None or new_cost < min_cost:
                min_cost = new_cost

        if worktime not in devices[year]:
            devices[year][worktime] = cost
        else:
            devices[year][worktime] = min(cost, devices[year][worktime])

    return min_cost if min_cost is not None else error


if __name__ == "__main__":
    print(device_selection())
