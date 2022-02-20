import re
import sys


# Get expected value of an event pair
def flatten_pair(pair):
    return float(pair[0]) * float(pair[1])


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
    if isinstance(pairs_list[0],list):
        return sum(map(check_if_list_pair, pairs_list))
    else:
        if list(pairs_list[1]):
            return pairs_list[0] * sum(map(check_if_list_pair, pairs_list[1]))
        else:
            return flatten_pair(pairs_list)


# This is the entry function into user input, will generate the top level event-outcome pairs
def get_unique_pathways():
    while True:
        num_unique_pathways = input("Input how many unique top-level events can occur:")
        try:
            num_unique_paths = int(num_unique_pathways)
            if num_unique_paths < 1:
                print("Please input a positive integer")
            elif num_unique_paths == 1:
                print("This is top level event 1 of 1")
                return get_pathway()
            else:
                unique_events = []
                for i in range(1, (num_unique_paths + 1)):
                    print("This is top level event " + str(i) + " of " + num_unique_pathways)
                    unique_events.append(get_pathway())
                return unique_events
        except ValueError:
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
                    prob = input("Input probability of this event")
                    if float(prob):
                        break
                    print("Please input a number!")
                events = []
                for i in range(1, num_paths + 1):
                    print("This is pathway " + str(i) + " of " + num_pathways + " leading from the event with probability of " + str(prob))
                    events.append(get_pathway())
                return [float(prob), events]
        except ValueError:
            print("Invalid input detected, please try again")


# This function is used to get users to input a probability-value pair
def get_pair():
    while True:
        prob = input("Input probability of outcome")
        value = input("Input value of outcome")
        if float(prob) and float(value):
            return [float(prob), float(value)]
        else:
            print("Invalid input detected, please try again")


# regex for start of new sub-pathway, group 0 is prob
regex_subpath_start = re.compile("[/[]([.\d]*)[,]")
# regex for probability-value pair, group 0 is prob and group 1 is value
regex_pair = re.compile("[/[]([.\d]*)[,]([.\d]*)[/]]")
# regex for end of sub-pathway
regex_subpath_end = re.compile("[/]]")


def strip_whitespace(input_string):
    return input_string.replace(" ", "")


def parse_file(file_pathway):
    file = open(file_pathway, "r")
    try:
        events = top_level_file_read(file)
        file.close()
        return events
    except ValueError:
        print("File was incorrectly formatted!")
    file.close()
    return


# This is the controlling function for reading an input file. If this function reaches the end of a file, we know that
# the file was properly formatted and can return the events list.
# Checking if object exists is slightly inefficient, but more readable
def top_level_file_read(file):
    events = []
    while True:
        # Remove all white space from the input line!
        line = file.readline().replace(" ", "")
        if len(line) == 0:
            break
        elif regex_pair.match(line):
            events.append(read_pair(line))
        elif regex_subpath_start.match(line):
            subpath_start = regex_subpath_start.match(line)
            subpath = []
            subpath.append(float(subpath_start.group(1)))
            subpath.append(read_subpath(file))
            events.append(subpath)
        else:
            return ValueError
    return events

# Given a line we know has a probability-value pair, return the pair as a list
def read_pair(line):
    pair = regex_pair.match(line)
    pair_list = []
    for group in pair.groups():
        pair_list.append(float(group))
    return pair_list

# After we detect the start of an event subpath, pass the file to this function to properly format the subpath
def read_subpath(file):
    subpath = []
    while True:
        # Remove all white space from the input line!
        line = file.readline().replace(" ", "")
        if regex_pair.match(line):
            subpath.append(read_pair(line))
        elif regex_subpath_start.match(line):
            new_subpath_start = regex_subpath_start.match(line)
            new_subpath = []
            new_subpath.append(float(new_subpath_start.group(1)))
            new_subpath.append(read_subpath(file))
            subpath.append(new_subpath)
        elif regex_subpath_end.match(line):
            return subpath
        else:
            return ValueError

# Q for quit, R for read file and M for manual input
def main():
    while True:
        mode = (input("Input R(/r) to read from file, M(/m) to input manually, Q(/q) to quit")).upper()[0]
        if mode == "Q":
            sys.exit(0)
        elif mode == "R":
            print("File input selected")
            file_name = input("Please input file name")
            file_input = top_level_file_read(file_name)
            print("The expected value of the event is: " + str(flatten_list(file_input)))
        elif mode == "M":
            print("Manual input selected")
            user_input = get_unique_pathways()
            print("The expected value of the event is: " + str(flatten_list(user_input)))
        else:
            print("Invalid input detected, please try again")


if __name__ == "__main__":
    main()
