import unittest
from puerto_rico.take7.game import Game, InvalidChoiceError
from puerto_rico.take7.fields import *

class GeneralTest(unittest.TestCase):

    def test_settup(self):
        """
        tile flip
        -> p1_hacienda_choice
        -> -> p1_hacienda_flip
        """

        g = Game()

        self.assertEqual(g[farm_open][tile.corn], 0)

        g.step(tile.corn)
        g.step(tile.corn)
        g.step(tile.corn)

        self.assertEqual(g[state], states.role_choice)
        self.assertEqual(g[farm_open][tile.corn], 3)
        self.assertEqual(g[active], 0)

    def test_settup_invalid(self):
        g = Game()
        with self.assertRaises(Exception):
            g.step('planter')
        with self.assertRaises(Exception):
            g.step(6)
        with self.assertRaises(Exception):
            g.step(1.2)

    def test_role_cards(self):

        for amount in (0, 1, 2, 12):
            for card in range(7):
                g = Game()
                g[state] = states.role_choice
                g[which_role_has_bonus] = card
                g[role_bonus] = amount

                start = g[g[active]+cash]
                g.step(card)
                diff = g[g[active]+cash] - start
                self.assertEqual(amount, diff)

    def test_invalid_role_choice(self):
        g = Game()
        with self.assertRaises(Exception):
            g.step('planter')
        with self.assertRaises(Exception):
            g.step(7)
        with self.assertRaises(Exception):
            g.step(1.2)

class TestPlanter(unittest.TestCase):

    def test_role_choice_to_planter(self):

        for start_player in (0, 5):
            g = Game()
            g[active] = start_player
            g[farm_open] = [1, 1, 1, 0, 0, 5]
            g[state] = states.role_choice
            g.step(role.planter)
            self.assertEqual(states.planter_main, g[state])

            g = Game()
            g[active] = start_player
            g[farm_open] = [1, 1, 1, 0, 0, 5]
            g[state] = states.role_choice
            g[start_player + island][building.hacienda] = 1
            g[start_player + jobs][building.hacienda] = 1
            g.step(role.planter)
            self.assertEqual(states.hacienda_choice, g[state])

    def test_hacienda_choice_branching(self):

        for hacienda_player in (0, 5):
            for hacienda_choice in (False, True):
                g = Game()
                g[active] = hacienda_player
                g[farm_open] = [1,1,1,0,0,5]
                g[state] = states.hacienda_choice

                g.step(hacienda_choice)
                if hacienda_choice:
                    self.assertEqual(states.hacienda_flip, g[state])
                else:
                    self.assertEqual(states.planter_main, g[state])

    def test_hacienda_flip(self):

        for active_player in (0, 5):
            for random_tile in range(5):
                g = Game()
                g[active] = active_player
                g[state] = states.hacienda_flip

                start = g[g[active]+island][random_tile]
                g.step(random_tile)
                self.assertEqual(start+1, g[g[active]+island][random_tile])

    def test_quarry_choice_invalid(self):

        g = Game()
        g[active] = 0
        g[role_user] = 5
        g[state] = states.planter_main
        with self.assertRaises(Exception):
            g.step(tile.quarry)

    def test_quarry_choice_role_user(self):
        g = Game()
        g[active] = 0
        g[role_user] = 0
        g[state] = states.planter_main
        g.step(tile.quarry)
        self.assertEqual(g[0+island][tile.quarry], 1)

    def test_quarry_choice_construction_hut(self):
        g = Game()
        g[active] = 0
        g[role_user] = 5
        g[state] = states.planter_main
        g[0 + island][building.construction_hut] = 1
        g[0 + jobs][building.construction_hut] = 1
        g.step(tile.quarry)
        self.assertEqual(g[0+island][tile.quarry], 1)


class MayorTest(unittest.TestCase):
    def test_mayor_bonus_invalid(self):
        g = Game()
        g[state] = states.mayor_bonus
        with self.assertRaises(Exception):
            g.step(1)

    def test_mayor_bonus_refused(self):
        g = Game()
        g[state] = states.mayor_bonus
        g[settler_ship] = 0
        self.assertEqual(sum(g[jobs]), 0)
        g.step(False)
        self.assertEqual(sum(g[jobs]), 0)

    def test_mayor_bonus_accepted(self):
        g = Game()
        g[state] = states.mayor_bonus
        g[settler_ship] = 0
        self.assertEqual(sum(g[jobs]), 0)
        g.step(True)
        self.assertEqual(sum(g[jobs]), 1)

    def test_give_settlers_odd(self):

        g = Game()
        g[settler_ship] = 5
        g[active] = 0
        g[role_user] = 0
        g.give_settlers()
        self.assertEqual(sum(g[0+jobs]), 3)

        g[active] = 5
        g.give_settlers()
        self.assertEqual(sum(g[5+jobs]), 2)

    def test_give_settlers_even(self):
        g = Game()
        g[settler_ship] = 4
        g[active] = 0
        g.give_settlers()
        self.assertEqual(sum(g[0+jobs]), 2)

        g[active] = 5
        g.give_settlers()
        self.assertEqual(sum(g[5+jobs]), 2)

    def test_mayor_flow(self):
        g = Game()
        g[state] = states.role_choice
        g.step(role.mayor)
        self.assertEqual(states.mayor_bonus,g[state])

        g.step(True)
        self.assertEqual(states.assign_work,g[state])

        assignments = [0 for _ in range(island_size)]
        assignments[tile.indigo] = 1
        assignments[building.idle] = 1
        g.step(assignments)
        self.assertEqual(states.assign_work, g[state])

        assignments = [0 for _ in range(island_size)]
        assignments[tile.corn] = 1
        g.step(assignments)
        self.assertEqual(states.role_choice, g[state])

class GameEndTest(unittest.TestCase):
    def draw(self):
        g = Game()
        g[game_end] = True
        g.proceed()
        self.assertEqual(states.draw, g[state])

    def p1_wins(self):
        g = Game()
        g[game_end] = True
        g[0+vp] = 5
        g.proceed()
        self.assertEqual(states.p1_victory, g[state])

    def p2_wins(self):
        g = Game()
        g[game_end] = True
        g[5 + vp] = 5
        g.proceed()
        self.assertEqual(g[state],states.p2_victory)

    def test_score_basic(self):
        g = Game()

        g.score()
        self.assertEqual(g.score(), [0, 0])

        g[0+vp] = 3
        g[5+vp] = 1
        self.assertEqual(g.score(), [3, 1])

        g[0+vp] = 1
        g[5+vp] = 3
        self.assertEqual(g.score(), [1, 3])

    def test_score_buildings(self):
        g = Game()

        g[0+island][building.construction_hut] = 1
        self.assertEqual(g.score(), [1,0])

        g[5+island][building.coffee_roaster] = 2
        self.assertEqual(g.score(), [1,3])

    def test_score_guild_hall(self):

        g = Game()
        g[0 + island][building.guild_hall] = 1
        g[0 + island][building.small_sugar_mill] = 1
        g[0 + island][building.sugar_mill] = 1
        g[0 + island][building.small_indigo_plant] = 1
        g[0 + island][building.coffee_roaster] = 1

        self.assertEqual(g.score(), [11, 0])

        g[0 + jobs][building.guild_hall] = 1
        self.assertEqual(g.score(), [17,0])

    # def test_prep_tile_flip(self):
    #     g = Game()
    #     g[farm_open][tile.corn] = 2
    #     g[farm_open][tile.indigo] = 1
    #
    #     g.prep_tile_flip()
    #
    #     self.assertTrue(not any(g[farm_open]))
    #
    # def test_tile_flip_invalid(self):
    #     g = Game()
    #     g.state = states.tile_flip
    #
    #     with self.assertRaises(Exception):
    #         g.tile_flip(7)
    #     # with self.assertRaises(Exception):
    #     #     g.tile_flip(-1)
    #     with self.assertRaises(Exception):
    #         g.tile_flip('corn')
    #
    #     g[farm_deck][tile.corn] = 0
    #     with self.assertRaises(Exception):
    #         g.tile_flip(tile.corn)
    #
    # def test_tile_flip_add_each(self):
    #     g = Game()
    #     g.state = states.tile_flip
    #
    #     # adding each tile
    #     for each in range(len(tile.lookup)):
    #         g.prep_tile_flip()
    #         self.assertTrue(not any(g[farm_open]))
    #
    #         g.tile_flip(each)
    #         self.assertEquals(g[farm_open][each], 1)
    #         self.assertEquals(g[state], states.tile_flip)
    #
    # def test_tile_flip_state_progression(self):
    #     g = Game()
    #     g[state] = states.tile_flip
    #
    #     g.step(tile.corn)
    #     self.assertEquals(states.tile_flip, g[state])
    #     print(g[farm_open])
    #
    #     g.step(tile.indigo)
    #     self.assertEquals(states.tile_flip, g[state])
    #     print(g[farm_open])
    #
    #     g.step(tile.sugar)
    #     print(g[farm_open])
    #     self.assertEquals(states.planter_main, g[state])
    #
    # def test_hacienda(self):
    #     pass
    #







if __name__ == '__main__':
    unittest.main()
