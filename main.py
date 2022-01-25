

def flatten_pair(pair):
    return pair[0] * pair[1]


def check_if_list_pair(pairs_list):
    if any(isinstance(elem, list) for elem in pairs_list):
        return flatten_list(pairs_list)
    elif len(pairs_list) == 1:
        return pairs_list
    else:
        return flatten_pair(pairs_list)


def flatten_list(pairs_list):
    if isinstance(pairs_list[0],float):
        return pairs_list[0] * sum(map(check_if_list_pair, pairs_list[1]))
    return sum(map(check_if_list_pair, pairs_list))


def main():
    print(flatten_list([[0.5,-3],[0.5,4]]))


if __name__ == "__main__":
    main()

def get_pathway():
    while True:
        num_pathways = input("Input number of pathways:")
        try:
            num_paths = int(num_pathways)
            if num_paths < 1:
                print("Please input a positive integer")
            elif num_paths == 1:
            else:

        except:
            print("Invalid input detected, please try again")
