from amiibo import AmiiboDump, AmiiboMasterKey
import random
import os


# takes characters and hexnums from characters.txt for character menu
def create_character_dict(directory):
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
        print("Characters loaded in successfully.")
        print(' ')
    except:
        input("Something went wrong with characters.txt, please read the README.txt, program will now close.")
        end()
    return char_dict


# does a brain transplant from to selected character, if character is Random it rolls a random character
def transplant(bin, character, char_dict, directory):
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
        #can't figure out how to get bin to work with random alts
        #rand_alt = random.choice(["00", "01", "02", "03", "04", "05", "06", "07"])
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


# prints a list in a 3 column format, bottom line looks bad if not multiple of 3
def print_bins(input_list):
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


# handles picking character/random
def character_selector(char_dict):
    char_list = list(char_dict.keys())
    char_list += ["All", "Random"]
    print_bins(char_list)
    print("Note: Using the Random option will overwrite any bins involved. The other options will create additional bins.")
    char_error = True
    while char_error:
        answer = input("Please type in name EXACTLY as it appears: ")
        if answer in char_list:
            return answer
        else:
            print("Character not found, please try again!")
