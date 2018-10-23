class Reader:
    def __init__(self, filename):
        self.filename = filename
        self.f = None
        try:
            self.f = open(self.filename, 'rt')
        except FileNotFoundError as err:
            print("Could not locate" + self.filename + ". Ensure that it exists.")

    def close(self):
        if self.f is not None:
            self.f.close()

    def read(self):
        lines = []
        if self.f is not None:
            try:
                lines = self.f.readlines()
                #lines = self.remove_empty_lines_from_list(lines)
            except IOError as err:
                print("Could read from " + self.filename + ".")
                print("Ensure that it exists and is not opened by other programs.")
        return lines

    def print_content(self):
        lines = self.read()

        for line in lines:
            print(line)
        self.close()

    def remove_empty_lines_from_list(self, source_list):
        target_list = []
        for item in source_list:
            item = item.replace("\n", "")
            if item is not None and len(item) > 0:
                target_list.append(item)
        return target_list
