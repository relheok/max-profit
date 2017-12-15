"""
Module implementing simplex algorithm
"""

import configparser

class Simplex:
    def __init__(self, resources, prices, parser):
        if len(resources) + len(prices) != parser.get_nb_constraints() + parser.get_nb_products():
            raise ValueError('Invalid number of arguments')

        self.pivot = {'x': -1, 'y': -1}
        self.resources = resources
        self.prices = prices
        self.base = [-1] * len(prices)
        self.constraints_names = parser.get_constraints_names()
        self.pdt_names = parser.products

        self.mtx = []
        self.init_mtx(parser)

    def init_mtx(self, parser):
        values = parser.get_constraints_values()
        psize = len(self.prices)
        for i in range(len(self.resources)):
            self.mtx.append(values[i]
                            + [0] * i
                            + [1]
                            + [0] * (psize - i - 1)
                            + [self.resources[i]])

        # set matrix last line
        pr = []
        for i in range(psize):
            check = True
            for x in range(len(self.mtx)):
                check = self.mtx[x][i] == 0 or self.mtx[x][-1] != 0
            pr.append(-self.prices[i] if check else self.prices[i])
        pr.extend([0] * (psize - 1) + [1, 0])
        self.mtx.append(pr)

    def solve(self):
        # We are finished when all the elements of the last lines are greate or equal to 0
        while any(x < 0 for x in self.mtx[-1]):
            self.get_pivot_position()
            self.set_values()

            # set the entry value
            if self.pivot['x'] in self.base:
                self.base[self.base.index(self.pivot['x'])] = -1
            if self.pivot['y'] < len(self.base):
                self.base[self.pivot['y']] = self.pivot['x']

    def get_pivot_position(self):
        self.pivot = {'x': -1, 'y': -1} # reset pivot

        mini = 0
        for y in range(len(self.mtx[-1])):
            if self.mtx[-1][y] < mini:
                mini = self.mtx[-1][y]
                self.pivot['y'] = y

        mini = -1
        for x in range(len(self.mtx)):
            if self.mtx[x][self.pivot['y']] == 0:
                continue
            res = self.mtx[x][-1] / self.mtx[x][self.pivot['y']]
            if res > 0 and (res < mini or mini == -1):
                mini = res
                self.pivot['x'] = x

        return self.pivot

    def set_values(self):
        pivot_value = self.mtx[self.pivot['x']][self.pivot['y']]

        # set pivot line
        for y in range(len(self.mtx[self.pivot['x']])):
            self.mtx[self.pivot['x']][y] /= pivot_value

        # set all the others
        for x in range(len(self.mtx)):
            if x == self.pivot['x']:
                continue
            value = self.mtx[x][self.pivot['y']]
            for y in range(len(self.mtx[x])):
                self.mtx[x][y] -= self.mtx[self.pivot['x']][y] * value

    def get_pdt_quantities(self):
        if not hasattr(self, 'pdt_quantities'):
            self.pdt_quantities = [self.mtx[x][-1] if x != -1 else 0 for x in self.base]
        return self.pdt_quantities

    def get_total(self):
        if not hasattr(self, 'total'):
            self.total = sum(pdt * prc for pdt, prc in zip(self.get_pdt_quantities(), self.prices))
        return self.total

    def __str__(self):
        resources = ', '.join('{} {}'
                              .format(r, n) for r, n in zip(self.resources, self.constraints_names))
        return ('resources: {}\n\n'.format(resources)
                + ''.join('{}: {} units at € {} /unit\n'
                            .format(n, '{:.2f}'.format(pdt) if pdt != 0 else 0, prc)
                          for n, pdt, prc in zip(self.pdt_names, self.get_pdt_quantities(), self.prices))
                + 'total production value: € {:.2f}'.format(self.get_total()))


def simplex(resources, prices, csvfile='', parser=None):
    if parser:
        spx = Simplex(resources, prices, parser)
    else:
        spx = Simplex(resources, prices, configparser.configparser(csvfile))
    return spx
