README 2.0.0

ACTUAL IMPORTANT THINGS:
------------------------------------------------------------------------------
In order for this program to work you need two amiibo encryption keys.
I can't help you find locked-secret.bin and unfixed-info.bin, but I can tell you these are the same keys used with Tagmo. Hopefully google can be helpful enough for you to find them on your own.
Once you have them place them in the Brain_Transplant_Assests Folder.
------------------------------------------------------------------------------



FAQ:
------------------------------------------------------------------------------
Q: What can I do with this tool
A: Using this tool it is possible to:
- Convert any bin into any character*
- Perform a metadata transplant so you can put bins onto figures
*any character listed in characters.xml
------------------------------------------------------------------------------
Q: How do I find the hex_character_id of a character not on the list, but I have a bin of that character?
A: Add it yourself by opening the amiibo in a hex editor (i like https://hexed.it/) and locate it yourself. On the 6th row (row 5 if you include 0), it is the middle 8 bytes. It will ALWAYS end in 02. (02 is one byte)
------------------------------------------------------------------------------
Q: Why do mii fighters not work?
A: Mii fighters hold special data for the mii of the character. If a mii fighter bin is scanned into ultimate without any data for a mii it crashes the game.