from amiibo import AmiiboMasterKey
from ssbu_amiibo import SsbuAmiiboDump as AmiiboDump
import random

class BinManager:
    def __init__(self, char_dict, key_directory="Brain_Transplant_Assets"):
        """
        This class manages bin files, does transplants and serial editing
        :param char_dict:
        """
        self.characters = char_dict
        self.key_directory = key_directory
        try:
            with open(r'\\'.join([self.key_directory, 'key_retail.bin']), 'rb') as fp_j:
                self.master_keys = AmiiboMasterKey.from_combined_bin(
                    fp_j.read())
        except FileNotFoundError:
            with open(r'/'.join([self.key_directory, 'unfixed-info.bin']), 'rb') as fp_d, \
                open(r'/'.join([self.key_directory, 'locked-secret.bin']), 'rb') as fp_t:
                    self.master_keys = AmiiboMasterKey.from_separate_bin(
                        fp_d.read(), fp_t.read())
    def __open_bin(self, bin_location):
        """
        Opens a bin and makes it 540 bytes if it wasn't

        :param bin_location: file location of bin you want to open
        :return: opened bin
        """
        bin_fp = open(bin_location, 'rb')

        bin_dump = bytes()
        for line in bin_fp:
            bin_dump += line
        bin_fp.close()

        if len(bin_dump) == 540:
            with open(bin_location, 'rb') as fp:
                dump = AmiiboDump(self.master_keys, fp.read())
                return dump
        elif 532 <= len(bin_dump) <= 572:
            while len(bin_dump) < 540:
                bin_dump += b'\x00'
            if len(bin_dump) > 540:
                bin_dump = bin_dump[:-(len(bin_dump) - 540)]
            b = open(bin_location, 'wb')
            b.write(bin_dump)
            b.close()

            with open(bin_location, 'rb') as fp:
                dump = AmiiboDump(self.master_keys, fp.read())
                return dump
        else:
            return None

    def update_char_dictionary(self, new_char_dict):
        """
        Updates character dictionary

        :param new_char_dict: dictionary to replace old one with
        :return: None
        """
        self.characters = new_char_dict

    def randomize_sn(self, dump=None, bin_location=None):
        """
        Randomizes the serial number of a given bin dump
        :param dump: Pyamiibo dump of a bin
        :return: None
        """
        if bin_location is not None:
            dump = self.__open_bin(bin_location)
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
        if bin_location is not None:
            with open(bin_location, 'wb') as fp:
                fp.write(dump.data)

    def transplant(self, bin_location, character, saveAs_location, randomize_SN=False):
        """
        Takes a bin and replaces it's character ID with given character's ID

        :param bin_location: file location of bin to use
        :param character: Character from char_dict you want to transplant into
        :param randomize_SN: If the bin SN should be randomized or not
        :param saveAs_location: location to save new bin
        :return: Character it was transplanted into
        """

        dump = self.__open_bin(bin_location)
        mii_ids = [bytes.fromhex('07c0000000210002'), bytes.fromhex('07c0010000220002'), bytes.fromhex('07c0020000230002')]
        mii_characters = ['Mii Brawler', 'Mii Swordfighter', 'Mii Gunner']
        mii_transplant = 'B3E038270F1D4C92ABCEF5427D67F9DCEC30CE3000000000000000000000000000000000000000000040400000000000001F02000208040304020C1302040306020C010409171304030D080000040A0008040A0004021400'
        if dump is None:
            return None

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
            Opening {} has failed.
            Hit any button to close the program.'''.format(bin))
            exit()
        if (character in mii_characters) and (dump.data[84:92] not in mii_ids):
            dump.data[0x148:0x1A0] = bytes.fromhex(mii_transplant)
        if (character not in mii_characters) and (dump.data[84:92] in mii_ids):
            dump.data[0x148:0x1A0] = bytes.fromhex('0' * 176)
            dump.data[0x143:0x147] = bytes.fromhex('0' * 8)
            dump.data[503] = 0
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
        donor_dump = self.__open_bin(donor)
        receiver_dump = self.__open_bin(receiver)

        if donor_dump is None or receiver_dump is None:
            return None

        receiver_dump.unlock()
        # RO areas from https://wiki.gbatemp.net/wiki/Amiibo give FP metadata needed for transplant
        receiver_dump.data[0:17] = donor_dump.data[0:17]
        receiver_dump.data[52:129] = donor_dump.data[52:129]
        receiver_dump.data[520:533] = donor_dump.data[520:533]
        receiver_dump.lock()

        with open(saveAs_location, 'wb') as fp:
            fp.write(receiver_dump.data)

        return True
