import os
# install tldextract


class classifier:
    def __init__(self):
        self.checkoutDict = dict()
        self.couponSet = set()
        self.reviewSet = set()
        self.socialMediaSet = set()

    def __init__(self, path):
        self.checkoutDict = dict()
        self.couponSet = set()
        self.reviewSet = set()
        self.socialMediaSet = set()

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
            f = open(os.path.join(path, filename), "r")
            with open(os.path.join(path, filename), "r") as f:
                self.add_category_from_file(f)
            f.close()

    def add_category_from_file(self, f):
        category = os.path.basename(f.name)[:-9]
        for line in f:
            key = line.split("\t")[0]
            value = line.split("\t")[1],line.split("\t")[2],category
            self.checkoutDict[key] = value

    def add_coupon_from_file(self, f):
        for line in f:
            if "\t" in line:
                line = line.split("\t")[0]
            if line[0] == ".":
                line = line[1:]
            self.couponSet.add(line.rstrip())


    def add_review_from_file(self, f):
        for line in f:
            if line[0] == ".":
                line = line[1:]
            self.reviewSet.add(line.rstrip())

    def add_socialmedia_from_file(self, f):
        for line in f:
            if line[0] == ".":
                line = line[1:]
            self.socialMediaSet.add(line.rstrip())

    def in_target_site(self, domain):
        return domain in self.checkoutDict

    def in_relevant_site(self, domain):
        return (domain in self.checkoutDict or domain in self.reviewSet or domain in self. socialMediaSet or
            domain in self.couponSet)


    def get_category(self, domain):
        if self.in_target_site(domain):
            return self.checkoutDict[domain][2]
        else:
            return "Key Not Found"

    def get_checkoutURL(self, domain):
        if self.in_target_site(domain):
            return self.checkoutDict[domain][1]
        else:
            return "Key Not Found"

    def get_productURL(self, domain):
        if self.in_target_site(domain):
            return self.checkoutDict[domain][0]
        else:
            return "Key Not Found"

    def checkout_match(self, domain, url):
        return self.get_checkoutURL( domain) == url

    def product_match(self, domain, url):
        return self.get_productURL(domain) == url

    def is_coupon(self, domain):
        return domain in self.couponSet

    def is_review(self, domain):
        return domain in self.reviewSet

    def is_socialmedia(self, domain):
        return domain in self.socialMediaSet






