from amiibo_functions import *
from transplant_functions import *
import os

def main():
    #gets current key_directory
    directory = os.path.dirname(os.path.realpath(__file__))

    print('''---------------------------------------------------------------------------------
    | Welcome to release 1.0.2 of MiDe's Brain Transplant Service,                  |
    | Make sure to check out the README.txt in the Brain_Transplant_Assets folder! |
    |                                                                               |
    | Using Mii Fighters with this program will not work. PLEASE DON'T USE THEM!!!  |
    ---------------------------------------------------------------------------------
    ''')

    char_dict = create_character_dict(directory)

    Transplanter = BinManager(char_dict)

    # central loop for detecting bins, picking new character, and saving
    do_again = 'y'
    while do_again.lower() == 'y':
        found_bins = []
        for bin_file in os.listdir(directory):
            if bin_file[-3:] == "bin":
                if bin_file != 'unfixed-info.bin' and bin_file != 'locked-secret.bin':
                    found_bins.append(bin_file[:-4])

        # for printing out found bins
        print("Detected Bins:")
        print_bins(found_bins)
        print('''Or type "All" to select all bins. (make sure to make backups!)''')

        # asks user to pick a bin
        name_error = True
        while name_error:
            selected_bin = input("Enter bin name EXACTLY as it appears: ")
            if selected_bin == "All":
                name_error = False
                character = character_selector(char_dict)
                print('-' * 50) # for spacing
                for bin_file in os.listdir(directory):
                    if bin_file[-3:] == "bin":
                        if bin_file != 'unfixed-info.bin' and bin_file != 'locked-secret.bin':
                            Transplanter.transplant(bin_file[:-4], character)
            elif selected_bin in found_bins:
                name_error = False
                character = character_selector(char_dict)
                Transplanter.transplant(selected_bin, character)
            else:
                print("ERROR: Name not found, please try again")
        print('-' * 50)
        do_again = input('Transplant successful, Do you want to do another one? (y/n) ')
    # not required but I like to do it
    # fp_d.close()
    # fp_t.close()
    print('-' * 50)
    input('''Thank you for using amiibo brain transplant!
    Press any button to close.''')

if __name__ == '__main__':
    main()