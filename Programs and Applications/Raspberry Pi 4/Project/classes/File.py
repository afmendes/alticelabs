import os


# class used for debugging to save data in files
class File:
    # class initializer
    def __init__(self, filepath):
        self.filepath = filepath

    # ensures directory exists by creating it if missing
    def ensure_dir(self):
        directory = os.path.dirname(self.filepath)
        if not os.path.exists(directory):
            os.makedirs(directory)

    # returns True if file exists else returns False
    def exists(self):
        try:
            open(self.filepath, "r")
        except IOError:
            return False
        else:
            return True

    # creates a new file
    def create(self, headers=""):
        self.ensure_dir()
        file = open(self.filepath, "w")
        if headers != "":
            file.write(headers+"\n")
        file.close()

    # writes on file with append mode by default
    def write(self, data, mode="a", headers=""):
        if not self.exists():
            self.create(headers)
        with open(self.filepath, mode) as file:
            file.write(str(data) + "\n")

    # write content on list format
    def write_list(self, data, mode="a"):
        if not self.exists():
            self.create()
        with open(self.filepath, mode) as file:
            string = ""
            for element in data:
                string += str(element) + ","
            file.write(string[:-1] + "\n")

    # reads and returns file content
    def read(self):
        if not self.exists():
            return "File doesn't exist"
        file = open(self.filepath, "r")
        return file.readlines()
