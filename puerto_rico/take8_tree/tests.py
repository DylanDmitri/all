import unittest
from puerto_rico.take8_tree.game import Game
from puerto_rico.take8_tree.data import *


class PlanterTest(unittest.TestCase):

    def test_basic(self):
        g = Game()

        tiles = tile.corn, tile.indigo, tile.coffee
        for t in tiles:
            g.step(t)

        for t in tiles:
            self.assertIn(t, g.possible)

        g.step(role.planter)
        self.assertEqual(g.state, State.planter)
        g.step(tile.quarry)
        g.step(tile.corn)

        self.assertEqual(g.farm_open[tile.corn], 0)
        self.assertEqual(g.farm_open[tile.quarry], 4)

class BuilderTest(unittest.TestCase):

    def test_basic(self):
        g = Game()
        g.state = State.role_choice
        g.step(role.builder)

        self.assertEqual(sum(g.p1.island),0)
        self.assertEqual(sum(g.p2.island),0)

        g.step(building.small_market)
        g.step(None)

        self.assertEqual(g.p1.island[building.small_market], 1)
        self.assertEqual(sum(g.p2.island), 0)

    def test_pricing(self):
        g = Game()

        for cash in range(0, 11):
            g.p1.cash = cash

            for quarries in range(0, 5):
                g.p1.island[tile.quarry] = quarries

                for role_user in (g.p1, g.p2):
                    g.role_user = role_user

                    money = cash + (role_user==g.p1)

                    g.transition_to_builder()
                    for b in building.all:

                        if money >= building.costs[b] - min(quarries, building.tiers[b]):
                            self.assertIn(b, g.possible)
                        else:
                            self.assertNotIn(b, g.possible)





if __name__ == '__main__':
    unittest.main()
