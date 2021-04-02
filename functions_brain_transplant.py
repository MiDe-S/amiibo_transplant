from amiibo import AmiiboDump, AmiiboMasterKey
import random
import os


def create_character_dict(directory):
    '''
    Reads characters and hexnums from characters.txt for character menu
    :param directory: file location of characters.txt
    :return: Dictionary of character: hexnum
    '''
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


def hex_list_to_string(values):
    '''
    Converts list of hex values to pyamiibo format

    :param values: List of hexadecimal string values
    :return: A string of hexadecimal values in pyamiibo format
    '''

    output = ""
    for item in values:
        if len(item ) == 1:
            output += '0' + item.upper() + ' '
        else:
            output += item.upper() + ' '
    # removes extra space at the end
    return output[:-1]


def print_bins(input_list):
    '''
    Prints a list of bin names in a 3 column format, bottom line looks bad if not multiple of 3

    :param input_list: list of bin names
    :return: None
    '''
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


def ask_for_bin_name(insert_all = True):
    '''
    Prompts user to select bin name from pwd

    :param insert_all: bool containing if "All" should be an option
    :return: string of selected file name
    '''
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


def transplant(bin, character, char_dict, directory):
    '''
    Takes a bin and replaces it's character ID with given character's ID

    :param bin: file location of bin to use
    :param character: Character from char_dict you want to transplant into
    :param char_dict: character dictionary from create_character_dictionary
    :param directory: file location of Brain_Transplant_Assets Folder
    :return: None
    '''
    directory = r'/'.join([directory, "Brain_Transplant_Assests"])
    with open(r'/'.join([directory, 'unfixed-info.bin']), 'rb') as fp_d, \
            open(r'/'.join([directory, 'locked-secret.bin']), 'rb') as fp_t:
        master_keys = AmiiboMasterKey.from_separate_bin(
            fp_d.read(), fp_t.read())

    with open('.'.join([bin, 'bin']), 'rb') as fp:
        dump = AmiiboDump(master_keys, fp.read())

    if character == "Random":
        same_check = True
        char_list = list(char_dict.keys())
        while same_check:
            rng_character = random.choice(char_list)
            if rng_character != "Pokemon Trainer":
                hex_tag = char_dict[rng_character]
            else:
                hex_tag = random.choice(["1907000003840002", "1902000003830002", "1906000000240002"])

            hex_tag = hex_tag[0] + hex_tag[1] + ' ' + hex_tag[2] + hex_tag[3] + ' ' + hex_tag[4] + hex_tag[5] + ' ' + \
                      hex_tag[6] + hex_tag[7] + ' ' + hex_tag[8] + hex_tag[9] + ' ' + hex_tag[10] + hex_tag[11] + ' ' + \
                      hex_tag[12] + hex_tag[13] + ' ' + hex_tag[14] + hex_tag[15]

            try:
                dump.unlock()
            except:
                input('''
                Opening {} has failed, this is probably because the bin isn't exactly 540 bytes in size
                To fix your bin, please check out the README
                Hit any button to close the program.'''.format(bin))
                exit()

            if dump.data[84:92] != bytes.fromhex(hex_tag):
                same_check = False
            else:
                dump.lock()
        # prevents conversion of mii fighters
        if ' '.join('{:02X}'.format(b) for b in dump.data[84:86]) == "07 C0":
            input("Mii fighters are currently not usable with this program, press any button to exit")
            exit()
        dump.data[84:92] = bytes.fromhex(hex_tag)
        # can't figure out how to get bin to work with random alts
        #dump.data[503:504] = bytes.fromhex(rand_alt)
        dump.lock()
        print("{} is now a {} amiibo".format(bin, rng_character))
        new_bin_name = bin
        with open('.'.join([new_bin_name, "bin"]), 'wb') as fp:
            fp.write(dump.data)

    elif character != "All":
        hex_tag = char_dict[character]
        hex_tag = hex_tag[0] + hex_tag[1] + ' ' + hex_tag[2] + hex_tag[3] + ' ' + hex_tag[4] + hex_tag[5] + ' ' + \
                  hex_tag[6] + hex_tag[7] + ' ' + hex_tag[8] + hex_tag[9] + ' ' + hex_tag[10] + hex_tag[11] + ' ' + \
                  hex_tag[12] + hex_tag[13] + ' ' + hex_tag[14] + hex_tag[15]

        try:
            dump.unlock()
        except:
            input('''
            Opening {} has failed, this is probably because the bin isn't exactly 540 bytes in size
            To fix your bin, please check out the README
            Hit any button to close the program.'''.format(bin))
            exit()
        # prevents conversion of mii fighters
        if ' '.join('{:02X}'.format(b) for b in dump.data[84:86]) == "07 C0":
            input("Mii fighters are currently not usable with this program, press any button to exit")
            exit()
        dump.data[84:92] = bytes.fromhex(hex_tag)
        dump.lock()
        new_bin_name = "{} into a {}".format(bin, character)
        with open('.'.join([new_bin_name, "bin"]), 'wb') as fp:
            fp.write(dump.data)

    else:
        warning = input('''WARNING, FOR THIS SERIAL NUMBERS ARE CHANGED, NOT RANDOMIZED, DO NOT SEND THESE TO TOURNEYS
        Also this will create a lot of bins, I hope you know what you are doing
        Also Also all bins for this are saved in Brain_Transplant_Assests
        Are you sure you want to continue? (y/n) ''')
        if warning.lower() != 'y':
            input("The program will now close.")
            exit()

        serial_number_tail = 10
        for char in char_dict:
            hex_tag = char_dict[char]
            hex_tag = hex_tag[0] + hex_tag[1] + ' ' + hex_tag[2] + hex_tag[3] + ' ' + hex_tag[4] + hex_tag[5] + ' ' + \
                      hex_tag[6] + hex_tag[7] + ' ' + hex_tag[8] + hex_tag[9] + ' ' + hex_tag[10] + hex_tag[11] + ' ' + \
                      hex_tag[12] + hex_tag[13] + ' ' + hex_tag[14] + hex_tag[15]

            try:
                dump.unlock()
            except:
                input('''
                Opening {} has failed, this is probably because the bin isn't exactly 540 bytes in size
                To fix your bin, please check out the README
                Hit any button to close the program.'''.format(bin))
                exit()

            dump.data[84:92] = bytes.fromhex(hex_tag)
            serial_number = '04 FF FF FF FF FF ' + str(serial_number_tail)
            serial_number_tail += 1
            dump.uid_hex = serial_number
            dump.lock()
            with open(r'/'.join([directory, '.'.join([char, "bin"])]), 'wb') as fp:
                fp.write(dump.data)





def character_selector(char_dict, insert_all=True, insert_random=True):
    '''
    Interface for picking character from char_dict

    :param char_dict: created from create_character_dict
    :param insert_all: bool indicating if 'All' should be an option
    :param insert_random: bool indicating if 'Random' should be an option
    :return: The name of the chosen character
    '''
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


def bin_value_getter():
    '''
    Gets all the "personality" values of the bins in the same folder as this .py script
    and returns them in a list of lists

    :return: None
    '''

    # Opening Key Files
    with open(r'Brain_Transplant_Assests\unfixed-info.bin', 'rb') as fp_d, \
            open(r'Brain_Transplant_Assests\locked-secret.bin', 'rb') as fp_t:
        master_keys = AmiiboMasterKey.from_separate_bin(
            fp_d.read(), fp_t.read())

    # gets current directory
    directory = os.path.dirname(os.path.realpath(__file__))
    bin_values = []
    for bin_file in os.listdir(directory):
        if bin_file[-3:] == "bin":
            if bin_file != 'unfixed-info.bin' and bin_file != 'locked-secret.bin':
                try:
                    with open(bin_file, 'rb') as fp:
                        dump = AmiiboDump(master_keys, fp.read())
                except...:
                    input("Failed to open: ", bin_file)

                dump.unlock()

                value_string = ' '.join('{:02X}'.format(b) for b in dump.data[444:502])

                # to get rid of bad POWERSAVES formatting
                if '[' in bin_file:
                    file_name = bin_file.split('[')[1].split(']')[0]
                else:
                    file_name = bin_file.split('.')[0]
                values = value_string.split(' ')
                bin_values.append(values)
                print("Successfully Opened: ", file_name)
                fp.close()

    fp_d.close()
    fp_t.close()
    return bin_values


def construct_bin(base_bin_location, character, values, char_dict):
    '''
    Makes a bin based on a given base, with character string
    and list of values to be used

    :param base_bin_location: file_location of bin to build off of
    :param character: character to use
    :param values: list of values to paste into values section
    :param char_dict: character_dictionary made from characters.txt
    :return: None
    '''

    # Opening Key Files
    with open(r'Brain_Transplant_Assests\unfixed-info.bin', 'rb') as fp_d, \
            open(r'Brain_Transplant_Assests\locked-secret.bin', 'rb') as fp_t:
        master_keys = AmiiboMasterKey.from_separate_bin(
            fp_d.read(), fp_t.read())
    with open(base_bin_location, 'rb') as fp:
        dump = AmiiboDump(master_keys, fp.read())

    hex_tag = char_dict[character]
    hex_tag = hex_tag[0] + hex_tag[1] + ' ' + hex_tag[2] + hex_tag[3] + ' ' + hex_tag[4] + hex_tag[5] + ' ' + \
        hex_tag[6] + hex_tag[7] + ' ' + hex_tag[8] + hex_tag[9] + ' ' + hex_tag[10] + hex_tag[11] + ' ' + \
        hex_tag[12] + hex_tag[13] + ' ' + hex_tag[14] + hex_tag[15]

    try:
        dump.unlock()
    except:
        input('''
                Opening {} has failed, this is probably because the bin isn't exactly 540 bytes in size
                To fix your bin, please check out the README
                Hit any button to close the program.'''.format(base_bin_location))
        exit()
    # prevents conversion of mii fighters
    if ' '.join('{:02X}'.format(b) for b in dump.data[84:86]) == "07 C0":
        input("Mii fighters are currently not usable with this program, press any button to exit")
        exit()

    dump.randomize_sn()

    dump.data[84:92] = bytes.fromhex(hex_tag)

    values = hex_list_to_string(values)
    dump.data[444:502] = bytes.fromhex(values)
    dump.data[503] = 7

    dump.lock()
    new_bin_name = "Calculated {}".format(character)
    with open('.'.join([new_bin_name, "bin"]), 'wb') as fp:
        fp.write(dump.data)
