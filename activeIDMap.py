from datetime import datetime, timedelta

class activeIDMap:
    def __init__(self):
        self.id_dict = dict()
        self.id_category_dict = dict()
        self.id_domain_dict = dict()

    def __init__(self, path, classifier):
        self.id_dict = dict()
        self.id_category_dict = dict()
        self.id_domain_dict = dict()

        with open(path) as f:
            for line in f:
                linelist = line.split("\t")
                value = (int(linelist[2]),int(linelist[3]),int(linelist[4]))
                append_create(linelist[0], value, self.id_dict)
                append_create(linelist[0] + "_" + classifier.get_category(linelist[1]), value, self.id_category_dict)
                append_create(linelist[0] + "_" + linelist[1], value, self.id_domain_dict)

    def get_id_n(self, id, ss2k):
        return get_n(id, ss2k, self.id_dict)

    def get_id_domain_n(self, id, domain, ss2k):
        return get_n(id+"_"+domain, ss2k, self.id_domain_dict)

    def get_id_category_n(self, id, domain, ss2k, classifier):
        return get_n(id + "_" + classifier.get_category(domain), ss2k, self.id_category_dict)

    def is_active_id(self, id):
        return id in self.id_dict

def get_n(key, ss2k, dict):
    this_month_n = 0;
    next_month_n = 0;

    t = ss2k_to_int_time(ss2k)
    if key in dict:
        for i in dict[key]:
            if t >= i[0] and t <= i[1]:
                month = t/1000000
                if month == i[2]:
                    this_month_n += 1
                else:
                    next_month_n += 1
    return this_month_n, next_month_n


def append_create(key, value, dict):
    if key in dict.keys():
        dict[key].append(value)
    else:
        dict[key] = [value]

def ss2k_to_int_time(ss2k):
    return int(datetime.strftime(datetime(1999, 12, 31, 00, 00) + timedelta(seconds=int(ss2k)),"%Y%m%d%H%M%S"))