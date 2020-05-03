

def ai_play(dict_army,
            dict_board,
            dict_memory,
            dict_recruit,
            players,
            player,):
    """make the Ai play

    parameters
    ----------
    dict_army: dictionnary with the unit of the two player(dict)
    dict_board: dictionnary with all the characteristic of the board (dict)
    players: names of the players(tuple)
    player: current player(str)
    dict_memory : dictionnary of order given by the ai in past turn and useful data(dict)

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
    orders += analyse_upgrade(dict_army, dict_memory, dict_recruit, players)

    dict_peaks = analyse_data(dict_army, dict_board, dict_memory, players)[1]
    dict_enemy_cruisers = analyse_data(
        dict_army, dict_board, dict_memory, players)[2]
    # determine move orders
    orders += analyse_move(dict_army, dict_board,
                           dict_peaks, dict_enemy_cruisers, dict_memory, players)
    orders += analyse_transfer(dict_army, dict_board, dict_peaks, dict_memory, players)

    return orders


def analyse_data(dict_army, dict_board, dict_memory, players):
    """update dict_memory

    Parameters
    ----------
    dict_army: dictionnary with the unit of the two player(dict)
    dict_board: dictionnary with all the characteristic of the board (dict)
    dict_memory : dictionnary of order given by the ai in past turn and useful data(dict)
    players: names of the players(tuple)

    return
    -------
    dict_memory :dictionnary of order given by the ai in past turn and useful data(dict)

    Version
    −−−−−−−
    specification: Dominik Everaert (v.1 20/04/20)
    implementation:  François Bechet (v.1  27/04/20)
    """
    # determine some stats
    enemy_cruiser, enemy_tanker, ally_cruiser, ally_tanker, total_energy_required, total_energy_giveable = 0, 0, 0, 0, 0, 0
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

    # check if orders are still valid
    wrong_orders = []
    print(dict_memory)
    for unit, order in dict_memory['orders'].items():
        if (
            # delete orders if a tanker want to go on a dead cruiser
            (dict_army[players[1]][unit]['ship_type'] == 'tanker' and 'peak' not in order and 'hub' not in order) and
            (dict_army[players[1]][order]['hp'] <= 0 or order not in dict_army[players[1]]) or

            # delete orders if a cruiser want to go on a dead enemy cruiser
            (dict_army[players[1]][unit]['ship_type'] == 'cruiser' and 'peak' not in order and 'hub' not in order) and
            (dict_army[players[0]][order]['hp'] <= 0 or unit not in dict_army[players[0]]) or

            # verify that the peak still exist
            (('hub' not in dict_memory['orders'][unit]) and (('peak' in dict_memory['orders'][unit]) and
            (dict_memory['orders'][unit] not in dict_peaks)))
        ):
            wrong_orders.append(unit)

    # delete all wrong orders
    if wrong_orders != []:
        for unit in wrong_orders:
            dict_memory['orders'].pop(unit)

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
    implementation: François Bechet (v.1 28/04/20)

    """
    recruit_units = ''
    # tankers
    if (dict_memory['data']['ally_tanker'] < dict_memory['data'][
            'enemy_tanker'] or dict_memory['data'][
                'ally_tanker'] < 2 or dict_memory['data'][
                    'total_energy_required'] > dict_memory['data'][
                        'total_energy_giveable']):
        recruit_units += (' tanker_%s:tanker ' %
                          dict_memory['data']['ally_tanker'])

    # cruisers
    # if enemy has more cruiser, recruit one and also check that we have at least one tanker
    if (dict_memory['data']['ally_cruiser'] < dict_memory['data'][
            'enemy_cruiser'] or dict_memory['data'][
                'ally_cruiser'] == 0 or dict_memory['data'][
                    'total_energy_required'] > dict_memory['data'][
                        'total_energy_giveable']) and (dict_memory['data']['ally_tanker'] >= 1):
        recruit_units += (' cruiser_%s:cruiser ' %
                          dict_memory['data']['ally_cruiser'])
    # if dict_army[player]
    return recruit_units


def analyse_upgrade(dict_army, dict_memory, dict_recruit, players):
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
    implementation: Dominik Everaert (v.1 29/04/20)

    """
    upgrade_orders = ''
    lim_regen = 2 + min(dict_recruit[players[1]]['research']['storage'], dict_recruit[players[1]]
                        ['research']['range'], dict_recruit[players[1]]['research']['move'])
    lim_storage = min(dict_recruit[players[1]]['research']['regeneration'], dict_recruit[players[1]]
                      ['research']['range'], dict_recruit[players[1]]['research']['move'])
    lim_range = 2 + min(dict_recruit[players[1]]['research']['storage'], dict_recruit[players[1]]
                        ['research']['regeneration'], dict_recruit[players[1]]['research']['move'])
    lim_move = 2 + min(dict_recruit[players[1]]['research']['storage'], dict_recruit[players[1]]
                       ['research']['range'], dict_recruit[players[1]]['research']['regeneration'])
    # check if  ther is two ally tanker
    if dict_memory['data']['ally_tanker'] >= 2:
        # see wich upgrade need to be made
        if (dict_recruit[players[1]]['research']['regeneration']) < 5 and dict_recruit[players[1]]['research']['regeneration'] < lim_regen and (dict_army[players[1]]['hub']['current_energy']) >= 750:
            upgrade_orders = 'upgrade:regeneration'
            return upgrade_orders
        elif (dict_recruit[players[1]]['research']['storage']) < 3 and dict_recruit[players[1]]['research']['storage'] < lim_storage and (dict_army[players[1]]['hub']['current_energy']) >= 600:
            upgrade_orders = 'upgrade:storage'
            return upgrade_orders
        elif (dict_recruit[players[1]]['research']['move']) < 5 and dict_recruit[players[1]]['research']['move'] < lim_move and (dict_army[players[1]]['hub']['current_energy']) >= 500:
            upgrade_orders = 'upgrade:move'
            return upgrade_orders
        elif (dict_recruit[players[1]]['research']['range']) < 5 and dict_recruit[players[1]]['research']['range'] < lim_range and (dict_army[players[1]]['hub']['current_energy']) >= 400:
            upgrade_orders = 'upgrade:range'
            return upgrade_orders
        else:
            return upgrade_orders
    else:
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
    x_shooter, y_shooter, x_target, y_target, shooting_range = 0, 0, 0, 0, 0
    # pick a unit from army
    for shooter in dict_army[players[1]]:
        # check if it is a cruiser
        if dict_army[players[1]][shooter]['ship_type'] == 'cruiser':
            # pick its coordinate
            for key, value in dict_board.items():
                if players[1] in value:
                    unit = value[players[1]]
                    if shooter in unit:
                        x_shooter, y_shooter = case_into_pos(key)
            # pick its shooting_range
            shooting_range = dict_army[players[1]][shooter]['shooting_range']
            # pick the coordinate of a possible target
            for target in dict_army[players[0]]:
                for key, value in dict_board.items():
                    if players[0] in value:
                        unit = value[players[0]]
                        if target in unit:
                            x_target, y_target = case_into_pos(key)
                print(x_shooter, y_shooter, x_target, y_target)
                # check if the range is correct
                if compute_manhattan_distance(x_shooter, y_shooter, x_target,
                                              y_target, shooting_range):
                    # take 1/4 of the energy as damage
                    damage = dict_army[players[1]][shooter]['current_energy']
                    damage = (damage // 10) / 4
                    attack_orders += " %s:*%d-%d=%d " % (
                        shooter, x_target, y_target, damage)
    return attack_orders


def analyse_move(dict_army, dict_board, dict_peaks, dict_enemy_cruisers, dict_memory, players):
    """analyse the game too know where  the unit needs to go

    parameters
    ----------
    dict_army: dictionnary with the unit of the two player(dict)
    dict_board: dictionnary with all the characteristic of the board (dict)
    players: names of the players(tuple)
    dict_peaks: dictionnary with all the peaks locations(dict)
    dict_enemy_cruisers: dictionnary with all the enemy cruisers locations(dict)

    return
    ------
    move_units : movements made by ia (str)


    specification: Dominik Everaert (v.1 20/04/20)
    implementation:  François Bechet (v.1  28/04/20)

    """
    move_units = ''
    # if tanker energy_capacity <= 50% and there are still peaks on the map
    # move tankers to the nearest peak

    print(dict_memory)
    for unit in dict_army[players[1]]:
        if unit != 'hub' and dict_army[
                players[1]][unit]['ship_type'] == 'tanker':
            # check that the tanker doesn't already have an order
            if unit not in dict_memory['orders']:
                for case in dict_board:
                    if players[1] in dict_board[case] and unit in dict_board[case][
                            players[1]]:
                        # if tanker energy < 50% -> find energy
                        if dict_army[players[1]][unit]['current_energy'] / dict_army[players[1]][unit]['energy_capacity'] < 50 / 100:
                            # move tankers to the nearest peak
                            if dict_peaks != {}:
                                peak = find_nearest_entity(dict_peaks, case)
                                case_peak = dict_peaks[peak]['case']
                                move_units += " %s:%s " % (unit, go_to(case, case_peak))
                                dict_memory['orders'].update({unit: peak})
                            # move tankers to the hub
                            else:
                                for case_hub in dict_board:
                                    if players[1] in dict_board[case_hub] and 'hub' in dict_board[case_hub][players[1]]:
                                        move_units += " %s:%s " % (unit, go_to(case, case_hub))
                                        dict_memory['orders'].update({unit: 'receiving_hub'})
                        # if tanker energy > 50% -> give energy to the hub or to the cruisers
                        else:
                            for second_unit in dict_army[players[1]]:
                                # if cruiser energy < 1/4 -> cruisers
                                if (second_unit != 'hub' and dict_army[
                                    players[1]][second_unit]['ship_type'] == 'cruiser') and (dict_army[players[1]][second_unit]['current_energy'] / dict_army[players[1]][second_unit]['energy_capacity'] < 25 / 100):
                                    for case_cruiser in dict_board:
                                        if players[1] in dict_board[case_cruiser] and second_unit in dict_board[case_cruiser][players[1]]:
                                            move_units += " %s:%s " % (unit, go_to(case, case_cruiser))
                                            dict_memory['orders'].update({unit: second_unit})
                                            print('working')

                                # if hub energy < 1/2 -> hub
                                if second_unit == 'hub' and dict_army[players[1]]['hub']['current_energy'] / dict_army[players[1]]['hub']['energy_capacity'] < 50 / 100:
                                    # find hub position
                                    for case_hub in dict_board:
                                        if players[1] in dict_board[case_hub] and 'hub' in dict_board[case_hub][players[1]]:
                                            move_units += " %s:%s " % (unit, go_to(case, case_hub))
                                            dict_memory['orders'].update({unit: 'hub'})

                                # if cruisers < 3/4 -> cruisers
                                if (second_unit != 'hub' and dict_army[
                                    players[1]][second_unit]['ship_type'] == 'cruiser') and (dict_army[players[1]][second_unit]['current_energy'] / dict_army[players[1]][second_unit]['energy_capacity'] < 75 / 100):
                                    for case_cruiser in dict_board:
                                        if players[1] in dict_board[case_cruiser] and second_unit in dict_board[case_cruiser][players[1]]:
                                            move_units += " %s:%s " % (unit, go_to(case, case_cruiser))
                                            dict_memory['orders'].update({unit: second_unit})

                                # else -> hub
                                if second_unit == 'hub' and dict_army[players[1]]['hub']['current_energy'] / dict_army[players[1]]['hub']['energy_capacity'] < 75 / 100:
                                    # find hub position
                                    for case_hub in dict_board:
                                        if players[1] in dict_board[case_hub] and 'hub' in dict_board[case_hub][players[1]]:
                                            move_units += " %s:%s " % (unit, go_to(case, case_hub))
                                            dict_memory['orders'].update({unit: 'hub'})

            # if the tanker already has an order and the order is still valid, continue to execute it
            else:
                for case in dict_board:
                    if players[1] in dict_board[case] and unit in dict_board[case][
                            players[1]]:
                        order = dict_memory['orders'][unit]
                        # peak order
                        if 'peak' in order:
                            case_peak = dict_peaks[order]['case']
                            move_units += " %s:%s " % (unit, go_to(case, case_peak))
                        # hub order
                        elif 'hub' in order:
                            # find hub position
                            for case_hub in dict_board:
                                if players[1] in dict_board[case_hub] and 'hub' in dict_board[case_hub][players[1]]:
                                    move_units += " %s:%s " % (unit, go_to(case, case_hub))
                        # cruiser order
                        else:
                            for case_cruiser in dict_board:
                                if players[1] in dict_board[case_cruiser] and order in dict_board[case_cruiser][players[1]]:
                                    move_units += " %s:%s " % (unit, go_to(case, case_cruiser))

    # move cruisers to the nearest enemy cruiser
    for unit in dict_army[players[1]]:
        if unit != 'hub' and dict_army[
                players[1]][unit]['ship_type'] == 'cruiser':
            for case in dict_board:
                if (players[1] in dict_board[case] and unit in dict_board[case][
                        players[1]]) and (dict_enemy_cruisers != {}):
                    cruiser = find_nearest_entity(dict_enemy_cruisers, case)
                    case_cruiser = dict_enemy_cruisers[cruiser]['case']
                    move_units += " %s:%s " % (unit, go_to(case, case_cruiser))

    return move_units


def analyse_transfer(dict_army, dict_board, dict_peaks, dict_memory, players):
    """analyse the game to know where is energy needed and who can carry it

    parameters
    ----------
    dict_army: dictionnary with the unit of the two player(dict)
    dict_board: dictionnary with all the characteristic of the board (dict)
    dict_peaks: dictionnary with all the peaks locations(dict)
    dict_memory : dictionnary of order given by the ai in past turn and useful data(dict)
    players: names of the players(tuple)

    return
    ------
    transfer_orders : ia transfer orders(str)

    specification: Dominik Everaert (v.1 20/04/20)
    implementation:  François Bechet (v.1  29/04/20)

    """

    transfer_orders = ''
    from equest_namur_gr_50 import compute_manhattan_distance

    print(dict_memory)
    for unit in dict_army[players[1]]:
        if unit != 'hub' and dict_army[
                players[1]][unit]['ship_type'] == 'tanker':
            for case in dict_board:
                if players[1] in dict_board[case] and unit in dict_board[case][
                        players[1]] and unit in dict_memory['orders']:
                    # check the order assigned to the tanker
                    order = dict_memory['orders'][unit]

                    # tanker -> peak
                    if 'peak' in order:
                        peak = find_nearest_entity(dict_peaks, case)
                        case_peak = dict_peaks[peak]['case']

                        x_shooter, y_shooter = case_into_pos(case)

                        x_target, y_target = case_into_pos(case_peak)

                        if compute_manhattan_distance(x_shooter, y_shooter, x_target, y_target):
                            transfer_orders += " %s:<%i-%i " % (unit, x_target, y_target)
                            # clean dict_memory
                            dict_memory['orders'].pop(unit)

                    # tanker -> hub
                    elif 'hub' in order:
                        for case_hub in dict_board:
                            if players[1] in dict_board[case_hub] and 'hub' in dict_board[case_hub][players[1]]:

                                x_shooter, y_shooter = case_into_pos(case)

                                x_target, y_target = case_into_pos(case_hub)

                                if compute_manhattan_distance(x_shooter, y_shooter, x_target, y_target):
                                    if 'receiving_hub' in order:
                                        transfer_orders += " %s:<%d-%d " % (unit, x_target, y_target)
                                    else:
                                        transfer_orders += " %s:>hub " % (unit)
                                    # clean dict_memory
                                    dict_memory['orders'].pop(unit)

                    # tanker -> cruiser
                    else:
                        for case_cruiser in dict_board:
                            if players[1] in dict_board[case_cruiser] and order in dict_board[case_cruiser][players[1]]:
                                x_shooter, y_shooter = case_into_pos(case)
                                x_target, y_target = case_into_pos(case_cruiser)
                                if compute_manhattan_distance(x_shooter, y_shooter, x_target, y_target):
                                    transfer_orders += " %s:>%s " % (unit, order)
                                    # clean dict_memory
                                    dict_memory['orders'].pop(unit)
    return transfer_orders


def go_to(case_0, case_1):
    """move from case_0 to case_1

    parameters
    ----------
    case_0: case of current position(str)
    case_1: case of destination(str)

    return
    -------
    case: case location to go to(str)

    specification: François Bechet (v.1 28/04/20)
    implementation: François Bechet (v.1 28/04/20)
    """
    # extract x,y positions from case_0
    case_0_x, case_0_y = case_into_pos(case_0)

    # extract x,y positions from case_1
    case_1_x, case_1_y = case_into_pos(case_1)

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
    return case


def find_nearest_entity(dict_entities, case):
    """compute the distance between a cruiser and its target

    Parameters
    ----------
    dict_entity: dictionnary with all the entities locations(dict)
    case: case of the unit(str)

    return
    ------
    distance: distance between the cruiser and the target(int)

    Version
    -------
    specification: François Bechet (v.1 28/04/20)
    implementation: François Bechet (v.1 28/04/20)
    """
    case_x, case_y = case_into_pos(case)

    dict_distance = {}
    for entity in dict_entities:

        case_0, case_1 = case_into_pos(dict_entities[entity]['case'])

        x = abs(int(case_x) - int(case_0))
        y = abs(int(case_y) - int(case_1))
        dict_distance[entity] = (abs(x - y))

    return (min(dict_distance, key=dict_distance.get))


def case_into_pos(case):
    """change a case into coordinates of a positions

    Parameters
    ----------
    case: the case to transforme(str)

    return
    ------
     x: position in column
     y: position in line

     specification: Dominik Everaert (v.1 1/05/20)
     implementation: Dominik Everaert (v.1 1/05/20)
    """
    case = case.split('-')
    x = int(case[0].strip('@'))
    y = int(case[1])

    return x, y
