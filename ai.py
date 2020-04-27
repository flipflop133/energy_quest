

def ai_play(
        dict_army,
        dict_board,
        dict_memory,
        players,
        player,
        dict_order=''):
    """make the Ai play

    parameters
    ----------
    dict_army: dictionnary with the unit of the two player(dict)
    dict_board: dictionnary with all the characteristic of the board (dict)
    players: names of the players(tuple)
    player: current player(str)
    dict_memory : dictionnary of order given by the ai in past turn(dict)
    dict_order: dictionnary with all the orders(dict)

    return
    -----------
    ai_orders : the order of the ai player (str)

    specification: Dominik Everaert (v.1 20/04/20)
    implementation:  (v.1 )

    """
    # define ally and enemy
    for i in players:
        print(i)
        if i != player:
            enemy = i
    ally = player
    players = (enemy, ally)

    # analyse the game
    analyse_data(dict_army, dict_board, dict_memory, players)

    # determine recruit orders
    analyse_recruit(dict_army, players, dict_memory)

    return ''


def analyse_data(dict_army, dict_board, dict_memory, players):
    """update dict_memory

    Parameters
    ----------
    dict_army: dictionnary with the unit of the two player(dict)
    dict_board: dictionnary with all the characteristic of the board (dict)
    players: names of the players(tuple)

    returns
    -------
    dict_memory :dictionnary of order given by the ai in past turn(dict)
    Version
    −−−−−−−
    specification: Dominik Everaert (v.1 20/04/20)
    implementation:  (v.1 )
    """
    # determine some stats
    enemy_cruiser = 0
    enemy_tanker = 0
    ally_cruiser = 0
    ally_tanker = 0
    total_energy_required = 0
    total_energy_giveable = 0
    print(players[0])
    for unit in dict_army[players[0]]:
        if dict_army[players[0]][unit]['ship_type'] == 'cruisers':
            enemy_cruiser += 1
        elif dict_army[players[0]][unit]['ship_type'] == 'tankers':
            enemy_tanker += 1
    for unit in dict_army[players[1]]:
        if dict_army[players[1]][unit]['ship_type'] == 'cruisers':
            ally_cruiser += 1
            total_energy_required += dict_army[players[1]
                                               ][unit]['energy_capacity']
        elif dict_army[players[1]][unit]['ship_type'] == 'tankers':
            ally_tanker += 1
            total_energy_giveable += dict_army[players[1]
                                               ][unit]['energy_capacity']

    dict_memory['data'].update({'enemy_cruiser': enemy_cruiser,
                                'enemy_tanker': enemy_tanker,
                                'ally_cruiser': ally_cruiser,
                                'ally_tanker': ally_tanker,
                                'total_energy_required': total_energy_required,
                                'total_energy_giveable': total_energy_giveable})
    print(dict_memory)
    return dict_memory


def analyse_recruit(dict_army, players, dict_memory):
    """analyse the game to know if new units are needed

    parameters
    ----------
    dict_army: dictionnary with the unit of the two player(dict)
    players: names of the players(tuple)
    dict_memory : dictionnary of order given by the ai in past turn(dict)

    specification: Dominik Everaert (v.1 20/04/20)
    implementation:  (v.1 )

    """
    recruit_units = []
    # tankers
    if dict_memory['data']['ally_tanker'] < dict_memory['data']['enemy_tanker'] or dict_memory['data'][
            'ally_tanker'] == 0 or dict_memory['data']['total_energy_required'] > dict_memory['data']['total_energy_giveable']:
        recruit_units.append(
            'tanker%s:tanker' %
            dict_memory['data']['ally_tanker'])
    # if dict_army[player]

    return recruit_units


def analyse_upgrade(dict_army, players):
    """analyse the game to know which upgrade is needed and affordable

    parameters
    ----------
    dict_army: dictionnary with the unit of the two player(dict)
    players: names of the players(tuple)

    specification: Dominik Everaert (v.1 20/04/20)
    implementation:  (v.1 )

    """


def analyse_attack(dict_army, dict_board, players):
    """analyse the game too know wich unit can attack the enemy

    parameters
    ----------
    dict_army: dictionnary with the unit of the two player(dict)
    dict_board: dictionnary with all the characteristic of the board (dict)
    players: names of the players(tuple)

    specification: Dominik Everaert (v.1 20/04/20)
    implementation:  (v.1 )

    """


def analyse_move(dict_army, dict_board, players):
    """analyse the game too know where  the unit needs to go

    parameters
    ----------
    dict_army: dictionnary with the unit of the two player(dict)
    dict_board: dictionnary with all the characteristic of the board (dict)
    players: names of the players(tuple)

    specification: Dominik Everaert (v.1 20/04/20)
    implementation:  (v.1 )

    """


def analyse_transfer(dict_army, dict_board, players):
    """analyse the game too know where is energy needed and who can carry it

    parameters
    ----------
    dict_army: dictionnary with the unit of the two player(dict)
    dict_board: dictionnary with all the characteristic of the board (dict)
    players: names of the players(tuple)

    specification: Dominik Everaert (v.1 20/04/20)
    implementation:  (v.1 )

    """
