README 1.0.2
Hello friends, please follow these simple guidelines to make sure everything will run smoothly:

ACTUAL IMPORTANT THINGS:
------------------------------------------------------------------------------
PLEASE back up bins before using this program
------------------------------------------------------------------------------
Any bins you want to manipulate with this tool should be in the SAME FOLDER AS brain_transplant.exe (but outside of the assests folder)
------------------------------------------------------------------------------
In order for this program to work you need two amiibo encryption keys.
I can't help you find locked-secret.bin and unfixed-info.bin, but I can tell you these are the same keys used with Tagmo. Hopefully google can be helpful enough for you to find them on your own.
Once you have them place them in the Brain_Transplant_Assests Folder.
------------------------------------------------------------------------------
BINS HAVE TO BE 540 BYTES EXACTLY
you can change bin size by opening up the bin in a hex editor (i like https://hexed.it/) and adding/removing bytes. (to add bytes, right click at the end and add however many you need to reach 540) (to remove bytes, select the end and remove 00 bytes until you have 540 only)
------------------------------------------------------------------------------

That was all the super important stuff, other helpful info is in the FAQ though!

FAQ:
------------------------------------------------------------------------------
Q: What can I do with this tool
A: Using this tool it is possible to:
- Randomize every bin or just 1 bin to any character*
- Convert any single bin into any character*
- Convert every bin into any character*
- Convert any bin into every character**
*any character listed in characters.txt
**you can also technically try to Convert every bin into every character in one go but it won't work well
------------------------------------------------------------------------------
Q: How can I limit the random pool to just B through F tier amiibo?
A: Just put an @ symbol in front of all the amiibo you want to disapear from the random pool in characters.txt
------------------------------------------------------------------------------
Q: How random is the randomness?
A: It is pretty random, anything that looks non-random is probably just trying to find a pattern where patterns don't exist
------------------------------------------------------------------------------
Q: How do I add characters to characters.txt?
A: Format them like this:
Mario,0000000000000002
The name isn't important, just the second part, which I call the hex_character_id, has to be exactly right or else the game won't accept the amiibo.
------------------------------------------------------------------------------
Q: How do I find the hex_character_id of a character not on the list, but I have a bin of that character?
A: Add it yourself by opening the amiibo in a hex editor (i like https://hexed.it/) and locate it yourself. On the 6th row (row 5 if you include 0), it is the middle 8 bytes. It will ALWAYS end in 02. (02 is one byte)
------------------------------------------------------------------------------
Q: Can I put these bins on amiibos or NTAG215s?
A: These bins will only work with Powertags or NTAG215s that haven't been written to yet.
------------------------------------------------------------------------------
Q: Why do mii fighters not work?
A: Mii fighters hold special data for the mii of the character. If a mii fighter bin is scanned into ultimate without any data for a mii it crashes the game.