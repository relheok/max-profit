class Simplex:
    def __init__(self, resources, prices):
        self.mtx = [[1, 0, 1, 0, 2, 1, 0, 0, 0, 0, resources[0]],
                    [1, 2, 0, 1, 0, 0, 1, 0, 0, 0, resources[1]],
                    [2, 1, 0, 1, 0, 0, 0, 1, 0, 0, resources[2]],
                    [0, 0, 3, 1, 2, 0, 0, 0, 1, 0, resources[3]],
                    [-prices[0], -prices[1], -prices[2], -prices[3], -prices[4], 0, 0, 0, 0, 1, 0]]

        self.pivot = {'x': -1, 'y': -1}
        self.resources = resources
        self.prices = prices
        self.base = [-1] * len(prices)


    def solve(self):
        # We are finished when all the elements of the last lines are greate or equal to 0
        while any(x < 0 for x in self.mtx[-1]):
            self.getPivotPosition()
            self.setValues()

            # set the entry value
            if self.pivot['x'] in self.base:
                self.base[self.base.index(self.pivot['x'])] = -1
            if self.pivot['y'] < len(self.base):
                self.base[self.pivot['y']] = self.pivot['x']


    def getPivotPosition(self):
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


    def setValues(self):
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
