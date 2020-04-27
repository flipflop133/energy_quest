

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
    orders = ''
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
    orders += analyse_recruit(dict_army, players, dict_memory)

    # determine move orders
    analyse_move(dict_army, dict_board, players)

    return orders


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
    print(dict_army)
    for unit in dict_army[players[0]]:
        if dict_army[players[0]][unit]['ship_type'] == 'cruiser':
            enemy_cruiser += 1
        elif dict_army[players[0]][unit]['ship_type'] == 'tanker':
            enemy_tanker += 1
    for unit in dict_army[players[1]]:
        if dict_army[players[1]][unit]['ship_type'] == 'cruiser':
            ally_cruiser += 1
            total_energy_required += dict_army[players[1]
                                               ][unit]['energy_capacity']
        elif dict_army[players[1]][unit]['ship_type'] == 'tanker':
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
    recruit_units = ''
    # tankers
    if dict_memory['data']['ally_tanker'] < dict_memory['data']['enemy_tanker'] or dict_memory['data'][
            'ally_tanker'] == 0 or dict_memory['data']['total_energy_required'] > dict_memory['data']['total_energy_giveable']:
        recruit_units += (
            'tanker_%s:tanker' %
            dict_memory['data']['ally_tanker'])
    # if dict_army[player]

    print(recruit_units)
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
    # tanker_0:@5-4
    for unit in dict_army[players[1]]:
        if unit == 'tanker':
            pass

    # determine peaks positions
    dict_peaks = {}
    i = 0
    for case, value in dict_board.items():
        if 'peak' in value:
            print(case, value)
            dict_peaks['hub_' + str(i)] = ({'case': case, 'energy': dict_board[case]['peak']['energy']})
            i += 1  
    print(dict_peaks)

    
    for case, value in dict_board.items():
        # find tanker position
        if players[1] in value:
            for unit, unit_type in dict_board[case][players[1]].items():
                if unit_type != '':
                    for c_unit, property in dict_board[case][players[1]][unit].items():
                        if property == 'tanker':
                            print(case)
                
                # determine the nearest peak


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
