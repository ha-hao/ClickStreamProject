from datetime import datetime, timedelta

class activeMap:
    def __init__(self):
        self.id_dict = dict()
        self.id_url_dict = dict()

    def update_maps_from_file(self, path):
        self.id_dict = dict()
        self.id_url_dict = dict()
        with open(path) as f:
            for line in f:
                linelist = line.split("\t")
                if linelist[0] in self.id_dict.keys():
                    self.id_dict[linelist[0]].append((int(linelist[2]),int(linelist[3])))
                else:
                    self.id_dict[linelist[0]] = [(int(linelist[2]),int(linelist[3]))]

                composite_key = "_".join([linelist[0],linelist[1]])
                if composite_key in self.id_url_dict.keys():
                    self.id_url_dict[composite_key].append((int(linelist[2]),int(linelist[3])))
                else:
                    self.id_url_dict[composite_key] = [(int(linelist[2]),int(linelist[3]))]

    def get_id_n(self, key, ss2k):
        n = 0
        if key in self.id_dict:
            for i in self.id_dict[key]:
                t = ss2k_to_int_time(ss2k)
                if t > self.id_dict[key][0] and t < self.id_dict[key][1]:
                    n += 1
        return n

    def get_url_id_n(self, key, ss2k):
        n = 0
        if key in self.id_url_dict:
            for i in self.id_url_dict[key]:
                t = ss2k_to_int_time(ss2k)
                if t > self.id_url_dict[key][0] and t < self.id_url_dict[key][1]:
                    n += 1
        return n

    def is_active_id(self, id):
        return id in self.id_dict

    # def update_maps_from_file(self, f):
    #     for line in f:
    #
    #         if line[0] == "-":
    #             opt = -1
    #             line = line[1:]
    #         else:
    #             opt = 1
    #         id = line.split("_")[0]
    #         self.id_dict[id] = self.id_dict.get(id, 0) + opt
    #         self.id_dict[line] = self.id_url_dict.get(line, 0) + opt
    #
    # def getIDNum(self, id):
    #     return self.id_dict.get(id,0)
    #
    # def getID_URLNum(self, id, url):
    #     return self.id_dict.get(id+"_"+url,0)

def ss2k_to_int_time(ss2k):
    return int(datetime.strftime(datetime.datetime(1999, 12, 31, 00, 00) + timedelta(seconds=int(ss2k)),"%h%M%S"))