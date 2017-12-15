"""Module implementing simplex algorithm"""

import spxparser

class Simplex:
    """The Simplex object modelises production optimisation.

    Usually you call :func:`simplex.simplex` to instantiate a Simplex object

    Dependency: :mod:`spxparser`
    """
    def __init__(self, resources, prices, parser):
        """Initialises :class:`Simplex` according to
        the number of *resources*, the product *prices* and the *parser*
        
        *parser* is a :class:`spxparser.Spxparser` containing
        required resources to produce a product,
        resources names and products names.

        Raises:
            ValueError: Invalid number of arguments when resources, prices
            and parser don't match
        """
        if len(resources) + len(prices) != \
           parser.get_nb_resources() + parser.get_nb_products():
            raise ValueError('Invalid number of arguments')

        self.pivot = {'x': -1, 'y': -1}
        self.resources = resources
        self.prices = prices
        self.base = [-1] * len(prices)
        self.resources_names = parser.get_resources_names()
        self.pdt_names = parser.products

        self.mtx = []
        self.init_mtx(parser)

    def init_mtx(self, parser):
        """Initialize the matrix with the required resources
        defined in *parser*
        """
        values = parser.get_resources_values()
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
        """Solve the simplex.

        Call :func:`get_pivot_position`, :func:`set_values`
        and set the entry values
        """
        # We are finished when all the elements of
        # the last line are greater or equal to 0
        while any(x < 0 for x in self.mtx[-1]):
            self.get_pivot_position()
            self.set_values()

            # set the entry value
            if self.pivot['x'] in self.base:
                self.base[self.base.index(self.pivot['x'])] = -1
            if self.pivot['y'] < len(self.base):
                self.base[self.pivot['y']] = self.pivot['x']

    def get_pivot_position(self):
        """Find the pivot"""
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
        """Set the matrix values according to the pivot"""
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
        """Return the quantity of each product according the matrix
        and the entry values
        """
        if not hasattr(self, 'pdt_quantities'):
            self.pdt_quantities = [self.mtx[x][-1] if x != -1 else 0
                                   for x in self.base]
        return self.pdt_quantities

    def get_total(self):
        """Get the total amount
        """
        if not hasattr(self, 'total'):
            self.total = sum(pdt * prc
                             for pdt, prc
                             in zip(self.get_pdt_quantities(), self.prices))
        return self.total

    def __str__(self):
        """Stringify the simplex.
        It allows you to display the simplex easily:
        ``print(Simplex)`` will display::

            resources: NB1 NAME1, NB2 NAME2, ...

            PRODUCT1: NB1 units at € PRICE1 /unit
            PRODUCT2: NB2 units at € PRICE2 /unit
            ...
            total production value: € TOTAL
        """
        resources = ', '.join('{} {}'
                              .format(r, n)
                              for r, n
                              in zip(self.resources, self.resources_names))

        return ('resources: {}\n\n'.format(resources)
                + ''.join('{}: {} units at € {} /unit\n'
                            .format(n, '{:.2f}'.format(pdt) if pdt != 0 else 0,
                                    prc)
                          for n, pdt, prc
                          in zip(self.pdt_names, self.get_pdt_quantities(),
                                 self.prices))
                + 'total production value: € {:.2f}'.format(self.get_total()))


def simplex(resources, prices, csvfile='', parser=None):
    """Function to create a :class:`Simplex` object\
    according to numbers of *resources* and product *prices*.

    | If *parser* is defined, it instatiates Simplex with it.
    | Otherwise, it calls \
    :func:`spxparser.spxparser` with *csvfile* to get a :class:`spxparser.Spxparser`.
    """
    if parser:
        spx = Simplex(resources, prices, parser)
    else:
        spx = Simplex(resources, prices, spxparser.spxparser(csvfile))
    return spx
