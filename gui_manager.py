import PySimpleGUI as sg
from character_dictionary import CharacterDictionary
import os

class ListBoxWrapper:
    def __init__(self, internal_list):
        self._list = internal_list


class ListBoxManager:
    def __init__(self):
        self._listboxes = {}
        self._name_formatter = {}

    def __getitem__(self, key):
        return self._listboxes[key]

    def __found_bins(self, directory):
        found_bins = []
        for bin_file in os.listdir(directory):
            if bin_file[-3:] == "bin":
                if bin_file != 'unfixed-info.bin' and bin_file != 'locked-secret.bin':
                    # To catch powersaves dumb format
                    if '[' not in bin_file:
                        found_bins.append(bin_file[:-4])
                        self._name_formatter[bin_file[:-4]] = bin_file
                    else:
                        found_bins.append(bin_file.split('[')[1].split(']')[0])
                        self._name_formatter[bin_file.split('[')[1].split(']')[0]] = bin_file
        return found_bins

    def add_list_box(self, key, internal_list):
        self._listboxes[key] = internal_list

    def add_dir_box(self, key_list, new_directory):
        found_bins = self.__found_bins(new_directory)
        for key in key_list:
            self._listboxes[key] = found_bins

    def update_dir_box(self, window, key_list, new_directory):
        found_bins = self.__found_bins(new_directory)
        for key in key_list:
            self._listboxes[key] = found_bins
            window[key].update(self._listboxes[key])
        window.refresh()

    def update_list_box(self, window, key, internal_list):
        self._listboxes[key] = internal_list
        window[key].update(self._listboxes[key])
        window.refresh()

    def name_format(self, displayed_name):
        return self._name_formatter[displayed_name]


