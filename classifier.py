import os
# install tldextract

class classifier:
    def __init__(self):
        self.checkoutDict = dict()
        self.couponsSet = set()
        self.reviewSet = set()
        self.socialMediaSet = set()

    def add_category_from_file(self, f):
        category = file.names[:-9]
        for line in f:
            key = line.split("\t")[0]
            value = line.split("\t")[1],line.split("\t")[2],category
            self.checkoutDict[key] = value

    def add_coupon_from_file(self, f):
        for line in f:
            self.couponSet.add(line)

    def add_review_from_file(self, f):
        for line in f:
            self.reviewSet.add(line)

    def add_socialmedia_from_file(self, f):
        for line in f:
            self.socialMediaSet.add(line)

    def in_target_site(self, domain):
        return domain in self.checkoutDict

    def get_category(self, domain):
        if self.in_target_site(domain):
            return self.checkoutDict[domain][2]
        else:
            print("Key not found in category dict")
            return "Key Not Found"

    def get_checkoutURL(self, domain):
        if self.in_target_site(domain):
            return self.checkoutDict[domain][1]
        else:
            print("Key not found in category dict")
            return "Key Not Found"

    def get_productURL(self, domain):
        if self.in_target_site(domain):
            return self.checkoutDict[domain][0]
        else:
            print("Key not found in category dict")
            return "Key Not Found"

    def checkout_match(self, domain, url):
        return self.get_checkoutURL(self, domain) == url

    def product_match(self, domain, url):
        return self.get_productURL(self, domain) == url






