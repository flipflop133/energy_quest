dict_board = {‘case_1’ : {’cruiser_1’,’tanker _1’},’case_2 ‘ : {‘hub_1’}}
dict_army = {'player_1':{'alpha_1': {‘ship_type’ :’cruiser’, ‘HP’ :300, ‘energy’ :200, ‘distance’ :2, …}, beta_1’ : {‘ship_type’ :’tanker’, ‘HP’ :100, ‘energy’ :500, ‘, …}}}
dict_recruit = {'player_1':{'research':{'energy_regen':0,'move_cost':2},‘cruiser’ : {‘HP’ :300, ‘energy-capacity’ :200, ‘distance’ :2, ‘cost’ :1000…} ‘tanker : {, ‘HP’ :200, ‘energy-capacity’ :600, ‘cost’ :500, …}},
                'player_2':{'research':{'energy_regen':1,'move_cost':3},‘cruiser’ : {‘HP’ :300, ‘energy-capacity’ :200, ‘distance’ :2, ‘cost’ :1000…} ‘tanker : {, ‘HP’ :200, ‘energy-capacity’ :600, ‘cost’ :500, …}}}
dict_ordre = {‘player_1’ : {‘recruit’ : {},’upgrade’ : {}, …}
              ‘player_2’ : : {‘recruit’ : {},’upgrade’ : {}, …}}

def display_board(dict_board):
    """
    display the board at the beginning of the game

    parameters
    ----------
    dict_board: dictionnary with all the characteristic of the board (dict)

    Version
    −−−−−−−
    specification : Dominik Everaert ( v.1 24/02/2020)

    """
def game():
    """
    start the game and play it

    Version
    −−−−−−−
    specification : Dominik Everaert ( v.1 24/02/2020)

    """
def get_order():
    """
    ask the player for orders

    return
    ------
    dict_order :dictionnary with all the order
    
    Version
    −−−−−−−
    specification : Dominik Everaert ( v.1 24/02/2020)
    """
def create_board(board_file):
    """
    take a file and change it into a board

    parameters
    ----------
    board_file: file in which all the element needed for the board are(path)
    
    return
    ------
    dict_board: dictionnary with all the characteristic of the board (dict)

    Version
    −−−−−−−
    specification : Dominik Everaert ( v.1 24/02/2020)
    """
    
def attack(dict_order[attack],dict_army):
    """
    execute attack order of each player and modify stats of each effected unit

    parameters
    ----------
    dict_order[attack]: dictionnary of attack order(dict)
    dict_army : dictionnary with the unit of the two player(dict)
    
    return
    ------
    dict_army: dictionnary of the 2 army modified in result of the attack(dict)

    Version
    −−−−−−−
    specification : Dominik Everaert ( v.1 24/02/2020)
    """

def move(dict_order[move],dict_board,dict_army):
    """
    execute move order of each player and modify board and stats of moving units
    
    prameters
    ---------
    dict_order[move]: dictionnary of move order(dict)
    dict_board: dictionnary with all the characteristic of the board (dict)
    dict_army : dictionnary with the unit of the two player(dict)
    
    return
    ------
    dict_board : dictionnary with all the characteristic of the board (dict)

    Version
    −−−−−−−
    specification : Dominik Everaert ( v.1 24/02/2020)
    """

def upgrade(dict_order[upgrade],dict_army,dict_recruit):
    """
    execute the upgrage order of each player and modify the stats of each affected unit

    parameters
    ----------
    dict_order[upgrade]: dictionnary of upgrade order(dict)
    dict_army : dictionnary with the unit of the two player(dict)
    dict_recruit : dictionnary with research and stat of new ship

    return
    ------
    dict_army : dictionnary with the unit of the two player(dict)
    dict_recruit : dictionnary with research and stat of new ship(dict)

    Version
    −−−−−−−
    specification : Dominik Everaert ( v.1 24/02/2020)

    """
def energy_transfert(dict_army,dict_order[energy_transfert]):
    """
    execute transfert order and modify affected unit's stat
    
    parameters
    ----------
    dict_army : dictionnary with the unit of the two player(dict)
    dict_order[energy_transfert]:dictionnary of energy transfert order(dict)
    
    return
    ------
    dict_army : dictionnary with the unit of the two player(dict)

    Version
    −−−−−−−
    specification : Dominik Everaert ( v.1 24/02/2020)
    """
def regenerate(dict_army):
    """
    makes hub regenerate energy(at the end of the turn)

    parameters
    ----------
    dict_army : dictionnary with the unit of the two player(dict)

    return
    ------
    dict_army : dictionnary with the unit of the two player(dict)

    Version
    −−−−−−−
    specification : Dominik Everaert ( v.1 24/02/2020)
    """
def recruit_units(dict_recruit,dict_order[recruit],dict_army):
    """
    execute recruit order and add unit to the army

    parameters
    ----------
    dict_army : dictionnary with the unit of the two player(dict)
    dict_recruit : dictionnary with research and stat of new ship(dict)
    dict_order[recruit]:dictionnary of upgrade order(dict)

    return
    ------
    dict_army : dictionnary with the unit of the two player(dict)
    
    Version
    −−−−−−−
    specification : Dominik Everaert ( v.1 24/02/2020)
    """
def energy_mining(dict_army,dict_order[energy_mining],dict_board):
    """
    execute mining order and modify affected unit's stat and energy peak's stat
    
    parameters
    ----------
    dict_army : dictionnary with the unit of the two player(dict)
    dict_order[energy_mining]:dictionnary of energy mining order(dict)
    dict_board: dictionnary with all the characteristic of the board (dict)
    
    return
    ------
    dict_army : dictionnary with the unit of the two player(dict)
    dict_board: dictionnary with all the characteristic of the board (dict)

    Version
    −−−−−−−
    specification : Dominik Everaert ( v.1 24/02/2020)
    """