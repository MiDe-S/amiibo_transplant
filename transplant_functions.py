from amiibo import AmiiboDump, AmiiboMasterKey
import random
import os


def create_character_dict(directory):
    """
    Reads characters and hexnums from characters.txt for character menu
    :param directory: file location of characters.txt
    :return: Dictionary of character: hexnum
    """
    char_dict = {}
    directory = r'/'.join([directory, "Brain_Transplant_Assests"])
    try:
        with open(r'/'.join([directory, 'characters.txt']), 'r') as char_list:
            for line in char_list:
                if line[0] == '@':
                    continue
                else:
                    line = line.split(',')
                    # removes line break character
                    if len(line[1]) > 16:
                        line[1] = line[1][:-1]
                    char_dict[line[0]] = line[1]
        print("Characters loaded in successfully.\n")
    except:
        input("Something went wrong with characters.txt, please read the README.txt, enter any button to close.")
        exit()
    return char_dict


def print_bins(input_list):
    """
    Prints a list of bin names in a 3 column format, bottom line looks bad if not multiple of 3

    :param input_list: list of bin names
    :return: None
    """
    print('-' * 50)
    for index in range(0, len(input_list), 3):
        try:
            print("{} | {} | {}".format(input_list[index], input_list[index + 1], input_list[index + 2]))
        except:
            try:
                print("{} | {}".format(input_list[index], input_list[index + 1]))
            except:
                print("{}".format(input_list[index]))
    print('-' * 50)


def ask_for_bin_name(insert_all=True):
    """
    Prompts user to select bin name from pwd

    :param insert_all: bool containing if "All" should be an option
    :return: string of selected file name
    """
    # gets current directory
    directory = os.path.dirname(os.path.realpath(__file__))
    found_bins = []
    for bin_file in os.listdir(directory):
        if bin_file[-3:] == "bin":
            if bin_file != 'unfixed-info.bin' and bin_file != 'locked-secret.bin':
                found_bins.append(bin_file[:-4])

    # for printing out found bins
    print("Detected Bins:")
    print_bins(found_bins)
    # asks user to pick a bin
    name_error = True
    while name_error:
        selected_bin = input("Enter bin name EXACTLY as it appears: ")
        if insert_all and selected_bin == "All":
            name_error = False
            return found_bins
        elif selected_bin in found_bins:
            name_error = False
            return selected_bin + ".bin"
        else:
            print("ERROR: Name not found, please try again")


def character_selector(char_dict, insert_all=True, insert_random=True):
    """
    Interface for picking character from char_dict

    :param char_dict: created from create_character_dict
    :param insert_all: bool indicating if 'All' should be an option
    :param insert_random: bool indicating if 'Random' should be an option
    :return: The name of the chosen character
    """
    char_list = list(char_dict.keys())
    if insert_all:
        char_list.append("All")
    if insert_random:
        char_list.append("Random")
    print_bins(char_list)
    print("Note: Using the Random option will overwrite any bins involved. The other options will create additional bins.")
    char_error = True
    while char_error:
        answer = input("Please type in name EXACTLY as it appears: ")
        if answer in char_list:
            return answer
        else:
            print("Character not found, please try again!")
