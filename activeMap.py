class activeMap:
    def __init__(self):
        self.id_dict = dict()
        self.id_url_dict = dict()

    def update_maps_from_file(self, f):
        for line in f:
            if line[0] == "-":
                opt = -1
                line = line[1,:]
            else:
                opt = 1
            id = line.split("_")[0]
            self.id_dict[id] = self.id_dict.get(id, 0) + opt
            self.id_dict[line] = self.id_url_dict.get(line, 0) + opt
