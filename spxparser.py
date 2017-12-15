"""Module to parse CSV files."""

import csv

class Spxparser():
    def __init__(self):
        self.products = []
        self.resources = []

    def parse(self, name):
        with open(name, "r", newline='') as csvfile:
            rd = csv.reader(csvfile, delimiter=';')
            self.setProducts(next(rd)[1:])
            self.setResources(rd)            

    def setProducts(self, line):
        self.products = [name.strip() for name in line]
        for x in self.products:
            if self.products.count(x) > 1:
                raise ValueError("Product {} already exists".format(x))

    def setResources(self, rd):
        size = len(self.products)
        for row in rd:
            name = row[0].strip()
            line = '; '.join(r.strip() for r in row)

            if any(x['name'] == name for x in self.resources):
                raise ValueError("Resource {} already exists".format(name))
            elif size != len(row) - 1:
                raise ValueError("line '{}' expected {} values got {}"
                                 .format(line, size, len(row) - 1))

            try:
                self.resources.append({'name': name,
                                       'values': [float(x) for x in row[1:]]})
            except ValueError:
                raise ValueError("line '{}' expected numbers for each value"
                                 .format(line))

    def default_parser(self):
        self.products = ['oatmeal', 'wheat', 'corn', 'barley', 'soy']
        self.resources = [
            {'name': 'F1', 'values': [1, 0, 1, 0, 2]},
            {'name': 'F2', 'values': [1, 2, 0, 1, 0]},
            {'name': 'F3', 'values': [2, 1, 0, 1, 0]},
            {'name': 'F4', 'values': [0, 0, 3, 1, 2]}
        ]

    def get_resources_names(self):
        return [x['name'] for x in self.resources]

    def get_resources_values(self):
        return [x['values'] for x in self.resources]

    def get_nb_resources(self):
        return len(self.resources)

    def get_nb_products(self):
        return len(self.products)


# Init spxparser
def spxparser(csvfile=""):
    parser = Spxparser()
    if csvfile != "":
        parser.parse(csvfile)
    else:
        parser.default_parser()
    return parser