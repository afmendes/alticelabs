import os


class File:
    def __init__(self, filename, filepath):
        self.filepath = filepath + "/"
        self.filename = filename

    def ensure_dir(self):
        directory = os.path.dirname(self.filepath)
        if not os.path.exists(directory):
            os.makedirs(directory)

    def exists(self):
        try:
            open(self.filepath+self.filename, "r")
        except IOError:
            return False
        else:
            return True

    def create(self, headers=""):
        self.ensure_dir()
        file = open(self.filepath+self.filename, "w")
        if headers != "":
            file.write(headers+"\n")
        file.close()

    def write(self, data, mode="a", headers=""):
        if not self.exists():
            self.create(headers)
        with open(self.filepath+self.filename, mode) as file:
            file.write(str(data) + "\n")

    def write_list(self, data, mode="a"):
        if not self.exists():
            self.create()
        with open(self.filepath+self.filename, mode) as file:
            string = ""
            for element in data:
                string += str(element) + ","
            file.write(string[:-1] + "\n")

    def read(self):
        if not self.exists():
            return "File doesn't exist"
        file = open(self.filepath+self.filename, "r")
        return file.readlines()
