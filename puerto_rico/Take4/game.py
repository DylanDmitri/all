from puerto_rico.Take4.assumptions import generate_settings
from puerto_rico.Take4.players.human import HumanPlayer


class Game:
    def __init__(self, players, settings):


def play():
    settings = generate_settings(
        numPlayers=4,
        corn_player_balance=True,       # players who start with corn start with one less dubloon
        university_factory_swap=True,   # university costs 7, factory costs 8
        nobles_on_ships=False,          # should nobles arrive on mayor ships? (does not affect villa)

        additional_role_cards=None,
        # all six core roles are always included
        # if additional roles are not specified, an appropiate number of prospectors are added
        # this does not happen when additional roles are manually specified
        # additional_role_cards=('settler', 'mayor', 'builder', 'craftsman', 'trader', 'captain', 'prospector', 'politician', 'pirate')
        # additional_role_cards='politician'
    )

    # some additional modifications can be made here
    # settings.start_money = 5

    players = (HumanPlayer, HumanPlayer)

    Game(players, settings).start()






