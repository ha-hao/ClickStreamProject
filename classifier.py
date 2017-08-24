import os

class classifier:
    def __init__(self):
        self.checkoutDict = dict()
        self.couponSet = set()
        self.reviewSet = set()
        self.socialMediaSet = set()
        self.product_keyword_dict = dict()

    def __init__(self, path):
        self.checkoutDict = dict()
        self.couponSet = set()
        self.reviewSet = set()
        self.socialMediaSet = set()
        self.product_keyword_dict = dict()

        self.add_categories_from_folder(os.path.join(path, "DividedSiteToken"))
        with open(os.path.join(path, "coupon.txt")) as f:
            self.add_coupon_from_file(f)
        f.close()

        with open(os.path.join(path, "ReviewSiteDomain.txt")) as f:
            self.add_review_from_file(f)
        f.close()

        with open(os.path.join(path, "SocialMediaDomain.txt")) as f:
            self.add_socialmedia_from_file(f)
        f.close()



    def add_categories_from_folder(self, path):
        for filename in os.listdir(path):

            with open(os.path.join(path, filename), "r") as f:
                category = os.path.basename(f.name)[:-9]
                for line in f:
                    key = line.split("\t")[0].lower()
                    value = line.split("\t")[1].lower(),line.split("\t")[2].lower(),category
                    self.checkoutDict[key] = value
            f.close()

    def add_product_keys(self, path):
        for filename in os.listdir(path):
            with open(os.path.join(path, filename), "r") as f:
                category = os.path.basename(f.name)[:-4]
                for line in f:
                    key = line.split("\t")[0].rstrip().lower()
                    value = line.split("\t")[1].rstrip().lower(),line.split("\t")[2].rstrip().lower(),category
                    self.checkoutDict[key] = value
        f.close()

    def add_coupon_from_file(self, f):
        for line in f:
            if "\t" in line:
                line = line.split("\t")[0]
            if line[0] == ".":
                line = line[1:]
            self.couponSet.add(line.rstrip().lower())


    def add_review_from_file(self, f):
        for line in f:
            if line[0] == ".":
                line = line[1:]
            self.reviewSet.add(line.rstrip().lower())

    def add_socialmedia_from_file(self, f):
        for line in f:
            if line[0] == ".":
                line = line[1:]
            self.socialMediaSet.add(line.rstrip().lower())

    def in_target_site(self, domain):
        return domain in self.checkoutDict

    def in_relevant_site(self, domain):
        return (domain in self.checkoutDict or domain in self.reviewSet or domain in self. socialMediaSet or
            domain in self.couponSet)

    def get_category(self, domain):
        return self.checkoutDict[domain][2]

    def get_category_vector(self, domain,subdomain, url):
        output = [0] * 6
        if domain in self.couponSet:
            output[3] = 1
        elif domain in self.reviewSet:
            output[4] = 1
        elif domain in self.socialMediaSet:
            output[5] = 1
        elif self.checkout_match(domain, subdomain, url):
            output[0] = 1
            output[1] = 1
        elif self.product_match(domain, subdomain, url):
            output[0] = 1
            output[2] = 1
        else:
            output[0] = 1
        return output

    def checkout_match(self, domain, subdomain, url):
        if self.in_target_site(domain):
            key = self.checkoutDict[domain][1]
            if key == url:
                return True
            if key == subdomain:
                return True
            if ("/" in subdomain):
                for i in subdomain.split():
                    if i == "checkout" or i == key:
                        return True
            if ("/" in url):
                for i in subdomain.split():
                    if i == "checkout" or i == key:
                        return True
            return False
        else:
            return False

    def product_match(self, domain, subdomain, url):
        if self.in_target_site(domain):
            key = self.checkoutDict[domain][0]
            if key == url:
                return True
            if key == subdomain:
                return True
            if ("/" in subdomain):
                for i in subdomain.split():
                    if i == "product" or i == key:
                        return True
            if ("/" in url):
                for i in subdomain.split():
                    if i == "product" or i == key:
                        return True
            return False
        else:
            return False




