class Simplex:
    def __init__(self, resources, prices):
        self.mtx = [[1, 0, 1, 0, 2, 1, 0, 0, 0, 0, resources[0]],
                    [1, 2, 0, 1, 0, 0, 1, 0, 0, 0, resources[1]],
                    [2, 1, 0, 1, 0, 0, 0, 1, 0, 0, resources[2]],
                    [0, 0, 3, 1, 2, 0, 0, 0, 1, 0, resources[3]],
                    [-prices[0], -prices[1], -prices[2], -prices[3], -prices[4], 0, 0, 0, 0, 1, 0]]

        self.resources = resources
        self.prices = prices


    def solve(self):
        # We are finished when all the elements of the last lines are greate or equal to 0
        while any(x < 0 for x in self.mtx[-1]):
            pass
