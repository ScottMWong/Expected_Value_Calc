def main():
    print(flatten_list([[0.5,-3],[0.5,4]]))


if __name__ == "__main__":
    main()


# Get expected value of an event pair
def flatten_pair(pair):
    return pair[0] * pair[1]


# Checks if the list contains any event pairs, and if so tries to have them evaluated
def check_if_list_pair(pairs_list):
    if any(isinstance(elem, list) for elem in pairs_list):
        return flatten_list(pairs_list)
    elif len(pairs_list) == 1:
        if list(pairs_list[0]):
            return flatten_pair(pairs_list[0])
        else:
            return pairs_list
    else:
        return flatten_pair(pairs_list)


# Get the expected value of a list of outcomes
def flatten_list(pairs_list):
    if isinstance(pairs_list[0],float):
        return pairs_list[0] * sum(map(check_if_list_pair, pairs_list[1]))
    return sum(map(check_if_list_pair, pairs_list))


# This is the entry function into user input, will generate the top level event-outcome pairs
def get_unique_pathways():
    while True:
        num_unique_pathways = input("Input how many unique top-level events can occur:")
        try:
            num_unique_paths = int(num_unique_pathways)
            if num_unique_paths < 1:
                print("Please input a positive integer")
            elif num_unique_paths == 1:
                return get_pair()
            else:
                unique_events = []
                for i in range(1, num_unique_paths + 1):
                    print("This is top level event " + i + " of " + num_unique_paths)
                    unique_events.append(get_pathway())
                return unique_events
        except:
            print("Invalid input detected, please input an integer")


# This is the main function to get users to input a list containing a tree of probabilities and values
def get_pathway():
    while True:
        num_pathways = input("Input number of pathways for this event:")
        try:
            num_paths = int(num_pathways)
            if num_paths < 1:
                print("Please input a positive integer")
            elif num_paths == 1:
                return get_pair()
            else:
                while True:
                    prob = input("Input probability of this event pathway")
                    if float(prob):
                        break
                events = []
                for i in range(1, num_paths + 1):
                    print("This is pathway " + i + " of " + num_paths + "leading from the event with probability of " + prob)
                    events.append(get_pathway())
                return [prob, events]
        except:
            print("Invalid input detected, please try again")


# This function is used to get users to input a probability-value pair
def get_pair():
    while True:
        prob = input("Input probability of outcome")
        value = input("Input value of outcome")
        if float(prob) and float(value):
            return [prob, value]
        else:
            print("Invalid input detected, please try again")