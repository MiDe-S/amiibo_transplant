import PySimpleGUI as sg
from amiibo_functions import *
from character_dictionary import CharacterDictionary
from gui_manager import ListBoxManager
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
donor_browse_key = '_donor-browse_'
receiver_browse_key = '_receiver-browse_'
donor_box_key = '_donor-box_'
receiver_box_key = '_receiver-box_'
swapper_save_key = '_active-swap-save_'
swap_save_location_key = '_swap-save-location_'
display_dir1_key = '_swap_dir1_display_'
display_dir2_key = '_swap_dir2_display_'
success_swap_key = '_swap-completed_'
# Character.xml Modify Tab
add_character_key = '_add-character_'
character_edit_box_key = '_character-edit-box_'
delete_character_key = '_delete-character_'
change_enable_key = '_enable-status_'


def no_selection_error(error_phrase):
    sg.popup("ERROR:", error_phrase)


def main():
    # Initialize variables that get used throughout the program
    version_number = "2.0.1"

    if not os.path.exists("Brain_Transplant_Assets/unfixed-info.bin") or not os.path.exists("Brain_Transplant_Assets/locked-secret.bin"):
        no_selection_error("You are missing the encryption/decryption keys for amiibo.\nThey are named unfixed-info.bin and locked-secret.bin.\nPlease place them in the Brain_Transplant_Assets Folder.")
        exit()
    if not os.path.exists("Brain_Transplant_Assets/characters.xml"):
        no_selection_error("Something is wrong with characters.xml.\nTry deleting and reinstalling the program or just grab character.xml from the github repository.")
        exit()

    sg.theme("Dark Blue 12")

    list_manager = ListBoxManager()

    # gets current key_directory
    directory1 = os.path.dirname(os.path.realpath(__file__))

    char_dict = CharacterDictionary()

    list_manager.add_list_box(character_key, char_dict.get_list(insert_random=True))
    transplanter = BinManager(char_dict)

    # To format names to fix powersaves formatting
    list_manager.add_dir_box([bin_name_key, donor_box_key], directory1)

    # transplant tab
    transplant_layout = [[sg.FolderBrowse(target=browsed_key, key=folder_location_key, enable_events=True), sg.Text("Currently looking at:"), sg.Text(directory1, key=pwd_key, auto_size_text=True)],
              [sg.Input(key=submitted_key, enable_events=True, visible=False), sg.Input(key=browsed_key, enable_events=True, visible=False)],
              [sg.Listbox(list_manager[bin_name_key], sg.LISTBOX_SELECT_MODE_SINGLE, size=(40, 10), key=bin_name_key), sg.VerticalSeparator(),
               sg.Listbox(list_manager[character_key], sg.LISTBOX_SELECT_MODE_SINGLE, size=(30, 10), key=character_key)],
              [sg.FileSaveAs("Transplant", target=submitted_key, key=save_location_key, file_types=(('Bin Files', '*.bin'),), default_extension=".bin"),
               sg.Checkbox("Randomize Serial Number", key=randomize_sn_key, enable_events=True, default=True)],
              [sg.Text(key=success_text_key, size=(10, 1), visible=False)]]

    # serial swap tab
    directory2 = directory1
    list_manager.add_dir_box([receiver_box_key], directory2)
    serial_swapper_layout = [[sg.Input(key=browse1_key, enable_events=True, visible=False), sg.Input(key=browse2_key, enable_events=True, visible=False), sg.Input(key=swapper_save_key, enable_events=True, visible=False)],
                             [sg.FolderBrowse("Donor", key=donor_browse_key, target=browse1_key, enable_events=True),
                              sg.Text(directory1, key=display_dir1_key, auto_size_text=True),
                              sg.FolderBrowse("Receiver", key=receiver_browse_key, target=browse2_key, enable_events=True),
                              sg.Text(directory2, key=display_dir2_key, auto_size_text=True)],
              [sg.Listbox(list_manager[donor_box_key], sg.LISTBOX_SELECT_MODE_SINGLE, key=donor_box_key, size=(40, 10)), sg.VerticalSeparator(), sg.Listbox(list_manager[receiver_box_key], sg.LISTBOX_SELECT_MODE_SINGLE, key=receiver_box_key, size=(40, 10))],
              [sg.FileSaveAs("Transplant Figure Metadata", target=swapper_save_key, key=swap_save_location_key, file_types=(('Bin Files', '*.bin'),), default_extension=".bin")],
              [sg.Text(key=success_swap_key, size=(10, 1), visible=False)],
              [sg.Text("Donor is a bin from the figure itself, Receiver is the bin that has the training data you want to put on the figure.")],]

    # character list tab
    list_manager.add_list_box(character_edit_box_key, char_dict.print_contents())
    character_list_editor_layout = [[sg.Listbox(list_manager[character_edit_box_key], sg.LISTBOX_SELECT_MODE_SINGLE, size=(50, 13), key=character_edit_box_key, pad=(5, 5))],
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
                    chosen_character = transplanter.transplant(r"\\".join([directory1, list_manager.name_format(bins_to_transplant[0])]), selected_characters[0], values[save_location_key], values[randomize_sn_key])
                    if chosen_character is None:
                        no_selection_error("Not an amiibo bin")
                    else:
                        # Prints message showing a successful transplant
                        success_message = "{} bin was saved at {}".format(chosen_character, values[save_location_key])
                        window[success_text_key].update(success_message, visible=True)
                        window[success_text_key].set_size((len(success_message), 1))
                        list_manager.update_dir_box(window, [bin_name_key, donor_box_key], directory1)
                        list_manager.update_dir_box(window, [receiver_box_key], directory2)
        elif event == browsed_key:
            directory1 = values[folder_location_key]
            if len(directory1) != 0:
                window[pwd_key].update(directory1)
                # changes bin list when new folder is picked
                list_manager.update_dir_box(window, [bin_name_key, donor_box_key], directory1)

        # Serial Swap Tab
        elif event == browse1_key:
            directory1 = values[donor_browse_key]
            if len(directory1) != 0:
                window[display_dir1_key].update(directory1)
                # changes bin list when new folder is picked
                list_manager.update_dir_box(window, [bin_name_key, donor_box_key], directory1)
        elif event == browse2_key:
            directory2 = values[receiver_browse_key]
            if len(directory2) != 0:
                window[display_dir2_key].update(directory2)
                # changes bin list when new folder is picked
                list_manager.update_dir_box(window, [receiver_box_key], directory2)

        elif event == swapper_save_key:
            # If save as menu is closed or cancelled do nothing
            if values[swap_save_location_key] != '':
                donor_bin = r"\\".join([directory1, list_manager.name_format(values[donor_box_key][0])])
                receiver_bin = r"\\".join([directory2, list_manager.name_format(values[receiver_box_key][0])])
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
                        list_manager.update_dir_box(window, [receiver_box_key], directory2)
                        list_manager.update_dir_box(window, [bin_name_key, donor_box_key], directory1)

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
                        list_manager.update_list_box(window, character_key, char_dict.get_list(insert_random=True))
                        list_manager.update_list_box(window, character_edit_box_key, char_dict.print_contents())
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
                list_manager.update_list_box(window, character_edit_box_key, char_dict.print_contents())
                list_manager.update_list_box(window, character_key, char_dict.get_list(insert_random=True))


        # Window Closed
        elif event == sg.WIN_CLOSED:
            break

    window.close()


if __name__ == '__main__':
    main()
