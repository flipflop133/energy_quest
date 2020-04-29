

def ai_play(dict_army,
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
    dict_memory : dictionnary of order given by the ai in past turn and useful data(dict)
    dict_order: dictionnary with all the orders(dict)

    return
    -----------
    ai_orders : the order of the ai player (str)

    specification: Dominik Everaert (v.1 20/04/20)
    implementation:  François Bechet (v.1  27/04/20)

    """
    orders = ''
    # define ally and enemy
    for i in players:
        if i != player:
            enemy = i
    ally = player
    players = (enemy, ally)

    analyse_data(dict_army, dict_board, dict_memory, players)
    # determine recruit orders
    orders += analyse_recruit(dict_army, players, dict_memory)
    orders += analyse_attack(dict_army, dict_board, players)
    orders += analyse_upgrade(dict_army,dict_memory,dict_recruit, players)

    dict_peaks = analyse_data(dict_army, dict_board, dict_memory, players)[1]
    dict_enemy_cruisers = analyse_data(dict_army, dict_board, dict_memory, players)[2]
    # determine move orders
    orders += analyse_move(dict_army, dict_board, dict_peaks, dict_enemy_cruisers, players)
    analyse_transfer(dict_army, dict_board, dict_peaks, players)

    return orders


def analyse_data(dict_army, dict_board, dict_memory, players):
    """update dict_memory

    Parameters
    ----------
    dict_army: dictionnary with the unit of the two player(dict)
    dict_board: dictionnary with all the characteristic of the board (dict)
    dict_memory : dictionnary of order given by the ai in past turn and useful data(dict)
    players: names of the players(tuple)

    returns
    -------
    dict_memory :dictionnary of order given by the ai in past turn and useful data(dict)

    Version
    −−−−−−−
    specification: Dominik Everaert (v.1 20/04/20)
    implementation:  François Bechet (v.1  27/04/20)
    """
    # determine some stats
    enemy_cruiser = 0
    enemy_tanker = 0
    ally_cruiser = 0
    ally_tanker = 0
    total_energy_required = 0
    total_energy_giveable = 0
    for unit in dict_army[players[0]]:
        if dict_army[players[0]][unit]['ship_type'] == 'cruiser':
            enemy_cruiser += 1
        elif dict_army[players[0]][unit]['ship_type'] == 'tanker':
            enemy_tanker += 1
    for unit in dict_army[players[1]]:
        if dict_army[players[1]][unit]['ship_type'] == 'cruiser':
            ally_cruiser += 1
            total_energy_required += dict_army[
                players[1]][unit]['energy_capacity']
        elif dict_army[players[1]][unit]['ship_type'] == 'tanker':
            ally_tanker += 1
            total_energy_giveable += dict_army[
                players[1]][unit]['energy_capacity']

    dict_memory['data'].update({
        'enemy_cruiser': enemy_cruiser,
        'enemy_tanker': enemy_tanker,
        'ally_cruiser': ally_cruiser,
        'ally_tanker': ally_tanker,
        'total_energy_required': total_energy_required,
        'total_energy_giveable': total_energy_giveable
    })

    # determine peaks positions
    dict_peaks = {}
    i = 0
    for case, value in dict_board.items():
        if 'peak' in value:
            dict_peaks['peak_' + str(i)] = ({
                'case':
                case,
                'energy':
                dict_board[case]['peak']['energy']
            })
            i += 1

    # determine enemy cruisers positions
    dict_enemy_cruisers = {}
    for case, value in dict_board.items():
        if players[0] in value:
            for unit in (dict_board[case][players[0]]):
                if unit != 'hub':
                    dict_enemy_cruisers[unit] = ({'case': case})

    return dict_memory, dict_peaks, dict_enemy_cruisers


def analyse_recruit(dict_army, players, dict_memory):
    """analyse the game to know if new units are needed

    parameters
    ----------
    dict_army: dictionnary with the unit of the two player(dict)
    players: names of the players(tuple)
    dict_memory : dictionnary of order given by the ai in past turn and useful data(dict)

    return
    ------
    recruit_units: wich units need to be build by ia(str)

    specification: Dominik Everaert (v.1 20/04/20)
    implementation:  (v.1 )

    """
    recruit_units = ''
    # tankers
    if dict_memory['data']['ally_tanker'] < dict_memory['data'][
            'enemy_tanker'] or dict_memory['data'][
                'ally_tanker'] == 0 or dict_memory['data'][
                    'total_energy_required'] > dict_memory['data'][
                        'total_energy_giveable']:
        recruit_units += (' tanker_%s:tanker ' %
                          dict_memory['data']['ally_tanker'])

    # cruisers
    # if enemy has more cruiser, recruit one and also check that we have at least one tanker
    if (dict_memory['data']['ally_cruiser'] < dict_memory['data'][
            'enemy_cruiser'] or dict_memory['data'][
                'ally_cruiser'] == 0 or dict_memory['data'][
                    'total_energy_required'] > dict_memory['data'][
                        'total_energy_giveable']) and (dict_memory['data']['ally_tanker'] >= 1):
        recruit_units += (' cruiser_%s:cruiser ' % dict_memory['data']['ally_cruiser'])
    # if dict_army[player]
    return recruit_units


def analyse_upgrade(dict_army,dict_memory,dict_recruit, players):
    """analyse the game to know which upgrade is needed and affordable

    parameters
    ----------
    dict_army: dictionnary with the unit of the two player(dict)
    dict_memory : dictionnary of order given by the ai in past turn and useful data(dict)
    dict_recruit: dictionnary with research and stat of new ship(dict)
    players: names of the players(tuple)

    return
    ------
    upgrade_orders : upgrade orders for the ia(str)

    specification: Dominik Everaert (v.1 20/04/20)
    implementation: Dominik Everaert  (v.1 29/04/20)

    """
    upgrade_orders = ''
    lim_regen = 2 + min(dict_recruit[players[1]]['research']['storage'],dict_recruit[players[1]]['research']['range'],dict_recruit[players[1]]['research']['move'])
    lim_storage = min(dict_recruit[players[1]]['research']['regeneration'],dict_recruit[players[1]]['research']['range'],dict_recruit[players[1]]['research']['move'])
    lim_range = 2 + min(dict_recruit[players[1]]['research']['storage'],dict_recruit[players[1]]['research']['regeneration'],dict_recruit[players[1]]['research']['move'])
    lim_move = 2 + min(dict_recruit[players[1]]['research']['storage'],dict_recruit[players[1]]['research']['range'],dict_recruit[players[1]]['research']['regeneration'])
    #check if  ther is two ally tanker
    if dict_memory['data']['ally_tanker'] > 2 :
        #see wich upgrade need to be made
        if (dict_recruit[players[1]]['research']['regeneration'])<5 and dict_recruit[players[1]]['research']['regeneration']<lim_regen and
            (dict_army[player[1]]['hub']['current_energy']) >= 750  :
            upgrade_orders = 'upgrade:regeneration'
            return upgrade_orders
        elif (dict_recruit[players[1]]['research']['storage'])<3 and dict_recruit[players[1]]['research']['storage']<lim_storage and
            (dict_army[player[1]]['hub']['current_energy']) >= 600 :
            upgrade_orders = 'upgrade:storage'
            return upgrade_orders
        elif (dict_recruit[players[1]]['research']['move'])<5 and dict_recruit[players[1]]['research']['move']<lim_move and
            (dict_army[player[1]]['hub']['current_energy']) >= 500 :
            upgrade_orders = 'upgrade:move'
            return upgrade_orders
        elif (dict_recruit[players[1]]['research']['range'])<5 and dict_recruit[players[1]]['research']['range']<lim_range and
            (dict_army[player[1]]['hub']['current_energy']) >= 400 :
            upgrade_orders = 'upgrade:range'
            return upgrade_orders


def analyse_attack(dict_army, dict_board, players):
    """analyse the game too know wich unit can attack the enemy

    parameters
    ----------
    dict_army: dictionnary with the unit of the two player(dict)
    dict_board: dictionnary with all the characteristic of the board (dict)
    players: names of the players(tuple)

    return
    ------
    attack_orders : attack order made by ia(str)

    specification: Dominik Everaert (v.1 20/04/20)
    implementation: Dominik Everaert (v.1 28/04/20)

    """
    attack_orders = ""
    from equest_namur_gr_50 import compute_manhattan_distance
    x_shooter = 0
    y_shooter = 0
    x_target = 0
    y_target = 0
    shooting_range = 0
    # pick a unit from army
    for shooter in dict_army[players[1]]:
        # check if it is a cruiser
        if dict_army[players[1]][shooter]['ship_type'] == 'cruiser':
            # pick its coordinate
            for key, value in dict_board.items():
                if players[1] in value:
                    unit = value[players[1]]
                    if shooter in unit:
                        case = key.split('-')
                        case_0 = case[0].strip('@')
                        x_shooter, y_shooter = int(case_0), int(case[1])
            # pick its shooting_range
            shooting_range = dict_army[players[1]][shooter]['shooting_range']
            # pick the coordinate of a possible target
            for target in dict_army[players[0]]:
                for key, value in dict_board.items():
                    if players[0] in value:
                        unit = value[players[0]]
                        if target in unit:
                            case = key.split('-')
                            case_0 = case[0].strip('@')
                            x_target, y_target = int(case_0), int(case[1])
                # check if the range is correct
                if compute_manhattan_distance(x_shooter, y_shooter, x_target,
                                              y_target, shooting_range):
                    # take 1/4 of the energy as damage
                    damage = dict_army[players[1]][shooter]['current_energy']
                    damage = (damage // 10) / 4
                    attack_orders += " %s:*%d-%d=%d " % (shooter, x_target, y_target, damage)
    print(attack_orders)
    return attack_orders


def analyse_move(dict_army, dict_board, dict_peaks, dict_enemy_cruisers, players):
    """analyse the game too know where  the unit needs to go

    parameters
    ----------
    dict_army: dictionnary with the unit of the two player(dict)
    dict_board: dictionnary with all the characteristic of the board (dict)
    players: names of the players(tuple)
    TODO specification: dict_peaks,dict_ennemy_cruise
    return
    ------
    move_units : movements made by ia (str)


    specification: Dominik Everaert (v.1 20/04/20)
    implementation:  François Bechet (v.1  28/04/20)

    """
    move_units = ''
    # move tankers to the nearest peak
    for unit in dict_army[players[1]]:
        if unit != 'hub' and dict_army[
                players[1]][unit]['ship_type'] == 'tanker':
            for case in dict_board:
                if players[1] in dict_board[case] and unit in dict_board[case][
                        players[1]]:
                    peak = find_nearest_peak(dict_peaks, case)
                    case_peak = dict_peaks[peak]['case']
                    move_units += " %s:%s " % (unit, go_to(case, case_peak))

    # move cruisers to the nearest enemy cruiser
    for unit in dict_army[players[1]]:
        if unit != 'hub' and dict_army[
                players[1]][unit]['ship_type'] == 'cruiser':
            for case in dict_board:
                if (players[1] in dict_board[case] and unit in dict_board[case][
                        players[1]]) and (dict_enemy_cruisers != {}):
                    cruiser = find_nearest_cruiser(dict_enemy_cruisers, case)
                    case_cruiser = dict_enemy_cruisers[cruiser]['case']
                    move_units += " %s:%s " % (unit, go_to(case, case_cruiser))

    return (move_units)


def analyse_transfer(dict_army, dict_board, dict_peaks, players):
    """analyse the game to know where is energy needed and who can carry it

    parameters
    ----------
    dict_army: dictionnary with the unit of the two player(dict)
    dict_board: dictionnary with all the characteristic of the board (dict)
    players: names of the players(tuple)

    specification: Dominik Everaert (v.1 20/04/20)
    implementation:  François Bechet (v.1  29/04/20)

    """
    from equest_namur_gr_50 import compute_manhattan_distance
    # check if there's a tanker near a peak
    """ for unit in dict_army[players[1]]:
        if unit != 'hub' and dict_army[
                players[1]][unit]['ship_type'] == 'tanker':
            for case in dict_board:
                if players[1] in dict_board[case] and unit in dict_board[case][
                        players[1]]:
                    peak = find_nearest_peak(dict_peaks, case)
                    case_peak = dict_peaks[peak]['case']

                    compute_manhattan_distance([x_shooter], [y_shooter], [x_target], [y_target]) """

    # determine if the tanker is near a peak


def go_to(case_0, case_1):
    """move from case_0 to case_1

    parameters
    ----------
    case_0: case of current position(str)
    case_1: case of destination(str)

    specification: François Bechet (v.1 28/04/20)
    implementation: François Bechet (v.1 28/04/20)
    """
    # extract x,y positions from case_0
    case_0 = case_0.split('-')
    case_0_x = int(case_0[0].strip('@'))
    case_0_y = int(case_0[1])

    # extract x,y positions from case_1
    case_1 = case_1.split('-')
    case_1_x = int(case_1[0].strip('@'))
    case_1_y = int(case_1[1])

    # determine destination position
    if abs(case_0_x - case_1_x) > 1:  # don't need to be on the unit
        if case_0_x > case_1_x:
            case_0_x = case_0_x - 1
        elif case_0_x < case_1_x:
            case_0_x = case_0_x + 1

    if abs(case_0_y - case_1_y) > 1:  # don't need to be on the unit
        if case_0_y > case_1_y:
            case_0_y = case_0_y - 1
        elif case_0_y < case_1_y:
            case_0_y = case_0_y + 1

    case = ("@%i-%i") % (case_0_x, case_0_y)
    return (case)


def find_nearest_peak(dict_peaks, case):
    """compute the distance between a cruiser and its target

    Parameters
    ----------
    x_shooter: coordinate x of the shooter(int)
    y_shooter: coordinate y of the shooter(int)
    x_target: coordinate x of the target(int)
    y_target: coordinate y of the target(int)

    Return
    ------
    distance: distance between the cruiser and the target(int)

    Version
    -------
    specification: François Bechet (v.1 28/04/20)
    implementation: François Bechet (v.1 28/04/20)
    """
    case = case.split('-')
    case_x = case[0].strip('@')
    case_y = case[1]

    dict_distance = {}
    for peak in dict_peaks:
        case_peak = dict_peaks[peak]['case'].split('-')
        case_0 = case_peak[0].strip('@')
        case_1 = case_peak[1]

        x = abs(int(case_x) - int(case_0))
        y = abs(int(case_y) - int(case_1))
        dict_distance[peak] = (abs(x - y))

    return (min(dict_distance, key=dict_distance.get))


def find_nearest_cruiser(dict_enemy_cruisers, case):
    """compute the distance between a cruiser and its target

    Parameters
    ----------
    x_shooter: coordinate x of the shooter(int)
    y_shooter: coordinate y of the shooter(int)
    x_target: coordinate x of the target(int)
    y_target: coordinate y of the target(int)

    Return
    ------
    distance: distance between the cruiser and the target(int)

    Version
    -------
    specification: François Bechet (v.1 28/04/20)
    implementation: François Bechet (v.1 28/04/20)
    """
    case = case.split('-')
    case_x = case[0].strip('@')
    case_y = case[1]

    dict_distance = {}
    for cruiser in dict_enemy_cruisers:
        case_cruiser = dict_enemy_cruisers[cruiser]['case'].split('-')
        case_0 = case_cruiser[0].strip('@')
        case_1 = case_cruiser[1]

        x = abs(int(case_x) - int(case_0))
        y = abs(int(case_y) - int(case_1))
        dict_distance[cruiser] = (abs(x - y))

    return (min(dict_distance, key=dict_distance.get))
