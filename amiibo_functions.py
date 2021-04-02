from amiibo import AmiiboDump, AmiiboMasterKey
import random


class BinManager:
    def __init__(self, char_dict):
        """
        This class manages bin files, does transplants and serial editing
        :param char_dict:
        """
        self.characters = char_dict

    def update_char_dictionary(self, new_char_dict):
        """
        Updates character dictionary

        :param new_char_dict: dictionary to replace old one with
        :return: None
        """
        self.characters = new_char_dict

    def hex_list_to_string(self, values):
        """
        Converts list of hex values to pyamiibo format

        :param values: List of hexadecimal string values
        :return: A string of hexadecimal values in pyamiibo format
        """

        output = ""
        for item in values:
            if len(item) == 1:
                output += '0' + item.upper() + ' '
            else:
                output += item.upper() + ' '
        # removes extra space at the end
        return output[:-1]

    def randomize_sn(self, dump):
        """
        Randomizes the serial number of a given bin dump

        :param dump: Pyamiibo dump of a bin
        :return: None
        """
        serial_number = "04"
        while len(serial_number) < 20:
            temp_sn = hex(random.randint(0, 255))
            # removes 0x prefix
            temp_sn = temp_sn[2:]
            # creates leading zero
            if len(temp_sn) == 1:
                temp_sn = '0' + temp_sn
            serial_number += ' ' + temp_sn
        # if unlocked, keep it unlocked, otherwise unlock and lock
        if not dump.is_locked:
            dump.uid_hex = serial_number
        else:
            dump.unlock()
            dump.uid_hex = serial_number
            dump.lock()

    def transplant(self, bin, character, saveAs_location, key_directory="Brain_Transplant_Assets", randomize_SN=False):
        """
        Takes a bin and replaces it's character ID with given character's ID

        :param bin: file location of bin to use
        :param character: Character from char_dict you want to transplant into
        :param key_directory: file location of Brain_Transplant_Assets Folder
        :param randomize_SN: If the bin SN should be randomized or not
        :return: Character it was transplanted into
        """

        with open(r'\\'.join([key_directory, 'unfixed-info.bin']), 'rb') as fp_d, \
                open(r'\\'.join([key_directory, 'locked-secret.bin']), 'rb') as fp_t:
            master_keys = AmiiboMasterKey.from_separate_bin(
                fp_d.read(), fp_t.read())

        with open('.'.join([bin, 'bin']), 'rb') as fp:
            dump = AmiiboDump(master_keys, fp.read())

        if randomize_SN:
            self.randomize_sn(dump)

        if character == "Random":
            same_check = True
            char_list = list(self.characters.keys())
            while same_check:
                rng_character = random.choice(char_list)
                if rng_character != "Pokemon Trainer":
                    hex_tag = self.characters[rng_character]
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
            dump.lock()
            character = rng_character
            with open(saveAs_location, 'wb') as fp:
                fp.write(dump.data)

        elif character != "All":
            hex_tag = self.characters[character]
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
            with open(saveAs_location, 'wb') as fp:
                fp.write(dump.data)

        else:
            warning = input('''WARNING, FOR THIS SERIAL NUMBERS ARE CHANGED, NOT RANDOMIZED, DO NOT SEND THESE TO TOURNEYS
            Also this will create a lot of bins, I hope you know what you are doing
            Also Also all bins for this are saved in Brain_Transplant_Assets
            Are you sure you want to continue? (y/n) ''')
            if warning.lower() != 'y':
                input("The program will now close.")
                exit()

            serial_number_tail = 10
            for char in self.characters:
                hex_tag = self.characters[char]
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
                with open(r'/'.join([key_directory, '.'.join([char, "bin"])]), 'wb') as fp:
                    fp.write(dump.data)
        return character


