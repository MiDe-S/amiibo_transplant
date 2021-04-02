import PySimpleGUI as sg
from amiibo_functions import *
from character_dictionary import CharacterDictionary
import os

# Menu key variables for GUI
# Transplant Tab
character_key = '_character_'
save_location_key = '_save_location_'
submitted_key = '_transplant-submission_'
bin_name_key = '_bin-name_'
success_text_key = '_transplant-success_'
randomize_sn_key = '_randomize-sn_'
folder_location_key = '_selected-folder_'
browsed_key = '_browse-submission_'
pwd_key = '_current-directory_'
# Serial Swapper Tab
browse1_key = '_browse1_'
browse2_key = '_browse2_'
# Character.xml Modify Tab
add_character_key = '_add-character_'
character_edit_box_key = '_character-edit-box_'
delete_character_key = '_delete-character_'
change_enable_key = '_enable-status_'

def no_selection_error(error_phrase):
    sg.popup("ERROR:", error_phrase)

def found_bins(directory):
    found_bins = []
    for bin_file in os.listdir(directory):
        if bin_file[-3:] == "bin":
            if bin_file != 'unfixed-info.bin' and bin_file != 'locked-secret.bin':
                found_bins.append(bin_file[:-4])
    return found_bins


def update_all_listboxes(window, char_dict, directory):
    window[bin_name_key].update(found_bins(directory))
    window[character_key].update(char_dict.get_list(insert_random=True))
    window[character_edit_box_key].update(char_dict.print_contents())
    # refresh window to show updates
    window.refresh()


def main():
    # Initialize variables that get used throughout the program
    version_number = "2.0.0"

    # gets current key_directory
    directory = os.path.dirname(os.path.realpath(__file__))

    char_dict = CharacterDictionary()

    transplanter = BinManager(char_dict)

    located_bins = found_bins(directory)

    # transplant tab
    characters = char_dict.get_list(insert_random=True)
    transplant_layout = [[sg.FolderBrowse(target=browsed_key, key=folder_location_key, enable_events=True), sg.Text("Currently looking at:"), sg.Text(directory, key=pwd_key, auto_size_text=True)],
              [sg.Input(key=submitted_key, enable_events=True, visible=False), sg.Input(key=browsed_key, enable_events=True, visible=False)],
              [sg.Listbox(located_bins, sg.LISTBOX_SELECT_MODE_SINGLE, size=(40, 10), key=bin_name_key), sg.VerticalSeparator(),
               sg.Listbox(characters, sg.LISTBOX_SELECT_MODE_SINGLE, size=(30, 10), key=character_key)],
              [sg.FileSaveAs("Transplant", target=submitted_key, key=save_location_key, file_types=(('Bin Files', '*.bin'),), default_extension=".bin", initial_folder=directory),
               sg.Checkbox("Randomize Serial Number", key=randomize_sn_key, enable_events=True, default=True)],
              [sg.Text(key=success_text_key, size=(10, 1), visible=False)]]

    # serial swap tab
    serial_swapper_layout = [[sg.Input(key=browse1_key, enable_events=True, visible=False), sg.Input(key=browse2_key, enable_events=True, visible=False)],
                             [sg.FolderBrowse("Donor", target=browse1_key, enable_events=True),
                              sg.Text(directory, auto_size_text=True),
                              sg.FolderBrowse("Receiver", target=browse2_key, enable_events=True),
                              sg.Text(directory, auto_size_text=True)],
              [sg.Listbox(located_bins, sg.LISTBOX_SELECT_MODE_SINGLE, size=(40, 10)), sg.VerticalSeparator(), sg.Listbox(located_bins, sg.LISTBOX_SELECT_MODE_SINGLE, size=(40, 10))],
              [sg.FileSaveAs("Swap Serial Numbers", file_types=(('Bin Files', '*.bin'),), default_extension=".bin", initial_folder=directory)],
              [sg.Text(size=(10, 1), visible=False)]]

    # character list tab
    dict_contents = char_dict.print_contents()
    character_list_editor_layout = [[sg.Listbox(dict_contents, sg.LISTBOX_SELECT_MODE_SINGLE, size=(50, 15), key=character_edit_box_key, pad=(5, 5))],
         [sg.Button("Add", key=add_character_key), sg.Button("Enable/Disable", key=change_enable_key), sg.Button("Delete", key=delete_character_key)]]

    # about tab
    about_layout = [[sg.Text("Version Number {}".format(version_number))],
                    [sg.Text("If you encounter issues raise an issue on github or dm MiDe#9934 on discord")],
                    [sg.Text("Shoutouts to the amiibo homies at USAC: https://discord.gg/2SEqk9p", tooltip="I'm too lazy to make this an actual link for now")]]

    tabs = [[sg.TabGroup([[sg.Tab("Transplant", transplant_layout),
             sg.Tab("Serial Number Swapper", serial_swapper_layout),
             sg.Tab("Characters.txt Editor", character_list_editor_layout),
             sg.Tab("About", about_layout)]])]]

    window = sg.Window('MiDes Brain Transplant Service'.format(version_number), tabs)


    while True:
        event, values = window.read()
        print(event, values)
        # Transplant Tab
        if event == submitted_key:
            bins_to_transplant = values[bin_name_key]
            selected_characters = values[character_key]
            # If an option wasn't selected
            if len(selected_characters) == 0 or len(bins_to_transplant) == 0:
                no_selection_error("Please a bin and a character to transplant.")
            # If only 1 character and 1 bin were chosen do the single transplant
            elif len(selected_characters) == 1 and len(bins_to_transplant) == 1:
                chosen_character = transplanter.transplant(bins_to_transplant[0], selected_characters[0], values[save_location_key])
                # Prints message showing a successful transplant
                if values[randomize_sn_key]:
                    success_message = "{} bin was saved at {}".format(chosen_character, values[save_location_key], randomize_sn=True)
                else:
                    success_message = "{} bin was saved at {}".format(chosen_character, values[save_location_key], randomize_sn=False)
                window[success_text_key].update(success_message, visible=True)
                window[success_text_key].set_size((len(success_message), 1))
                update_all_listboxes(window, char_dict, directory)
        elif event == browsed_key:
            directory = values[folder_location_key]
            # changes bin list when new folder is picked
            update_all_listboxes(window, char_dict, directory)
            window[pwd_key].update(directory)
            window.refresh()
        # Serial Swap Tab
        # Character Dictionary Tab
        # Add Character
        elif event == add_character_key:
            # Addition menu
            add_name_key = "_name_"
            add_ID_key = "_id_"
            add_enable_key = "_enable_"
            add_cancel_key = "_cancel_"
            add_confirm_key = "_confirm_"

            add_layout = [[sg.InputText(key=add_name_key)],
                          [sg.InputText(key=add_ID_key)],
                          [sg.Checkbox("Enabled", key=add_enable_key, default=True)],
                          [sg.Submit("Confirm", key=add_confirm_key), sg.Cancel(key=add_cancel_key)]]
            add_window = sg.Window("Add a character", add_layout)
            while True:
                event, values = add_window.read()
                print(event, values)
                # Add character confirmation
                if event == add_confirm_key:
                    if len(values[add_ID_key]) == 16:
                        char_dict.add_character(values[add_name_key], values[add_ID_key], values[add_enable_key])
                        char_dict.save_XML()
                        update_all_listboxes(window, char_dict, directory)
                        break
                    else:
                        sg.Popup("Invalid Length!", "Amiibo character IDs are always 16 characters long", "Try Again!")

                # Window Closed
                elif event == sg.WIN_CLOSED or event == add_cancel_key or event == "Quit":
                    break
            add_window.close()
        # Remove / enable or disable character
        elif event == delete_character_key or event == change_enable_key:
            if len(values[character_edit_box_key]) == 0:
                no_selection_error("Please select a character to delete.")
            else:
                # This long expression grabs the character name
                character = values[character_edit_box_key][0].split(',')[0]
                if event == delete_character_key:
                    char_dict.remove_character(character)
                else:
                    char_dict.enable(character)
                char_dict.save_XML()
                update_all_listboxes(window, char_dict, directory)

        # Window Closed
        elif event == sg.WIN_CLOSED:
            break

    window.close()


if __name__ == '__main__':
    main()
