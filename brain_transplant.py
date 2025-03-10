import FreeSimpleGUI as sg
from amiibo_functions import *
from character_dictionary import CharacterDictionary
import os
import requests

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
donor_browse_key = '_donor-browse_'
receiver_browse_key = '_receiver-browse_'
donor_box_key = '_donor-box_'
receiver_box_key = '_receiver-box_'
swapper_save_key = '_active-swap-save_'
swap_save_location_key = '_swap-save-location_'
display_dir1_key = '_swap_dir1_display_'
display_dir2_key = '_swap_dir2_display_'
success_swap_key = '_swap-completed_'
# Serial Shuffle
browse3_key = '_browse3_'
folder_location2_key = '_selected-folder2_'
pwd2_key = '_current-directory2_'
shuffle_save_key = '_save-shuffle_'
shuffle_save_location_key = '_shuffle-save-location_'
shuffle_name_key = '_shuffle-name_'
success_shuffle_key = '_shuffle-success_'
# Character.xml Modify Tab
add_character_key = '_add-character_'
character_edit_box_key = '_character-edit-box_'
delete_character_key = '_delete-character_'
change_enable_key = '_enable-status_'

# I know global variables are bad but I'm doing this until I work this into a class
name_formatter = {}


def no_selection_error(error_phrase):
    sg.popup("ERROR:", error_phrase)


def found_bins(directory):
    found_bins = []
    for bin_file in os.listdir(directory):
        if bin_file[-3:] == "bin":
            if bin_file != 'unfixed-info.bin' and bin_file != 'locked-secret.bin':
                # To catch powersaves dumb format
                if '[' not in bin_file:
                    found_bins.append(bin_file[:-4])
                    name_formatter[bin_file[:-4]] = bin_file
                else:
                    found_bins.append(bin_file.split('[')[1].split(']')[0])
                    name_formatter[bin_file.split('[')[1].split(']')[0]] = bin_file

    return found_bins


def update_all_listboxes(window, char_dict, directory1, directory2):
    if directory1 != "":
        updated_dir1 = found_bins(directory1)

        window[bin_name_key].update(updated_dir1)
        window[donor_box_key].update(updated_dir1)
        window[shuffle_name_key].update(updated_dir1)

    if directory2 != "":
        updated_dir2 = found_bins(directory2)
        window[receiver_box_key].update(updated_dir2)

    window[character_key].update(char_dict.get_list(insert_random=True))

    window[character_edit_box_key].update(char_dict.print_contents())

    # refresh window to show updates
    window.refresh()


def main():
    # Initialize variables that get used throughout the program
    version_number = "2.1.0"

    if not ((os.path.exists("Brain_Transplant_Assets/unfixed-info.bin") and os.path.exists("Brain_Transplant_Assets/locked-secret.bin")) or os.path.exists("Brain_Transplant_Assets/key_retail.bin")):
        no_selection_error("You are missing the encryption/decryption keys for amiibo.\nPlease place them in the Brain_Transplant_Assets Folder.")
        os._exit(0)
    if not os.path.exists("Brain_Transplant_Assets/characters.xml"):
        try:
            xml = requests.get("https://raw.githubusercontent.com/MiDe-S/amiibo_transplant/master/Brain_Transplant_Assets/characters.xml")
            with open("Brain_Transplant_Assets/characters.xml", "w+") as xml_file:
                xml_file.write(xml.text)
                xml_file.close()
        except Exception:
            no_selection_error("Something is wrong with characters.xml.\nTry deleting and reinstalling the program or just grab character.xml from the github repository.")
            os._exit(0)

    sg.theme("Dark Blue 12")

    # gets current key_directory
    directory1 = os.path.dirname(os.path.realpath(__file__))

    char_dict = CharacterDictionary()

    transplanter = BinManager(char_dict)

    # To format names to fix powersaves formatting
    located_bins1 = found_bins(directory1)

    # transplant tab
    characters = char_dict.get_list(insert_random=True)
    transplant_layout = [[sg.FolderBrowse(target=browsed_key, key=folder_location_key, enable_events=True), sg.Text("Currently looking at:"), sg.Text(directory1, key=pwd_key, auto_size_text=True)],
              [sg.Input(key=submitted_key, enable_events=True, visible=False), sg.Input(key=browsed_key, enable_events=True, visible=False)],
              [sg.Listbox(located_bins1, sg.LISTBOX_SELECT_MODE_SINGLE, size=(40, 10), key=bin_name_key), sg.VerticalSeparator(),
               sg.Listbox(characters, sg.LISTBOX_SELECT_MODE_SINGLE, size=(30, 10), key=character_key)],
              [sg.FileSaveAs("Transplant", target=submitted_key, key=save_location_key, file_types=(('Bin Files', '*.bin'),), default_extension=".bin"),
               sg.Checkbox("Randomize Serial Number", key=randomize_sn_key, enable_events=True, default=True)],
              [sg.Text(key=success_text_key, size=(10, 1), visible=False)]]

    # serial swap tab
    directory2 = directory1
    located_bins2 = found_bins(directory2)
    serial_swapper_layout = [[sg.Input(key=browse1_key, enable_events=True, visible=False), sg.Input(key=browse2_key, enable_events=True, visible=False), sg.Input(key=swapper_save_key, enable_events=True, visible=False)],
                             [sg.FolderBrowse("Donor", key=donor_browse_key, target=browse1_key, enable_events=True),
                              sg.Text(directory1, key=display_dir1_key, auto_size_text=True),
                              sg.FolderBrowse("Receiver", key=receiver_browse_key, target=browse2_key, enable_events=True),
                              sg.Text(directory2, key=display_dir2_key, auto_size_text=True)],
              [sg.Listbox(located_bins1, sg.LISTBOX_SELECT_MODE_SINGLE, key=donor_box_key, size=(40, 10)), sg.VerticalSeparator(), sg.Listbox(located_bins2, sg.LISTBOX_SELECT_MODE_SINGLE, key=receiver_box_key, size=(40, 10))],
              [sg.FileSaveAs("Transplant Figure Metadata", target=swapper_save_key, key=swap_save_location_key, file_types=(('Bin Files', '*.bin'),), default_extension=".bin")],
              [sg.Text(key=success_swap_key, size=(10, 1), visible=False)],
              [sg.Text("Donor is a bin from the figure itself, Receiver is the bin that has the training data you want to put on the figure.")],]

    # serial shuffle tab
    serial_shuffle_layout = [[sg.Input(key=browse3_key, enable_events=True, visible=False), sg.Input(key=shuffle_save_key, enable_events=True, visible=False), sg.FolderBrowse(target=browse3_key, key=folder_location2_key, enable_events=True), sg.Text("Currently looking at:"), sg.Text(directory1, key=pwd2_key, auto_size_text=True)], [sg.Listbox(located_bins1, sg.LISTBOX_SELECT_MODE_SINGLE, size=(70, 11), key=shuffle_name_key)], [sg.Text(key=success_shuffle_key, size=(10, 1), visible=False)], [sg.FileSaveAs(target=shuffle_save_key, key = shuffle_save_location_key)]]

    # character list tab
    dict_contents = char_dict.print_contents()
    character_list_editor_layout = [[sg.Listbox(dict_contents, sg.LISTBOX_SELECT_MODE_SINGLE, size=(50, 13), key=character_edit_box_key, pad=(5, 5))],
         [sg.Button("Add", key=add_character_key), sg.Button("Enable/Disable", key=change_enable_key), sg.Button("Delete", key=delete_character_key)]]

    # about tab
    about_layout = [[sg.Text("Version Number {}".format(version_number))],
                    [sg.Text("If you encounter issues raise an issue on github or dm MiDe#9934 on discord")],
                    [sg.Text("The transplant tab changes the character of the bin.")],
                    [sg.Text("The Figure Metadata transplant tab copies the SN of the donor on to the receiver.")],
                    [sg.Text("*In order to put a bin onto a figure, you have to perform the metadata transplant.")],
                    [sg.Text("*then put the transplanted bin on a powertag, save it in powersaves, THEN it will appear in the restore tab.")],
                    [sg.Text("*POWERSAVES will say the restoration failed, but it actually didn't.")],
                    [sg.Text("The Characters.xml Editor tab lets you add new amiibo ID's to the Character box.")],
                    [sg.Text("Shoutouts to the amiibo homies at USAC: https://discord.gg/2SEqk9p", tooltip="I'm too lazy to make this an actual link for now")]]

    tabs = [[sg.TabGroup([[sg.Tab("Transplant", transplant_layout),
             sg.Tab("Figure Metadata Transplant", serial_swapper_layout, element_justification='center'),
             sg.Tab('Serial Number Shuffle', serial_shuffle_layout, element_justification='center'),
             sg.Tab("Characters.xml Editor", character_list_editor_layout, element_justification='center'),
             sg.Tab("About", about_layout)]])]]

    window = sg.Window('MiDe\'s Brain Transplant Service'.format(version_number), tabs, element_justification='center')

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
                # If save as menu is closed or cancelled do nothing
                if values[save_location_key] != '':
                    chosen_character = transplanter.transplant(r"\\".join([directory1, name_formatter[bins_to_transplant[0]]]), selected_characters[0], values[save_location_key], values[randomize_sn_key])
                    if chosen_character is None:
                        no_selection_error("Not an amiibo bin")
                    else:
                        # Prints message showing a successful transplant
                        success_message = "{} bin was saved at {}".format(chosen_character, values[save_location_key])
                        window[success_text_key].update(success_message, visible=True)
                        window[success_text_key].set_size((len(success_message), 1))
                        update_all_listboxes(window, char_dict, directory1, directory2)
        elif event == browsed_key:
            directory1 = values[folder_location_key]
            if len(directory1) != 0:
                # changes bin list when new folder is picked
                update_all_listboxes(window, char_dict, directory1, directory2)
                window[pwd_key].update(directory1)
                window.refresh()
        # Serial Swap Tab
        elif event == browse1_key:
            directory1 = values[donor_browse_key]
            if len(directory1) != 0:
                # changes bin list when new folder is picked
                update_all_listboxes(window, char_dict, directory1, directory2)
                window[display_dir1_key].update(directory1)
                window.refresh()
        elif event == browse2_key:
            directory2 = values[receiver_browse_key]
            if len(directory2) != 0:
                # changes bin list when new folder is picked
                update_all_listboxes(window, char_dict, directory1, directory2)
                window[display_dir2_key].update(directory2)
                window.refresh()

        elif event == browse3_key:
            directory1 = values[folder_location2_key]
            if len(directory1) != 0:
                # changes bin list when new folder is picked
                update_all_listboxes(window, char_dict, directory1, directory2)
                window[pwd2_key].update(directory1)
                window.refresh()

        elif event == shuffle_save_key:
            if values[shuffle_save_location_key] != '':
                to_shuffle = r"\\".join([directory1, name_formatter[values[shuffle_name_key][0]]])
                name = values[shuffle_name_key][0]
                if len(to_shuffle) == 0:
                    no_selection_error("Please select bin to shuffle the serial number.") 
                else:
                    transplanter.randomize_sn(bin_location=to_shuffle, save_to_location = values[shuffle_save_location_key])
                    success_message = "{} received a new SN and was successfully saved at {}".format(name, values[shuffle_save_location_key])
                    window[success_shuffle_key].update(success_message, visible=True)
                    window[success_shuffle_key].set_size((len(success_message), 1))
                    update_all_listboxes(window, char_dict, directory1, directory2)

        elif event == swapper_save_key:
            # If save as menu is closed or cancelled do nothing
            if values[swap_save_location_key] != '':
                donor_bin = r"\\".join([directory1, name_formatter[values[donor_box_key][0]]])
                receiver_bin = r"\\".join([directory2, name_formatter[values[receiver_box_key][0]]])
                if len(donor_bin) == 0 or len(receiver_bin) == 0:
                    no_selection_error("Please select a donor and a receiver to transplant a serial number.")
                else:
                    success_check = transplanter.serial_swapper(donor_bin, receiver_bin, values[swap_save_location_key])
                    if success_check is None:
                        no_selection_error("Not an amiibo bin")
                    else:
                        success_message = "{} received a new SN and was successfully saved at {}".format(receiver_bin, values[swap_save_location_key])
                        window[success_swap_key].update(success_message, visible=True)
                        window[success_swap_key].set_size((len(success_message), 1))
                        update_all_listboxes(window, char_dict, directory1, directory2)

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
                        update_all_listboxes(window, char_dict, directory1, directory2)
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
                update_all_listboxes(window, char_dict, directory1, directory2)

        # Window Closed
        elif event == sg.WIN_CLOSED:
            break

    window.close()


if __name__ == '__main__':
    main()
