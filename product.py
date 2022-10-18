

class Product():
    def __init__(self, json):
        self.id = json['id']
        self.root = json['root']
        self.name = json['name']
        self.brand = json['brand']
        self.price = int(int(json['priceU'])/100)
        self.salePrice = int(int(json['salePriceU'])/100)
        self.averagePrice = int(int(json['averagePrice'])/100)
        self.rating = json['rating']
        self.feedbacks = json['feedbacks']


