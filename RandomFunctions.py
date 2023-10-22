def locate_element(array: list, element):
    places_found = []
    if element in array:
        index = 0
        for item in array:
            if item == element:
                places_found.append(index)
            index += 1
    return places_found


def mean_list(array: list):
    total = 0
    for num in array:
        total += num
    return total / len(array)


def replace_element(array: list, original, new):
    locations = locate_element(array, original)
    print(locations)
    for location in locations:
        array = array[:location] + [new] + array[location + 1:]
    return array
