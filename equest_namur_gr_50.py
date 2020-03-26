# imports
import copy
import math
import random
import colored


def display_board(dict_board, height, width, players, dict_army):
    """display the board at the beginning of the game

    parameters
    ----------
    dict_board: dictionnary with all the characteristic of the board (dict)
    height:height of the board(int)
    width:width of the board(int)
    players:names of the players(tuple)

    Version
    −−−−−−−
    specification: Dominik Everaert (v.3 24/02/20)
    implementation: François Bechet (v.1 01/03/20)
    """
    # define colored colors
    default_color = colored.attr('reset')
    green = colored.fg('#00ff00')
    red = colored.fg('#ff0000')
    gold = colored.fg('#b08f26')

    # display game's header
    print("################")
    print("# ENERGY QUEST #")
    print("################")

    # display the board
    print(' ', end='')
    for i in range(1, height + 1):
        if i < 10:
            print(i, end='  ')
        else:
            print(i, end=' ')
    print('')

    # display the board's elements
    armies = {}
    for x in range(width):
        n = 1
        for y in range(height):
            # display player0 hub and units
            if players[0] in dict_board['@%d-%d' % (x + 1, y + 1)]:
                tempDict = dict_board['@%d-%d' % (x + 1, y + 1)][players[0]]
                if 'hub' in tempDict:
                    print(green + ' ⌂ ' + default_color, end='')
                else:
                    if len(tempDict) == 1:
                        for key in tempDict:
                            unit = tempDict[key]
                            if 'cruiser' in unit['ship_type']:
                                print(green + ' ☿ ' + default_color, end='')
                            if 'tanker' in unit['ship_type']:
                                print(green + ' * ' + default_color, end='')
                    # if there is more than one unit on the case display dice faces
                    else:
                        case = str(x + 1) + ':' + str(y + 1)
                        armies[case] = {}
                        armies[case].update(tempDict)
                        if len(tempDict) == 2:
                            print(colored.fg('#009900') + ' ⚁ ' + default_color, end='')
                            case = str(x + 1) + ':' + str(y + 1)
                            armies[case] = {}
                            armies[case].update(tempDict)
                        elif len(tempDict) == 3:
                            print(colored.fg('#008800') + ' ⚂ ' + default_color, end='')
                        elif len(tempDict) == 4:
                            print(colored.fg('#007700') + ' ⚃ ' + default_color, end='')
                        elif len(tempDict) == 5:
                            print(colored.fg('#006600') + ' ⚄ ' + default_color, end='')
                        else:
                            print(colored.fg('#005500') + ' ⚅ ' + default_color, end='')
            # display player1 hub and units
            elif players[1] in dict_board['@%d-%d' % (x + 1, y + 1)]:
                tempDict = dict_board['@%d-%d' % (x + 1, y + 1)][players[1]]
                if 'hub' in tempDict:
                    print(red + ' ⌂ ' + default_color, end='')
                else:
                    if len(tempDict) == 1:
                        for key in tempDict:
                            unit = tempDict[key]
                            if 'cruiser' in unit['ship_type']:
                                print(red + ' ☿ ' + default_color, end='')
                            if 'tanker' in unit['ship_type']:
                                print(red + ' * ' + default_color, end='')
                    # if there is more than one unit on the case display dice faces
                    else:
                        case = str(x + 1) + ':' + str(y + 1)
                        armies[case] = {}
                        armies[case].update(tempDict)
                        if len(tempDict) == 2:
                            print(colored.fg('#009900') + ' ⚁ ' + default_color, end='')
                        elif len(tempDict) == 3:
                            print(colored.fg('#008800') + ' ⚂ ' + default_color, end='')
                        elif len(tempDict) == 4:
                            print(colored.fg('#007700') + ' ⚃ ' + default_color, end='')
                        elif len(tempDict) == 5:
                            print(colored.fg('#006600') + ' ⚄ ' + default_color, end='')
                        else:
                            print(colored.fg('#005500') + ' ⚅ ' + default_color, end='')
            # display peaks
            elif 'peak' in dict_board['@%d-%d' % (x + 1, y + 1)]:
                print(gold + ' ⚑ ' + default_color, end='')
            # display cases
            else:
                print(colored.bg('#4fc3f7') + " . " + default_color, end='')
        n = n + x
        print(' ' + str(n))

    # display armies (more than one unit on a case)
    if armies != {}:
        print('\nARMIES')
        for case in armies:
            print('case:', case)
            for unit in armies[case]:
                print(unit)
    # display the energy peaks
    print(gold + '\nENERGY PEAKS' + default_color)
    for case in dict_board:
        if 'peak' in dict_board[case]:
            print(('peak%s') % (case))
            print('energy :', dict_board[case]['peak']['energy'])

    # display the players units and hubs
    for player in players:
        if player == players[0]:
            print('\n' + green + player + default_color + ' : ')
        else:
            print('\n' + red + player + default_color + ' : ')
        for unit, value in dict_army[player].items():
            print(unit.upper())
            for property, value in dict_army[player][unit].items():
                if property != 'turn_attack' and property != 'move':  # player don't need to see these properties
                    print(property, ':', value, end=' ▍')
            print('')
        print('\n')


def game(play_game):
    """start the game and play it

    Version
    −−−−−−−
    specification: François Bechet (v.1 24/02/20)
    implementation: François Bechet (v.1 01/03/20)
    """
    # create the players
    players = (input("who is player1 : "), input("who is player2 : "))

    # create dict_recruit
    dict_recruit = {players[0]: {'cruiser': {'ship_type': 'cruiser',
                                             'hp': 100,
                                             'current_energy': 200,
                                             'energy_capacity': 400,
                                             'shooting_range': 1,
                                             'move_cost': 10,
                                             'shooting_cost': 10,
                                             'cost': 750,
                                             'turn_attack': False,
                                             'move': False},
                                 'tanker': {'ship_type': 'tanker',
                                            'hp': 50,
                                            'current_energy': 400,
                                            'energy_capacity': 600,
                                            'move_cost': 0,
                                            'cost': 1000,
                                            'move': False},
                                 'research': {'regeneration': 0,
                                              'storage': 0,
                                              'range': 0,
                                              'move': 0}},
                    players[1]: {'cruiser': {'ship_type': 'cruiser',
                                             'hp': 100,
                                             'current_energy': 200,
                                             'energy_capacity': 400,
                                             'shooting_range': 1,
                                             'move_cost': 10,
                                             'shooting_cost': 10,
                                             'cost': 750,
                                             'turn_attack': False,
                                             'move': False},
                                 'tanker': {'ship_type': 'tanker',
                                            'hp': 50,
                                            'current_energy': 400,
                                            'energy_capacity': 600,
                                            'move_cost': 0,
                                            'cost': 1000,
                                            'move': False},
                                 'research': {'regeneration': 0,
                                              'storage': 0,
                                              'range': 0,
                                              'move': 0}}}

    # call the create_board function and store its return values
    board_values = create_board("board.txt", players)
    dict_board, height, width = board_values[0], board_values[1], board_values[2]

    # create dictionnary of the army
    dict_army = board_values[3]

    # call the display_board function
    display_board(dict_board, height, width, players, dict_army)

    # initialize peace
    peace = 0

    # start the main game loop
    """ while play_game is not False:
        try:
            peace = play_turn(dict_board, dict_army, dict_recruit, width, height, players, peace)
        except Exception:
            print("One of the players entered a bad order") """
    while play_game is not False:
        peace = play_turn(dict_board, dict_army, dict_recruit, width, height, players, peace)


def get_order(players, dict_army, dict_board):
    """ask the player for orders

    Orders must respect this syntax :
        RECRUIT ORDER : 'alpha:tanker bravo:cruiser'
        UPGRADE ORDER : 'upgrade:regeneration; upgrade:storage; upgrade:shooting_range; upgrade:move_cost'
        MOVE ORDER(name:@r-c where r is row and c is column) : 'alpha:@30-31'
        ATTACK ORDER(nom:*r-c=q where r,c is position of target and q are damages) : 'charlie:*10-15=23'
        TRANSFER ORDER(nom:<r-c where the tanker take energy in the targeted hub; name1:>name2 where name1(tanker) gives energy to name2(cruiser or hub)) : alpha:<30-31 bravo:>charlie delta:>hub

    parameters
    ----------
    players: names of the players(tuple)

    return
    ------
    dict_order: dictionnary with all the order

    Version
    −−−−−−−
    specification: Dominik Everaert (v.3 24/02/20)
    implementation: François Bechet (v.1 01/03/20)
    """

    # convert list_oder to dict_order
    dict_order = {players[0]: {'move': [], 'attack': [], 'upgrade': [], 'recruit': [], 'transfer': []},
                  players[1]: {'move': [], 'attack': [], 'upgrade': [], 'recruit': [], 'transfer': []}}

    # ask orders to players and add them to dict_order
    print(dict_army)
    for player in players:
        if player != 'ai':
            list_order_player = (input("%s, please enter your orders : " % player)).split()
        else:
            list_order_player = ai(dict_army, dict_board, players)
        for i in range(len(list_order_player)):
            if '@' in list_order_player[i]:
                dict_order[player]['move'].append(list_order_player[i])
            elif '*' in list_order_player[i]:
                dict_order[player]['attack'].append(list_order_player[i])
            elif 'upgrade' in list_order_player[i]:
                dict_order[player]['upgrade'].append(list_order_player[i])
            elif '>' in list_order_player[i] or '<' in list_order_player[i]:
                dict_order[player]['transfer'].append(list_order_player[i])
            else:
                dict_order[player]['recruit'].append(list_order_player[i])

    # return dictionnary of orders
    print(dict_order)
    return dict_order


def create_board(board_file, players):
    """take a file and change it into a board

    parameters
    ----------
    board_file: file in which all the element needed for the board are(path)
    players: names of the players(tuple)

    return
    ------
    dict_board: dictionnary with all the characteristic of the board (dict)

    Version
    −−−−−−−
    specification: Dominik Everaert (v.3 24/02/20)
    implementation: François Bechet (v.1 01/03/20)
    """

    # open the board file and save its content
    with open(board_file, "r") as f:
        data = f.readlines()

    # create a dict and store all board file infos into it
    dictFile = {}
    for i in data:
        if ':' in i:
            for j in range(len(i)):
                if i[j] == ':':
                    index = j
            key = i[:index]
            dictFile[key] = []
        else:
            dictFile[key].append(i.split())

    # get map width and height
    width, height = int(dictFile['map'][0][0]), int(dictFile['map'][0][1])

    # create a dictionnary of the board with keys as cases
    dict_board = {}
    for x in range(width):
        for y in range(height):
            dict_board['@%d-%d' % (x + 1, y + 1)] = {}

    # add hubs to the board's dictionnary
    dict_board['@%d-%d' % (int(dictFile['hubs'][0][0]), int(dictFile['hubs'][0][1]))] = {players[0]: {'hub': ''}}
    dict_board['@%d-%d' % (int(dictFile['hubs'][1][0]), int(dictFile['hubs'][1][1]))] = {players[1]: {'hub': ''}}

    # create dict_army
    hub_1 = {'hp': int(dictFile['hubs'][0][2]), 'current_energy': int(dictFile['hubs'][0][3]), 'energy_capacity': int(dictFile['hubs'][0][3]), 'regeneration': int(dictFile['hubs'][0][4]), 'ship_type': 'hub'}
    hub_2 = {'hp': int(dictFile['hubs'][1][2]), 'current_energy': int(dictFile['hubs'][1][3]), 'energy_capacity': int(dictFile['hubs'][1][3]), 'regeneration': int(dictFile['hubs'][1][4]), 'ship_type': 'hub'}
    dict_army = {players[0]: {'hub': hub_1}, players[1]: {'hub': hub_2}}

    # add peaks to the board's dictionnary
    for i in range(len(dictFile['peaks'])):
        dict_board['@%d-%d' % (int(dictFile['peaks'][i][0]), int(dictFile['peaks'][i][1]))] = {'peak': {'energy': int(dictFile['peaks'][i][2])}}

    # returns
    return dict_board, height, width, dict_army


def attack(dict_order, dict_army, dict_board, players, peace):
    """execute attack order of each player and modify stats of each effected unit

    parameters
    ----------
    dict_order[attack]: dictionnary of attack order(dict)
    dict_army: dictionnary with the unit of the two player(dict)
    players: names of the players(tuple)
    peace : number of turn wihout damage (int)

    return
    ------
    dict_army: dictionnary of the 2 army modified in result of the attack(dict)
    dict_board: dictionnary with all the characteristic of the board (dict)
    peace : number of turn wihout damage (int)
    Version
    −−−−−−−
    specification: Dominik Everaert (v.4 24/02/20)
    implementation : Dominik Everaert (v.2 11/03/20)
    """
    # extract the attack order from dict_order and change unit stat
    total_damage = 0
    attackList = ''
    shooting_range = 0
    x_shooter, y_shooter, x_target, y_target = '', '', '', ''
    for player in players:
        if player == players[0]:
            attacker = players[0]
            target = players[1]
        else:
            attacker = players[1]
            target = players[0]
        # extract the attack order
        for i in range(len(dict_order[attacker]['attack'])):
            attack = dict_order[attacker]['attack'][i]
        # change order into list [shooter_name,attack_stats]
            attackList = attack.split(':*')
        # separate attack_stats into position and damage
            spliting = attackList[1].split('=')
            shooter_name = attackList[0]
            damage = int(spliting[1])
            target_position = spliting[0]
        # separate position_target into target x et target y
            targetxy = target_position.split('-')
        # separate target position
            x_target = int(targetxy[0])
            y_target = int(targetxy[1])

            target_units = []
            for unit in dict_board['@%s-%s' % (x_target, y_target)][target]:
                target_units.append(unit)
       
        # search shooter range
        shooting_range = dict_army[player][shooter_name]['shooting_range']

        # search shooter position
            for key, value in dict_board.items():
                if attacker in value:
                    unit = value[attacker]
                    if attackList[0] in unit:
                        case = key.split('-')
                        case_0 = case[0].strip('@')
                        x_shooter, y_shooter = int(case_0), int(case[1])
        # execute the attack
            # check manhattan distance and check that that the unit has enough energy to attack
            if compute_manhattan_distance(x_shooter, y_shooter, x_target, y_target,shooting_range) and dict_army[attacker][shooter_name]['current_energy'] >= 10 * damage:
                dict_army[attacker][shooter_name]['current_energy'] -= 10 * damage
                for i in target_units:
                    # change the unit hp : hp = hp - damage
                    dict_army[target][i]['hp'] -= damage
                    total_damage += damage
        # if it's a cruiser disable his move ability for the turn
            if dict_army[attacker][attackList[0]]['ship_type'] == 'cruiser':
                dict_army[attacker][attackList[0]]['turn_attack'] = True

        # delete the unit if damage is >= unit hp

        for ship in dict_army[player]:
            if dict_army[player][ship]['hp'] <= 0:
                # if the unit is the hub the attacker win
                if ship == 'hub':
                    if player == players[0]:
                        winner = players[1]
                    else:
                        winner = players[0]
                    return('win', winner)
                else:
                    del dict_army[player][ship]
                    # if there is only one unit delete the player key
                    for case, value in dict_board.items():
                        if ship in dict_board[case][player]:
                            if len(dict_board[case][player]) == 1:
                                del dict_board[case][player]
                                # else delete only the unit key
                            else:
                                del dict_board[case][player][ship]
    if total_damage == 0:
        peace += 1
    return dict_board, dict_army, peace


def move(dict_order, dict_board, dict_army, players):
    """execute move order of each player and modify board and stats of moving units

    prameters
    ---------
    dict_order[move]: dictionnary of move order(dict)
    dict_board: dictionnary with all the characteristic of the board (dict)
    dict_army: dictionnary with the unit of the two player(dict)
    players: names of the players(tuple)

    return
    ------
    dict_board: dictionnary with all the characteristic of the board (dict)

    Version
    −−−−−−−
    specification: François Bechet (v.3 24/02/20)
    implementation: François Bechet (v.1 25/02/20)
    """
    # extract the move order from dict_order and change the position unit in dict_board
    for player in players:
        moveList = []
        # extract the move order
        for i in range(len(dict_order[player]['move'])):
            move = dict_order[player]['move'][i]
            moveList = move.split(':')

            if moveList != []:
                # check manhattan distance
                x_shooter, y_shooter, x_target, y_target = 0, 0, 0, 0
                xy_shooter = ''
                moveLegality = True

                # destination correspond to target
                case = moveList[1].split('-')
                case_0 = case[0].strip('@')
                x_target, y_target = int(case_0), int(case[1])
                # unit to move correspond to shooter
                unit = ''
                for key, value in dict_board.items():
                    if player in value:
                        if moveList[0] in value[player]:
                            unit = value[player]
                            xy_shooter = key  # store unit position to delete it after the move
                            case = key.split('-')
                            case_0 = case[0].strip('@')
                            x_shooter, y_shooter = int(case_0), int(case[1])
                # verify that the unit didn't already moved this turn
                if dict_army[player][moveList[0]]['move']:
                    moveLegality = False
                # verify that the cruiser didn't already attacked this turn
                if dict_army[player][moveList[0]]['ship_type'] == 'cruiser':
                    if dict_army[player][moveList[0]]['turn_attack']:
                        moveLegality = False
                # check manhattan distance and moveLegality
                if compute_manhattan_distance(x_shooter, y_shooter, x_target, y_target) and moveLegality:
                    # move the unit position in dict_board
                    # change the position of the unit in dict_board
                    unit = unit[moveList[0]]
                    if player not in dict_board[moveList[1]]:
                        tempDict = {player: {moveList[0]: {}}}
                        tempDict[player][moveList[0]].update(unit)
                        dict_board[moveList[1]].update(tempDict)
                    else:
                        tempDict = {moveList[0]: {}}
                        tempDict[moveList[0]].update(unit)
                        dict_board[moveList[1]][player].update(tempDict)
                    # set move to True so unit only move one time each turn
                    dict_army[player][moveList[0]]['move'] = True
                    # delete the old unit position
                    # if there is only one unit, also delete the player key
                    if len(dict_board[xy_shooter][player]) == 1:
                        del dict_board[xy_shooter][player]
                    # else, delete only the unit key
                    else:
                        del dict_board[xy_shooter][player][moveList[0]]
                    # make the cruiser pay  the move
                    if dict_army[player][moveList[0]]['ship_type'] == 'cruiser':
                        move_cost = dict_army[player][moveList[0]]['move_cost']
                        dict_army[player][moveList[0]]['current_energy'] -= move_cost
        # restore units move properties so they can move again next turn
        for unit, value in dict_army[player].items():
            for property in dict_army[player][unit]:
                # restore move so unit can move again next turn
                if property == 'move':
                    dict_army[player][unit][property] = False
                # restore cruiser move legality
                if property == 'turn_attack':
                    dict_army[player][unit][property] = False
    return dict_board


def upgrade(dict_order, dict_army, dict_recruit, players):
    """execute the upgrage order of each player and modify the stats of each affected unit

    parameters
    ----------
    dict_order[upgrade]: dictionnary of upgrade order(dict)
    dict_army: dictionnary with the unit of the two player(dict)
    dict_recruit: dictionnary with research and stat of new ship(dict)
    players: names of the players(tuple)

    return
    ------
    dict_army: dictionnary with the unit of the two player(dict)
    dict_recruit: dictionnary with research and stat of new ship(dict)

    Version
    −−−−−−−
    specification: François Bechet (v.2 24/02/20)
    implementation: Dominik Everaert (v.1 05/03/20)
    """
    # extract the upgrade order from dict_order and change the stat of unit
    for player in players:
        upgradeList = ''
        # extract the upgrade order
        for i in range(len(dict_order[player]['upgrade'])):
            upgrade = dict_order[player]['upgrade'][i]
            upgradeList = upgrade.split(':')
            upgradeList.append(player)
        # choose which upgrade must be done
        if upgradeList != '':
            if upgradeList[1] == 'regeneration':
                if (dict_army[player]['hub']['current_energy']) >= 750 and (dict_recruit[player]['research']['regeneration']) < 10:
                    dict_army[player]['hub']['regeneration'] += 5
                    dict_army[player]['hub']['current_energy'] -= 750
                    dict_recruit[player]['research']['regeneration'] += 1
                else:
                    print("you can't upgrade energy regeneration")

            elif upgradeList[1] == 'storage':
                if (dict_army[player]['hub']['current_energy']) >= 600 and (dict_recruit[player]['research']['storage']) < 12:
                    dict_recruit[player]['research']['storage'] += 1
                    dict_army[player]['hub']['current_energy'] -= 600
                    dict_recruit[player]['tanker']['energy_capacity'] += 100
                    temp_dict = list(dict_army[player])
                    for i in range(len(temp_dict)):
                        if dict_army[player][temp_dict[i]]['ship_type'] == 'tanker':
                            dict_army[player][temp_dict[i]]['energy_capacity'] += 100
                else:
                    print("you can't upgrade energy capacity")

            elif upgradeList[1] == 'range':
                if (dict_army[player]['hub']['current_energy']) >= 400 and (dict_recruit[player]['research']['range']) < 5:
                    dict_recruit[player]['research']['range'] += 1
                    dict_army[player]['hub']['current_energy'] -= 400
                    dict_recruit[player]['cruiser']['shooting_range'] += 1
                    temp_dict = list(dict_army[player])
                    for i in range(len(temp_dict)):
                        if dict_army[player][temp_dict[i]]['ship_type'] == 'cruiser':
                            dict_army[player][temp_dict[i]]['shooting_range'] += 1
                else:
                    print("you can't upgrade shooting range")

            elif upgradeList[1] == 'move':
                if (dict_army[player]['hub']['current_energy']) >= 500 and (dict_recruit[player]['research']['move']) < 5:
                    dict_recruit[player]['research']['move'] += 1
                    dict_army[player]['hub']['current_energy'] -= 500
                    dict_recruit[player]['cruiser']['move_cost'] -= 1
                    temp_dict = list(dict_army[player])
                    for i in range(len(temp_dict)):
                        if dict_army[player][temp_dict[i]]['ship_type'] == 'cruiser':
                            dict_army[player][temp_dict[i]]['move_cost'] -= 1
                else:
                    print("you can't upgrade movement")

    return dict_army, dict_recruit


def energy_transfert(dict_army, dict_order, dict_board, players):
    """execute transfert order and modify affected unit's stat

    parameters
    ----------
    dict_army: dictionnary with the unit of the two player(dict)
    dict_order[energy_transfert]:dictionnary of energy transfert order(dict)
    dict_board: dictionnary with all the characteristic of the board (dict)
    players: names of the players(tuple)

    return
    ------
    dict_army: dictionnary with the unit of the two player(dict)
    dict_board: dictionnary with all the characteristic of the board (dict)

    Version
    −−−−−−−
    specification: Dominik Everaert (v.3 24/02/20)
    implementation : François Bechet (v.1 10/03/20)
    """
    for player in players:
        order_peak = []
        order_unit = []
        order_hub = []
        tempList = []
        # extract order from dict_order and place each kind of transfert order in a specific list
        tempList = dict_order[player]['transfer']
        for i in range(len(tempList)):
            temp_order = tempList[i]
            if ':<' in temp_order:
                order_peak = temp_order.split(':<')
            elif ':>' in temp_order:
                order_unit = temp_order.split(':>')
            elif '>:' in temp_order:
                order_hub = temp_order.split('>:')

        # execute peak to unit transfert
        if order_peak != []:
            energy_unit = dict_army[player][order_peak[0]]['energy_capacity'] - dict_army[player][order_peak[0]]['current_energy']
            if energy_unit >= dict_board['@' + order_peak[1]]['peak']['energy']:
                energy = dict_board['@' + order_peak[1]]['peak']['energy']
            else:
                energy = energy_unit
            dict_board['@' + order_peak[1]]['peak']['energy'] -= energy
            dict_army[player][order_peak[0]]['current_energy'] += energy

            # if peak's energy reach 0, remove the peak
            if dict_board['@' + order_peak[1]]['peak']['energy'] == 0:
                del dict_board['@' + order_peak[1]]['peak']

        # execute unit to unit transfert
        if order_unit != []:
            energy_unit = dict_army[player][order_unit[1]]['energy_capacity'] - dict_army[player][order_unit[1]]['current_energy']
            if energy_unit >= dict_army[player][order_unit[0]]['current_energy']:
                energy = dict_army[player][order_unit[0]]['current_energy']
            else:
                energy = energy_unit
            dict_army[player][order_unit[0]]['current_energy'] -= energy
            dict_army[player][order_unit[1]]['current_energy'] += energy

        # execute unit to hub transfert
        if order_hub != []:
            # the hub must not be full
            energy_hub = dict_army[player][order_hub[1]]['energy_capacity'] - dict_army[player][order_hub[1]]['current_energy']
            if energy_hub >= dict_army[player][order_hub[0]]['current_energy']:
                energy = dict_army[player][order_hub[0]]['current_energy']
            else:
                energy = energy_hub

            # do the energy transfert
            dict_army[player][order_hub[0]]['current_energy'] -= energy
            dict_army[player][order_hub[1]]['current_energy'] += energy

    return dict_army, dict_board


def regenerate(dict_army, players):
    """makes hub regenerate energy(at the end of the turn)

    parameters
    ----------
    dict_army: dictionnary with the unit of the two player(dict)
    players: names of the players(tuple)

    return
    ------
    dict_army: dictionnary with the unit of the two player(dict)

    Version
    −−−−−−−
    specification: Dominik Everaert (v.2 24/02/20)
    implementation : Dominik Everaert (v.1 13/03/20)
    """
    for player in players:
        regen = dict_army[player]['hub']['regeneration']
        empty = dict_army[player]['hub']['energy_capacity'] - dict_army[player]['hub']['current_energy']
        if empty < regen:
            regen = empty
        dict_army[player]['hub']['current_energy'] += regen
    return dict_army


def recruit_units(dict_order, dict_army, players, dict_board, dict_recruit):
    """execute recruit order and add unit to the army

    parameters
    ----------
    dict_army: dictionnary with the unit of the two player(dict)
    dict_recruit: dictionnary with research and stat of new ship(dict)
    dict_order[recruit]: dictionnary of upgrade order(dict)
    players: names of the players(tuple)

    return
    ------
    dict_army: dictionnary with the unit of the two player(dict)

    Version
    −−−−−−−
    specification: Dominik Everaert (v.3 24/02/20)
    implementation: François Bechet (v.1 01/03/20)
    """

    # create a deepcopy of dict_recruit because otherwise it would point to the same object and cause issues later
    dict_recruit_copy = copy.deepcopy(dict_recruit)

    # extract the units from dict_order and place them into dict_board and dict_army
    for player in players:
        # find the hub case
        hub_case = ''
        for case, properties in dict_board.items():
            if player in properties:
                for unit in dict_board[case][player]:
                    if unit == 'hub':
                        hub_case = case
        # extract the order from dict_order
        for i in range(len(dict_order[player]['recruit'])):
            unit = dict_order[player]['recruit'][i]
            unitList = unit.split(':')
            # check that the unit name doesn't already exists
            if unitList[0] not in dict_army[player]:
                buy = False
                # check that the player hub has enough energy to buy the unit
                if unitList[1] == 'cruiser':
                    if dict_army[player]['hub']['current_energy'] > dict_recruit_copy[player]['cruiser']['cost']:
                        buy = True
                elif unitList[1] == 'tanker':
                    if dict_army[player]['hub']['current_energy'] > dict_recruit_copy[player]['tanker']['cost']:
                        buy = True

                if buy:
                    # add the unit to dict_board
                    unitDict = {unitList[0]: {'ship_type': unitList[1]}}
                    dict_board[hub_case][player].update(unitDict)
                    # add the unit to dict_army and pay the unit price
                    if unitList[0] not in dict_army[player]:  # verify that the unit is not already in dict_army
                        if 'cruiser' in unitList:
                            dict_army[player][unitList[0]] = dict_recruit_copy[player]['cruiser']
                            dict_army[player]['hub']['current_energy'] -= dict_recruit_copy[player]['cruiser']['cost']
                        elif 'tanker' in unitList:
                            dict_army[player][unitList[0]] = dict_recruit_copy[player]['tanker']
                            dict_army[player]['hub']['current_energy'] -= dict_recruit_copy[player]['tanker']['cost']

    return dict_army, dict_board


def compute_manhattan_distance(x_shooter, y_shooter, x_target, y_target,shooting_range=1):
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
    specification: François Bechet (v.1 24/02/20)
    implementation: François Bechet (v.1 12/03/20)
    """
    # formula : max( |r2−r1| , |c2−c1| )
    x = abs(x_shooter - x_target)
    y = abs(y_shooter - y_target)
    if max(x, y) <= shooting_range:
        return True


def play_turn(dict_board, dict_army, dict_recruit, width, height, players, peace):
    """ manage each turn of the game by receiving the commands of each player

    Parameters
    ----------
    dict_army: dictionnary with the unit of the two player(dict)
    dict_order:dictionnary of players orders(dict)
    dict_board: dictionnary with all the characteristic of the board (dict)
    dict_recruit: dictionnary with research and stat of new ship(dict)
    players: names of the players(tuple)
    peace : number of turn wihout damage (int)

    Version
    -------
    specification: François Bechet (v.2 24/02/20)
    implementation: François Bechet (v.1 13/03/20)
    """
    # get players orders
    dict_order = get_order(players, dict_army, dict_board)
    # call all functions to execute the player's orders
    recruit_units(dict_order, dict_army, players, dict_board, dict_recruit)
    upgrade(dict_order, dict_army, dict_recruit, players)
    # check if the hub is destroyed
    # if the hub is destroyed stop the game
    win_condition = attack(dict_order, dict_army, dict_board, players, peace)
    if win_condition[0] == 'win':
        print('the winner is %s' % win_condition[1])
        game(False)
    if win_condition[2] == 40:
        print("There was no attack during 40 turns so the game ended.")
        game(False)
    move(dict_order, dict_board, dict_army, players)
    energy_transfert(dict_army, dict_order, dict_board, players)
    regenerate(dict_army, players)
    display_board(dict_board, height, width, players, dict_army)
    return win_condition[2]


def ai(dict_army, dict_board, players):
    # find enemy
    if players[0] == 'ia':
        enemy = players[1]
    else:
        enemy = players[0]

    ai_orders = []
    # recruit unit
    unit_list = ['Alfa', 'Bravo', 'Charlie', 'Delta', 'Echo', 'Foxtrot', 'Golf', 'Hotel', 'India', 'Juliett', 'Kilo', 'Lima', 'Mike', 'November', 'Oscar', 'Papa', 'Quebec', 'Romeo', 'Sierra', 'Tango', 'Uniform', 'Victor', 'Whiskey', 'X-ray', 'Yankee', 'Zulu']
    unit_name = unit_list[random.randint(0, (len(unit_list)) - 1)]
    unit_type_list = ['tanker', 'cruiser']
    unit_type = unit_type_list[random.randint(0, (len(unit_type_list)) - 1)]
    recruit_order = "%s:%s" % (unit_name, unit_type)
    ai_orders.append(recruit_order)

    # move
    list_unit = []
    for unit in dict_army['ai']:
        if unit != 'hub':
            list_unit.append(unit)
    enemy_hub_case = []
    # find the enemy hub case
    for unit in list_unit:
        for case, properties in dict_board.items():
            if enemy in properties:
                for unit in dict_board[case][enemy]:
                    if unit == 'hub':
                        enemy_hub_case = case.split('-')
                        case_x = enemy_hub_case[0].strip('@')
                        case_y = enemy_hub_case[1]
                        enemy_hub_case = [case_x, case_y]
    # move the unit to it's target
    for case, properties in dict_board.items():
        if 'ai' in properties:
            for unit in dict_board[case]['ai']:
                if unit != 'hub':
                    # save unit case
                    unit_case = case.split('-')
                    case_y = unit_case[1]
                    case_x = unit_case[0].strip('@')
                    unit_case = [case_x, case_y]
                    # find the case to move to
                    # case_x
                    if enemy_hub_case[0] > unit_case[0]:
                        case_x = int(unit_case[0]) - 1
                    elif enemy_hub_case[0] < unit_case[0]:
                        case_x = int(unit_case[0]) + 1
                    else:
                        case_x = enemy_hub_case[0]
                    # case_y
                    if enemy_hub_case[1] > unit_case[1]:
                        case_y = int(unit_case[1]) - 1
                    elif enemy_hub_case[1] < unit_case[0]:
                        case_y = int(unit_case[1]) + 1
                    else:
                        case_y = enemy_hub_case[1]
                    move_order = '%s:@%s-%s' % (unit, case_x, case_y)
                    ai_orders.append(move_order)
    # attack
    # upgrade

    # ai_orders.append(move_order)
    # return all the orders
    print(ai_orders)
    return(ai_orders)


# Start the game
game(True)
