import tkinter

def flatten_pair(pair):
    return pair[0] * pair[1]


def check_if_list_pair(pairs_list):
    if any(isinstance(elem, pairs_list) for elem in pairs_list):
        return flatten_list(pairs_list)
    else:
        return flatten_pair(pairs_list)


def flatten_list(pairs_list):
    return sum(map(check_if_list_pair, pairs_list))

