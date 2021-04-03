from amiibo import AmiiboDump, AmiiboMasterKey
import random


class BinManager:
    def __init__(self, char_dict, key_directory="Brain_Transplant_Assets"):
        """
        This class manages bin files, does transplants and serial editing
        :param char_dict:
        """
        self.characters = char_dict
        self.key_directory = key_directory
        with open(r'\\'.join([self.key_directory, 'unfixed-info.bin']), 'rb') as fp_d, \
                open(r'\\'.join([self.key_directory, 'locked-secret.bin']), 'rb') as fp_t:
            self.master_keys = AmiiboMasterKey.from_separate_bin(
                fp_d.read(), fp_t.read())

    def update_char_dictionary(self, new_char_dict):
        """
        Updates character dictionary

        :param new_char_dict: dictionary to replace old one with
        :return: None
        """
        self.characters = new_char_dict

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

    def transplant(self, bin_location, character, saveAs_location, randomize_SN=False):
        """
        Takes a bin and replaces it's character ID with given character's ID

        :param bin_location: file location of bin to use
        :param character: Character from char_dict you want to transplant into
        :param randomize_SN: If the bin SN should be randomized or not
        :param saveAs_location: location to save new bin
        :return: Character it was transplanted into
        """

        with open(bin_location, 'rb') as fp:
            dump = AmiiboDump(self.master_keys, fp.read())

        if randomize_SN:
            self.randomize_sn(dump)
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
        dump.data[84:92] = bytes.fromhex(hex_tag)
        dump.lock()
        with open(saveAs_location, 'wb') as fp:
            fp.write(dump.data)
        return character

    def serial_swapper(self, donor, receiver, saveAs_location):
        """
        Transfer the SN of the donor to the receiver, saves new bin at given location

        :param donor: bin to give SN
        :param receiver: bin to receive SN
        :param saveAs_location: location to save new bin
        :return: None
        """
        with open('.'.join([donor, 'bin']), 'rb') as fp:
            donor_dump = AmiiboDump(self.master_keys, fp.read())
        with open('.'.join([receiver, 'bin']), 'rb') as fp:
            receiver_dump = AmiiboDump(self.master_keys, fp.read())
        receiver_dump.unlock()
        receiver_dump.uid_hex = donor_dump.uid_hex
        receiver_dump.lock()

        with open(saveAs_location, 'wb') as fp:
            fp.write(receiver_dump.data)
