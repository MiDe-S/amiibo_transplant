import PySimpleGUI as sg
from amiibo_functions import *
from character_dictionary import CharacterDictionary
import os


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
    folder_location_key = '_selected-folder_'
    browsed_key = '_browse-submission_'
    pwd_key = '_current-directory_'

    # gets current key_directory
    directory = os.path.dirname(os.path.realpath(__file__))

    char_dict = CharacterDictionary()

    transplanter = BinManager(char_dict)

    found_bins = []
    for bin_file in os.listdir(directory):
        if bin_file[-3:] == "bin":
            if bin_file != 'unfixed-info.bin' and bin_file != 'locked-secret.bin':
                found_bins.append(bin_file[:-4])

    characters = char_dict.get_list(insert_random=True)

    transplant_layout = [[sg.FolderBrowse(target=browsed_key, key=folder_location_key, enable_events=True), sg.Text("Currently looking at:"), sg.Text(directory, key=pwd_key, auto_size_text=True)],
              [sg.Input(key=submitted_key, enable_events=True, visible=False), sg.Input(key=browsed_key, enable_events=True, visible=False)],
              [sg.Listbox(found_bins, sg.LISTBOX_SELECT_MODE_SINGLE, size=(40, 10), key=bin_name_key), sg.VerticalSeparator(),
               sg.Listbox(characters, sg.LISTBOX_SELECT_MODE_SINGLE, size=(30, 10), key=character_key)],
              [sg.FileSaveAs("Transplant", target=submitted_key, key=save_location_key, file_types=(('Bin Files', '*.bin'),), default_extension=".bin", initial_folder=directory),
               sg.Checkbox("Randomize Serial Number", key=randomize_sn_key, enable_events=True, default=True)],
              [sg.Text(key=success_text_key, size=(10, 1), visible=False)]]

    serial_swapper_layout = [[sg.Text("Lasaga wins amiibo")]]

    character_editor_layout = [[sg.Text("who knows")]]

    about_layout = [[sg.Text("Version Number {}".format(version_number))],
                    [sg.Text("If you encounter issues raise an issue on github or dm MiDe#9934 on discord")],
                    [sg.Text("Shoutouts to the amiibo homies at USAC: https://discord.gg/2SEqk9p", tooltip="I'm too lazy to make this an actual link for now")]]

    tabs = [[sg.TabGroup([[sg.Tab("Transplant", transplant_layout),
             sg.Tab("Serial Number Swapper", serial_swapper_layout),
             sg.Tab("Characters.txt Editor", character_editor_layout),
             sg.Tab("About", about_layout)]])]]

    window = sg.Window('MiDes Brain Transplant Service'.format(version_number), tabs)

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
        if event == browsed_key:
            new_directory = values[folder_location_key]
            # changes bin list when new folder is picked
            new_found_bins = []
            for bin_file in os.listdir(new_directory):
                if bin_file[-3:] == "bin":
                    if bin_file != 'unfixed-info.bin' and bin_file != 'locked-secret.bin':
                        new_found_bins.append(bin_file[:-4])
            window[bin_name_key].update(new_found_bins)
            #window[pwd_key].set_size((len(new_directory), 1))
            window[pwd_key].update(new_directory)
            window.refresh()

        if event == sg.WIN_CLOSED:
            break

    window.close()


if __name__ == '__main__':
    main()
