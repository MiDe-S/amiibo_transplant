import xml.etree.ElementTree as xml
from random import choice

default_assets_location = r"Brain_Transplant_Assets/characters.xml"


class CharacterDictionary:
    def __init__(self, file_directory=default_assets_location):
        """
        Initializes the character dictionary

        :param file_directory: location of characters.xml
        """
        self.dict = {}

        self.directory = file_directory

        self.update_characters(file_directory)

    def __getitem__(self, item):
        """
        Returns the hex_id of the given item

        :param item: character to index dictionary for
        :return: string of given character's hex_id
        """
        if item == "Random":
            return self.dict[choice(self.get_list(False))][0]
        return self.dict[item][0]

    def update_characters(self, file_location=default_assets_location):
        """
        Reads and updates the character dictionary

        :param file_location:
        :return:
        """
        tree = xml.parse(file_location)
        root = tree.getroot()
        for child in root:
            self.dict[child[0].text] = (child[1].text, child.attrib["enabled"])

    def keys(self):
        """
        Gives the keys of the dictionary

        :return: keys of the dictionary
        """
        return self.dict.keys()

    def get_list(self, insert_random):
        """
        Returns list of characters in the dictionary

        :param insert_random: If true, random is inserted at the end
        :return: list of characters in the dictionary
        """
        output = []
        for key in self.dict:
            if self.dict[key][1] == "True":
                output.append(key)
        if insert_random:
            output.append("Random")
        return output

    def enable(self, character):
        """
        Flips the enabled status of the given character

        :param character: character to flip status of
        :return: None
        """
        if self.dict[character][1] == "True":
            self.dict[character] = (self.dict[character][0], "False")
        else:
            self.dict[character] = (self.dict[character][0], "True")

    def add_character(self, character, hex_id, enabled):
        """
        Adds a character to the dictionary

        :param character: character to be added
        :param hex_id: ID of added character
        :param enabled: enabled status of given character
        :return: None
        """
        self.dict[character] = (hex_id, str(enabled))

    def remove_character(self, character):
        """
        deletes given character from xml

        :param character: character to delete
        :return: None
        """
        del self.dict[character]

    def save_XML(self):
        """
        Saves current dictionary as the new characters.xml

        :return: None
        """
        root = xml.Element("Characters")

        for key in self.dict:
            node = xml.Element("Character")
            root.append(node)
            node.attrib = {'enabled': self.dict[key][1]}

            c_child = xml.SubElement(node, "Name")
            c_child.text = key

            child = xml.SubElement(node, "Hex_Identifier")
            child.text = self.dict[key][0]

        tree = xml.ElementTree(root)

        with open(self.directory, "wb") as files:
            tree.write(files)

    def print_contents(self):
        """
        Returns the contents of the dictionary

        :return: Gives the contents of the dictionary as a list of strings
        """
        output = []
        for key in self.dict:
            output.append("{}, {}, enabled={}".format(key, self.dict[key][0], self.dict[key][1]))
        return output