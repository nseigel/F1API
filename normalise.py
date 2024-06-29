import info as l

def min_max_value(data):
    mins = []
    maxes = []
    for group in data:
        mins.append(min(group))
        maxes.append(max(group))
    
    return(min(mins), max(maxes))

def scale(data, factor):
    for group in data:
        for i in range(len(group)):
            group[i] = group[i] * factor
    return data

def normalize(data, factor):
    abs_min, abs_max = min_max_value(data)
    negative_values = abs_min < 0
    data_range = abs_max - abs_min
    correction_factor = abs(abs_min)
    for group in data:
        if negative_values:
            for i in range(len(group)):
                group[i] += correction_factor
        for i in range(len(group)):
            if data_range == 0:
                group[i] = 0
            else:
                group[i] = group[i]/data_range
    data = scale(data, factor)
    return data

def normalize_live(value, factor, circuit):
    abs_min, abs_max = l.circuit_min_max[circuit]
    negative_values = abs_min < 0
    data_range = abs_max - abs_min
    correction_factor = abs(abs_min)
    if negative_values:
        value += correction_factor
        if data_range == 0:
            value = 0
        else:
            value = value/data_range
    value *= factor
    return value 