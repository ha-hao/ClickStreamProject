
class demographicsMap:

    def __init__(self):
        self.current_demo_map = dict()
        self.next_demo_map = dict()

    def update_demographics_map_from_file(self, path1, path2):
        self.current_demo_map = dict()
        with open(path1) as f:
            for line in f:
                linelist = line.split("\t")
                self.current_demo_map[linelist[1].strip()] = linelist[2:-2]
        f.close()

        with open(path2) as f:
            for line in f:
                linelist = line.split("\t")
                self.current_demo_map[linelist[1].strip()] = linelist[2:-2]
        f.close()

    def get_demographics(self, id):

        error = 0

        if id in self.current_demo_map.keys():
            output1 = self.current_demo_map[id]
        else:
            output1 = ["0"] * 8
            error += 1

        if id in self.next_demo_map.keys():
            output2 = self.next_demo_map[id]
        else:
            output2 = ["0"] * 8
            error += 1

        if error == 2 : print "not exist this id in demo map"
        return output1, output2