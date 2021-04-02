import PySimpleGUI as sg
from amiibo_functions import *
import os


def create_character_dict(directory):
    """
    Reads characters and hexnums from characters.txt for character menu
    :param directory: file location of characters.txt
    :return: Dictionary of character: hexnum
    """
    char_dict = {}
    directory = r'/'.join([directory, "Brain_Transplant_Assets"])
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


def main():
    # Initialize variables that get used throughout the program
    version_number = "2.0.0"
    # Menu key variables for GUI
    character_key = '_character_'
    save_location_key = '_save_location_'
    submitted_key = '_transplant-submission_'
    bin_name_key = '_bin-name_'
    success_text_key = '_transplant-success_'
    randomize_sn_key = '_randomize-sn_'

    # gets current key_directory
    directory = os.path.dirname(os.path.realpath(__file__))

    char_dict = create_character_dict(directory)

    transplanter = BinManager(char_dict)

    found_bins = []
    for bin_file in os.listdir(directory):
        if bin_file[-3:] == "bin":
            if bin_file != 'unfixed-info.bin' and bin_file != 'locked-secret.bin':
                found_bins.append(bin_file[:-4])

    characters = list(char_dict.keys())
    characters.insert(0, "Random")

    layout = [[sg.Text('My one-shot window.')],
              [sg.Input(key=submitted_key, enable_events=True, visible=False)],
              [sg.Listbox(found_bins, sg.LISTBOX_SELECT_MODE_SINGLE, size=(30, 10), key=bin_name_key),
               sg.Listbox(characters, sg.LISTBOX_SELECT_MODE_SINGLE, size=(30, 10), key=character_key)],
              [sg.Checkbox("Randomize Serial Number", key=randomize_sn_key, enable_events=True, default=True),
               sg.FileSaveAs("Transplant", target=submitted_key, key=save_location_key, file_types=(('Bin Files', '*.bin'),), default_extension=".bin", initial_folder=directory)],
              [sg.Text(key=success_text_key, size=(10, 1), visible=False)]]

    window = sg.Window('MiDes Brain Transplant Service - Version {}'.format(version_number), layout)

    w = True
    while w:
        event, values = window.read()
        print(event, values)
        if event == submitted_key:
            bins_to_transplant = values[bin_name_key]
            selected_characters = values[character_key]
            # If only 1 character and 1 bin were chosen do the single transplant
            if len(selected_characters) == 1 and len(bins_to_transplant) == 1:
                chosen_character = transplanter.transplant(bins_to_transplant[0], selected_characters[0], values[save_location_key])
                # Prints message showing a successful transplant
                if values[randomize_sn_key]:
                    success_message = "{} bin was saved at {}".format(chosen_character, values[save_location_key], randomize_sn=True)
                else:
                    success_message = "{} bin was saved at {}".format(chosen_character, values[save_location_key], randomize_sn=False)
                window[success_text_key].update(success_message, visible=True)
                window[success_text_key].set_size((len(success_message), 1))
                # refresh window to show updates
                window.refresh()
        if event == sg.WIN_CLOSED:
            break

    window.close()


if __name__ == '__main__':
    main()
