<h1>
NOTICE:
</h1>

<p>
    All features of brain transplant service are now present in <a href="https://github.com/jozz024/smash-amiibo-editor">SAE.</a> Please use SAE instead, this project is now considered deprecated.
</p>

<h1>
  MiDe's Brain Transplanting Service
</h1>

<p>
  This is a tool for changing the characters of amiibo bin files. The amiibo community has dubbed this as a "brain transplant" as it lets you view what you're training would look like on other characters.
</p>

<h2>
  Important Information
</h2>

<p>
  In order for this program to work you need two amiibo encryption keys. They are not supplied with this program but "unfixed-info" and "locked-secret" are easily found with some searching.
  Once you have them place them in the Brain_Transplant_Assests Folder.
</p>


<h2>
  FAQ
</h2>

<p>
  <b>Q:</b> What can I do with this tool <br />
  A: Using this tool it is possible to:
  - Convert any bin into any character*
  - Perform a metadata transplant so you can put bins onto figures
  *any character listed in characters.xml
  <hr />
  <b>Q:</b> How do I find the hex_character_id of a character not on the list, but I have a bin of that character? <br />
  A: Add it yourself by opening the amiibo in a hex editor (i like https://hexed.it/) and locate it yourself. On the 6th row (row 5 if you include 0), it is the middle 8 bytes. It will ALWAYS end in 02. (02 is one byte)
  <hr />
  <b>Q:</b> Why do mii fighters not work? <br />
  A: Mii fighters hold special data for the mii of the character. If a mii fighter bin is scanned into ultimate without any data for a mii it crashes the game.
  <hr />
</p>

<p>
  pyinstaller -wF -i logo.ico brain_transplant.py  
</p>

<p>
  Need help? <a href="https://mide-s.github.io/amiibo/">Contact me</a> on discord @MiDe#9934. 
</p>
