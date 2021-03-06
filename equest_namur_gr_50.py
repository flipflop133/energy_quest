# imports
import copy

import colored

import AI_gr_50
import remote_play


def game(board_path,
         local_player,
         remote_id='ai',
         remote_ip='127.0.0.1',
         local_ai=False,
         colored_display=True,
         play_game=True):
    """start the game and play it
    paramater
    ---------
    board_path : path to the board file(str)
    local_player : id of your group (int, optional)
    remote_id : id of the other group(int, optional)
    remote_ip : IP address where the referee or the other group is(str, optional)
    colored_display : enable or display colors for the display(bool)

    Version
    −−−−−−−
    specification: François Bechet (v.2 24/02/20)
    implementation: François Bechet (v.2 01/03/20)
    """
    # create the players
    players = [str(local_player), str(remote_id)]

    # establish connection if player2 is a remote player
    if 'ai' not in players[1]:
        connection = remote_play.create_connection(local_player, remote_id,
                                                   remote_ip, True)
    else:
        connection = ''
    # case when we play in remote with our ai
    if local_ai:
        players[0] = 'ai'

    # create dict_recruit
    temp_dict = {
        'cruiser': {
            'ship_type': 'cruiser',
            'hp': 100,
            'current_energy': 400,
            'energy_capacity': 400,
            'shooting_range': 1,
            'move_cost': 10,
            'shooting_cost': 10,
            'cost': 750,
            'turn_attack': False,
            'move': False
        },
        'tanker': {
            'ship_type': 'tanker',
            'hp': 50,
            'current_energy': 600,
            'energy_capacity': 600,
            'move_cost': 0,
            'cost': 1000,
            'move': False
        },
        'research': {
            'regeneration': 0,
            'storage': 0,
            'range': 0,
            'move': 0
        }
    }
    dict_recruit = {players[0]: temp_dict, players[1]: temp_dict}

    # create dict_memory for the ai
    dict_memory = {'orders': {}, 'data': {}}

    # call the create_board function and store its return values
    board_values = create_board(board_path, players)
    dict_board, height, width = board_values[0], board_values[1], board_values[
        2]

    # create dictionnary of the army
    dict_army = board_values[3]

    # call the display_board function
    display_board(dict_board, height, width, players, dict_army,
                  colored_display)

    # initialize peace
    peace = 0

    # start the main game loop
    """ while play_game:
        try:
            peace, play_game = play_turn(dict_board, dict_army, dict_recruit,
                                         dict_memory, width, height, players,
                                         peace, connection, colored_display,
                                         play_game)
        except Exception:
            print("One of the players entered a bad order") """
    while play_game:
        peace, play_game = play_turn(dict_board, dict_army, dict_recruit,
                                     dict_memory, width, height, players,
                                     peace, connection, colored_display,
                                     play_game)


def create_board(board_file, players):
    """take a file and change it into a board

    parameters
    ----------
    board_file: file in which all the element needed for the board are(path)
    players: names of the players(tuple)

    return
    ------
    dict_board: dictionnary with all the characteristic of the board (dict)
    height: height of the board(int)
    width: width of the board(int)
    dict_army: dictionnary with the unit of the two player(dict)

    Version
    −−−−−−−
    specification: Dominik Everaert (v.3 24/02/20)
    implementation: François Bechet (v.1 01/03/20)
    """

    # open the board file and save its content
    with open(board_file, "r") as f:
        data = f.readlines()

    # create a dict and store all board file infos into it
    dict_file = {}
    for i in data:
        if ':' in i:
            for j in range(len(i)):
                if i[j] == ':':
                    index = j
            key = i[:index]
            dict_file[key] = []
        else:
            dict_file[key].append(i.split())

    # get map width and height
    width, height = int(dict_file['map'][0][0]), int(dict_file['map'][0][1])

    # create a dictionnary of the board with keys as cases
    dict_board = {}
    case = '@%d-%d'
    for x in range(width):
        for y in range(height):
            dict_board[case % (x + 1, y + 1)] = {}

    # add hubs to the board's dictionnary
    dict_board[case % (int(
        dict_file['hubs'][0][0]), int(dict_file['hubs'][0][1]))] = {
            players[0]: {
                'hub': ''
            }
        }
    dict_board[case % (int(
        dict_file['hubs'][1][0]), int(dict_file['hubs'][1][1]))] = {
            players[1]: {
                'hub': ''
            }
        }

    # create dict_army
    hub_1 = {
        'hp': int(dict_file['hubs'][0][2]),
        'current_energy': int(dict_file['hubs'][0][3]),
        'energy_capacity': int(dict_file['hubs'][0][3]),
        'regeneration': int(dict_file['hubs'][0][4]),
        'ship_type': 'hub'
    }
    hub_2 = {
        'hp': int(dict_file['hubs'][1][2]),
        'current_energy': int(dict_file['hubs'][1][3]),
        'energy_capacity': int(dict_file['hubs'][1][3]),
        'regeneration': int(dict_file['hubs'][1][4]),
        'ship_type': 'hub'
    }
    dict_army = {players[0]: {'hub': hub_1}, players[1]: {'hub': hub_2}}

    # add peaks to the board's dictionnary
    for i in range(len(dict_file['peaks'])):
        dict_board[case % (int(
            dict_file['peaks'][i][0]), int(dict_file['peaks'][i][1]))] = {
                'peak': {
                    'energy': int(dict_file['peaks'][i][2])
                }
            }

    # returns
    return dict_board, height, width, dict_army


def display_board(dict_board, height, width, players, dict_army,
                  colored_display):
    """display the board at the beginning of the game

    parameters
    ----------
    dict_board: dictionnary with all the characteristic of the board (dict)
    height: height of the board(int)
    width: width of the board(int)
    players: names of the players(tuple)
    colored_display: enable or display colors for the display(bool)

    Version
    −−−−−−−
    specification: Dominik Everaert (v.3 24/02/20)
    implementation: François Bechet (v.2 01/03/20)
    """
    # define colored colors
    if colored_display:
        default_color = colored.attr('reset')
        green = colored.fg('#00ff00')
        red = colored.fg('#ff0000')
        gold = colored.fg('#ffbd00')
        blue = colored.bg('#006994')
        white = colored.fg('#ffffff')
        grey = colored.fg('#999999')
        cyan = colored.fg('#118ab2')
    else:
        default_color = ''
        green = ''
        red = ''
        gold = ''
        blue = ''
        white = ''
        grey = ''
        cyan = ''

    # display game's header
    print(cyan + "################")
    print("# ENERGY QUEST #")
    print("################" + default_color)

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
    units_positions = {}
    case_name = '@%d-%d'
    for x in range(width):
        n = 1
        for y in range(height):
            # set case
            case = case_name % (x + 1, y + 1)
            # if there is more than one unit on the case, display dice's faces
            multiple_elements = False
            if len(dict_board[case]) > 1:
                multiple_elements = True
            if players[0] in dict_board[case] and len(
                    dict_board[case][players[0]]) > 1:
                multiple_elements = True
            if players[1] in dict_board[case] and len(
                    dict_board[case][players[1]]) > 1:
                multiple_elements = True
            if multiple_elements:
                # add elements to dict armies
                armies[case] = []
                for element in dict_board[case]:
                    if element == 'peak':
                        armies[case].append(element)
                    elif element == players[0]:
                        for unit in dict_board[case][element]:
                            armies[case].append(unit)
                    elif element == players[1]:
                        for unit in dict_board[case][element]:
                            armies[case].append(unit)
                # display dice's faces
                if len(armies[case]) == 2:
                    print(white + blue + ' ⚁ ', end='' + default_color)
                elif len(armies[case]) == 3:
                    print(white + blue + ' ⚂ ', end='' + default_color)
                elif len(armies[case]) == 4:
                    print(white + blue + ' ⚃ ', end='' + default_color)
                elif len(armies[case]) == 5:
                    print(white + blue + ' ⚄ ', end='' + default_color)
                else:
                    print(white + blue + ' ⚅ ', end='' + default_color)
            # if there is only one unit on the case
            else:
                units_positions[case] = []
                for element in dict_board[case]:
                    if element == 'peak':
                        units_positions[case].append(element)
                    elif element == players[0]:
                        for unit in dict_board[case][element]:
                            units_positions[case].append(unit)
                    elif element == players[1]:
                        for unit in dict_board[case][element]:
                            units_positions[case].append(unit)
                # display player0 hub and units
                if players[0] in dict_board[case_name % (x + 1, y + 1)]:
                    temp_dict = dict_board[case_name %
                                           (x + 1, y + 1)][players[0]]
                    if 'hub' in temp_dict:
                        print(green + blue + ' ⌂ ' + default_color, end='')
                    else:
                        for key in temp_dict:
                            unit = temp_dict[key]
                            if 'cruiser' in unit['ship_type']:
                                print(green + blue + ' ✈ ' + default_color,
                                      end='')
                            if 'tanker' in unit['ship_type']:
                                print(green + blue + ' ⛴ ' + default_color,
                                      end='')
                # display player1 hub and units
                elif players[1] in dict_board[case_name % (x + 1, y + 1)]:
                    temp_dict = dict_board[case_name %
                                           (x + 1, y + 1)][players[1]]
                    if 'hub' in temp_dict:
                        print(red + blue + ' ⌂ ' + default_color, end='')
                    else:
                        for key in temp_dict:
                            unit = temp_dict[key]
                            if 'cruiser' in unit['ship_type']:
                                print(red + blue + ' ✈ ' + default_color,
                                      end='')
                            if 'tanker' in unit['ship_type']:
                                print(red + blue + ' ⛴ ' + default_color,
                                      end='')
                # display peaks
                elif 'peak' in dict_board[case_name % (x + 1, y + 1)]:
                    if len(dict_board[case_name % (x + 1, y + 1)]) == 1:
                        print(gold + blue + ' ☢ ' + default_color, end='')
                    else:
                        case = str(x + 1) + ':' + str(y + 1)
                        armies[case] = {}
                        armies[case].update(dict_board[case_name %
                                                       (x + 1, y + 1)])
                        if len(temp_dict) == 2:
                            print(green + ' ⚁ ' + default_color, end='')
                        elif len(temp_dict) == 3:
                            print(green + ' ⚂ ' + default_color, end='')
                        elif len(temp_dict) == 4:
                            print(green + ' ⚃ ' + default_color, end='')
                        elif len(temp_dict) == 5:
                            print(green + ' ⚄ ' + default_color, end='')
                        else:
                            print(green + ' ⚅ ' + default_color, end='')
                # display cases
                else:
                    print(grey + blue + " . " + default_color, end='')
        n = n + x
        print(' ' + str(n))

    # display armies (more than one unit on a case)
    if armies != {}:
        print(gold + '\nARMIES' + default_color)
        for case in armies:
            print('case:', case + ':')
            for unit in armies[case]:
                print(unit)

    # display the other units positions
    print(gold + '\nUNITS POSITIONS' + default_color)
    i = 0
    for key, value in units_positions.items():
        if not (value == []) and 'hub' not in value and 'peak' not in value:
            i += 1
            print(str(key) + str(value), end='  ▍ ')
            if i % 5 == 0:  # go to the next line every 5 peaks
                print('\n')

    # display the energy peaks
    print(gold + '\nENERGY PEAKS' + default_color)
    i = 0
    for case in dict_board:
        if 'peak' in dict_board[case]:
            i += 1
            print(('peak%s') % (case), end=' ')
            print('energy :', dict_board[case]['peak']['energy'], end='  ▍ ')
            if i % 5 == 0:  # go to the next line every 5 peaks
                print('\n')
    print('\n')
    # display the players units and hubs
    for player in players:
        for x in range(width):
            n = 1
            for y in range(height):
                # set case
                case = case_name % (x + 1, y + 1)

        if player == players[0]:
            print(green + player + default_color + ' : ')
        else:
            print(red + player + default_color + ' : ')
        for unit, value in dict_army[player].items():
            print(unit.upper(), end=' ⇒ ')
            for property, value in dict_army[player][unit].items():
                if property != 'turn_attack' and property != 'move':  # player don't need to see these properties
                    print(property, ':', value, end=' ▍')
            print('')
        print('\n')


def play_turn(dict_board, dict_army, dict_recruit, dict_memory, width, height,
              players, peace, connection, colored_display, play_game):
    """ manage each turn of the game by receiving the commands of each player

    Parameters
    ----------
    dict_army: dictionnary with the unit of the two player(dict)
    dict_order:dictionnary of players orders(dict)
    dict_board: dictionnary with all the characteristic of the board (dict)
    dict_recruit: dictionnary with research and stat of new ship(dict)
    dict_memory : dictionnary of order given by the ai in past turn(dict)
    players: names of the players(tuple)
    peace : number of turn wihout damage (int)
    connection : sockets to receive/send orders (dict of socket.socket)
    colored_display : enable or display colors for the display(bool)
    play_game : verify if the game need to continue(str)

    return
    ------
    play_game : verify if the game need to continue(str)
    peace : number of turn wihout damage (int)


    Version
    -------
    specification: François Bechet (v.3 24/02/20)
    implementation: François Bechet (v.1 13/03/20)
    """
    # get players orders
    dict_order = get_order(players, dict_army, dict_board, dict_memory,
                           connection, dict_recruit, width, height)
    # call all functions to execute the player's orders
    recruit_units(dict_order, dict_army, players, dict_board, dict_recruit)
    upgrade(dict_order, dict_army, dict_recruit, players)
    # check if the hub is destroyed
    # if the hub is destroyed stop the game
    win_condition = attack(dict_order, dict_army, dict_board, height, width,
                           players, peace)
    if win_condition[0] == 'win':
        print('The winner is %s!' % win_condition[1])
        if 'ai' not in players[1]:
            remote_play.close_connection(connection)
        play_game = False
        return 0, play_game
    elif win_condition[2] == 400:
        print("There was no attack during 400 turns so the game ended.")
        if 'ai' not in players[1]:
            remote_play.close_connection(connection)
        play_game = False
    else:
        move(dict_order, dict_board, height, width, dict_army, players)
        energy_transfert(dict_army, dict_order, dict_board, height, width,
                         players)
        regenerate(dict_army, players)
        display_board(dict_board, height, width, players, dict_army,
                      colored_display)

    return win_condition[2], play_game


def get_order(players, dict_army, dict_board, dict_memory, connection,
              dict_recruit, height, width):
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
    dict_army: dictionnary with the unit of the two player(dict)
    dict_board: dictionnary with all the characteristic of the board (dict)
    dict_memory : dictionnary of order given by the ai in past turn(dict)
    connection : sockets to receive/send orders (dict of socket.socket)
    height: height of the board(int)
    width: width of the board(int)
    dict_recruit: dictionnary with research and stat of new ship(dict)

    return
    ------
    dict_order: dictionnary with all the order

    Version
    −−−−−−−
    specification: Dominik Everaert (v.4 24/02/20)
    implementation: François Bechet (v.2 01/03/20)
    """

    # create dict_order
    dict_order = {
        players[0]: {
            'move': [],
            'attack': [],
            'upgrade': [],
            'recruit': [],
            'transfer': []
        },
        players[1]: {
            'move': [],
            'attack': [],
            'upgrade': [],
            'recruit': [],
            'transfer': []
        }
    }

    for player in players:
        # case when player2 is a remote player so we need to get his order and
        # give our orders
        if 'ai' not in players[1]:
            # get player1 orders and send them to the remote player
            if player == players[0]:
                if 'ai' not in players[0]:
                    order_player1 = (input("%s, please enter your orders : " %
                                           players[0]))
                    order_player1_send = send_orders(order_player1, height,
                                                     width)
                    remote_play.notify_remote_orders(connection,
                                                     order_player1_send)
                    list_order_player = (order_player1).split()
                else:
                    order_player1 = AI_gr_50.ai_play(dict_army, dict_board,
                                                     dict_memory, dict_recruit,
                                                     players, player)
                    order_player1_send = send_orders(order_player1, height,
                                                     width)
                    remote_play.notify_remote_orders(connection,
                                                     order_player1_send)
                    list_order_player = (order_player1).split()
            # get player2 orders
            else:
                list_order_player = (
                    remote_play.get_remote_orders(connection)).split()

        else:  # case when player2 is a local player
            # get player1 orders
            if player == players[0]:
                list_order_player = (input("%s, please enter your orders : " %
                                           players[0]).split())
            else:
                list_order_player = AI_gr_50.ai_play(dict_army, dict_board,
                                                     dict_memory, dict_recruit,
                                                     players, player).split()
        # place player's orders in dict_order
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

    # extract the units from dict_order and place them into dict_board and
    # dict_army
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
            # create a deepcopy of dict_recruit because otherwise it would point to
            # the same object and cause issues later
            dict_recruit_copy = copy.deepcopy(dict_recruit)
            unit = dict_order[player]['recruit'][i]
            unitList = unit.split(':')
            # check that the unit name doesn't already exists
            if (unitList[0] not in dict_army[players[0]]) and (
                    unitList[0] not in dict_army[players[1]]):
                buy = False
                # check that the player hub has enough energy to buy the unit
                if unitList[1] == 'cruiser':
                    if dict_army[player]['hub'][
                            'current_energy'] > dict_recruit_copy[player][
                                'cruiser']['cost']:
                        buy = True
                elif unitList[1] == 'tanker' and dict_army[player]['hub'][
                        'current_energy'] > dict_recruit_copy[player][
                            'tanker']['cost']:
                    buy = True

                if buy:
                    # add the unit to dict_board
                    unitDict = {unitList[0]: {'ship_type': unitList[1]}}
                    dict_board[hub_case][player].update(unitDict)
                    # add the unit to dict_army and pay the unit price
                    # verify that the unit is not already in dict_army
                    if unitList[0] not in dict_army[player]:
                        if 'cruiser' in unitList:
                            dict_army[player][unitList[0]] = dict_recruit_copy[
                                player]['cruiser']
                            dict_army[player]['hub'][
                                'current_energy'] -= dict_recruit_copy[player][
                                    'cruiser']['cost']
                        elif 'tanker' in unitList:
                            dict_army[player][unitList[0]] = dict_recruit_copy[
                                player]['tanker']
                            dict_army[player]['hub'][
                                'current_energy'] -= dict_recruit_copy[player][
                                    'tanker']['cost']

    return dict_army, dict_board


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
                    if (dict_army[player]['hub']['current_energy']
                        ) >= 750 and (dict_army[player]['hub']['regeneration']
                                      ) < 50 and (dict_recruit[player][
                                          'research']['regeneration']) < 5:
                        dict_army[player]['hub']['regeneration'] += 5
                        dict_army[player]['hub']['current_energy'] -= 750
                        dict_recruit[player]['research']['regeneration'] += 1
                    else:
                        print(player +
                              ", you can't upgrade energy regeneration.")

                elif upgradeList[1] == 'storage':
                    if (dict_army[player]['hub']['current_energy']
                        ) >= 600 and (
                            dict_recruit[player]['research']['storage']) < 3:
                        dict_recruit[player]['research']['storage'] += 1
                        dict_army[player]['hub']['current_energy'] -= 600
                        dict_recruit[player]['tanker'][
                            'energy_capacity'] += 100
                        temp_dict = list(dict_army[player])
                        # upgrade existing tankers
                        for i in range(len(temp_dict)):
                            if dict_army[player][temp_dict[i]][
                                    'ship_type'] == 'tanker' and dict_army[
                                        player][temp_dict[i]][
                                            'energy_capacity'] < 900:
                                dict_army[player][
                                    temp_dict[i]]['energy_capacity'] += 100
                    else:
                        print(player + ", you can't upgrade energy capacity.")

                elif upgradeList[1] == 'range':
                    if (dict_army[player]['hub']['current_energy']
                        ) >= 400 and (
                            dict_recruit[player]['research']['range']) < 4:
                        dict_recruit[player]['research']['range'] += 1
                        dict_army[player]['hub']['current_energy'] -= 400
                        dict_recruit[player]['cruiser']['shooting_range'] += 1
                        temp_dict = list(dict_army[player])
                        # upgrade existing cruisers
                        for i in range(len(temp_dict)):
                            if dict_army[player][temp_dict[i]][
                                    'ship_type'] == 'cruiser' and dict_army[
                                        player][temp_dict[i]][
                                            'shooting_range'] < 6:
                                dict_army[player][
                                    temp_dict[i]]['shooting_range'] += 1
                    else:
                        print(player + ", you can't upgrade shooting range.")

                elif upgradeList[1] == 'move':
                    if (dict_army[player]['hub']['current_energy']
                        ) >= 500 and (
                            dict_recruit[player]['research']['move']) < 4:
                        dict_recruit[player]['research']['move'] += 1
                        dict_army[player]['hub']['current_energy'] -= 500
                        dict_recruit[player]['cruiser']['move_cost'] -= 1
                        temp_dict = list(dict_army[player])
                        # upgrade existing cruisers
                        for i in range(len(temp_dict)):
                            if dict_army[player][temp_dict[i]][
                                    'ship_type'] == 'cruiser' and dict_army[
                                        player][temp_dict[i]]['move_cost'] > 4:
                                dict_army[player][
                                    temp_dict[i]]['move_cost'] -= 1
                    else:
                        print(player + ", you can't upgrade movement.")

    return dict_army, dict_recruit


def attack(dict_order, dict_army, dict_board, height, width, players, peace):
    """execute attack order of each player and modify stats of each effected unit

    parameters
    ----------
    dict_order[attack]: dictionnary of attack order(dict)
    dict_board: dictionnary with all the characteristic of the board (dict)
    height:height of the board(int)
    width:width of the board(int)
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
            # search target position
            # separate position_target into target x et target y
            targetxy = target_position.split('-')
            # separate target position
            x_target = int(targetxy[0])
            y_target = int(targetxy[1])

            # search shooter position
            for key, value in dict_board.items():
                if attacker in value:
                    unit = value[attacker]
                    if attackList[0] in unit:
                        case = key.split('-')
                        case_0 = case[0].strip('@')
                        x_shooter, y_shooter = int(case_0), int(case[1])

            # search shooter range
            if dict_army[player][shooter_name]['ship_type'] == 'cruiser':
                shooting_range = dict_army[player][shooter_name][
                    'shooting_range']

            # check that the targeted case is in the board and check that there
            # are units of the target on the targeted case
            if ((x_target <= width and x_target >= 1 and y_target <= height
                 and y_target >= 1) and
                (target in dict_board['@%s-%s' % (x_target, y_target)])):
                target_units = []
                for unit in dict_board['@%s-%s' %
                                       (x_target, y_target)][target]:
                    target_units.append(unit)

                # execute the attack
                # check manhattan distance and check that that the unit has
                # enough energy to attack
                if compute_manhattan_distance(
                        x_shooter, y_shooter, x_target, y_target,
                        shooting_range) and dict_army[attacker][shooter_name][
                            'current_energy'] >= 10 * damage:
                    dict_army[attacker][shooter_name][
                        'current_energy'] -= 10 * damage
                    for i in target_units:
                        # change the unit hp : hp = hp - damage
                        dict_army[target][i]['hp'] -= damage
                        total_damage += damage
                # if it's a cruiser disable his move ability for the turn
                if dict_army[attacker][
                        attackList[0]]['ship_type'] == 'cruiser':
                    dict_army[attacker][attackList[0]]['turn_attack'] = True

    for player in players:
        # delete the unit if damage is >= unit hp
        dead_units = []
        for ship in dict_army[player]:
            if dict_army[player][ship]['hp'] <= 0:
                # if the unit is the hub -> the attacker win
                if ship == 'hub':
                    if player == players[0]:
                        winner = players[1]
                    else:
                        winner = players[0]
                    return ('win', winner)
                else:
                    dead_units.append(ship)

        # delete dead units
        for ship in dead_units:
            del dict_army[player][ship]
            # if there is only one unit delete the player key
            for case, value in dict_board.items():
                if player in dict_board[case]:
                    if ship in dict_board[case][player]:
                        if len(dict_board[case][player]) == 1:
                            del dict_board[case][player]
                        # else delete only the unit key
                        else:
                            del dict_board[case][player][ship]
    if total_damage == 0:
        peace += 1
    else:
        peace = 0
    return dict_board, dict_army, peace


def move(dict_order, dict_board, height, width, dict_army, players):
    """execute move order of each player and modify board and stats of moving units

    prameters
    ---------
    dict_order[move]: dictionnary of move order(dict)
    dict_board: dictionnary with all the characteristic of the board (dict)
    height:height of the board(int)
    width:width of the board(int)
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
    # extract the move order from dict_order and change the position unit in
    # dict_board
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
                    if player in value and moveList[0] in value[player]:
                        unit = value[player]
                        xy_shooter = key  # store unit position to delete it after the move
                        case = key.split('-')
                        case_0 = case[0].strip('@')
                        x_shooter, y_shooter = int(case_0), int(case[1])
                # check that the cruiser has enough energy
                if (dict_army[player][moveList[0]]['ship_type'] == 'cruiser'
                        and dict_army[player][moveList[0]]['current_energy'] <
                        dict_army[player][moveList[0]]['move_cost']):
                    moveLegality = False
                # check that the targeted case is in the board
                if x_target > width or x_target < 1 or y_target > height or y_target < 1:
                    moveLegality = False
                # check that the targeted case is not the current case
                elif x_target == x_shooter and y_target == y_shooter:
                    moveLegality = False
                # verify that the unit didn't already moved this turn
                elif dict_army[player][moveList[0]]['move']:
                    moveLegality = False
                # verify that the cruiser didn't already attacked this turn
                elif dict_army[player][moveList[0]][
                        'ship_type'] == 'cruiser' and dict_army[player][
                            moveList[0]]['turn_attack']:
                    moveLegality = False
                # check manhattan distance and moveLegality
                if compute_manhattan_distance(x_shooter, y_shooter, x_target,
                                              y_target) and moveLegality:
                    # move the unit position in dict_board
                    # change the position of the unit in dict_board
                    unit = unit[moveList[0]]
                    if player not in dict_board[moveList[1]]:
                        temp_dict = {player: {moveList[0]: {}}}
                        temp_dict[player][moveList[0]].update(unit)
                        dict_board[moveList[1]].update(temp_dict)
                    else:
                        temp_dict = {moveList[0]: {}}
                        temp_dict[moveList[0]].update(unit)
                        dict_board[moveList[1]][player].update(temp_dict)
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
                    if dict_army[player][
                            moveList[0]]['ship_type'] == 'cruiser':
                        move_cost = dict_army[player][moveList[0]]['move_cost']
                        dict_army[player][
                            moveList[0]]['current_energy'] -= move_cost
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


def energy_transfert(dict_army, dict_order, dict_board, height, width,
                     players):
    """execute transfert order and modify affected unit's stat

    parameters
    ----------
    dict_army: dictionnary with the unit of the two player(dict)
    dict_order[energy_transfert]:dictionnary of energy transfert order(dict)
    dict_board: dictionnary with all the characteristic of the board (dict)
    height:height of the board(int)
    width:width of the board(int)
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
        # extract order from dict_order and place each kind of transfert order
        # in a specific list
        for order in dict_order[player]['transfer']:
            list_order, receiving = [], False
            if ':<' in order:
                list_order = order.split(':<')
                receiving = True
            elif ':>' in order:
                list_order = order.split(':>')

            # execute energy transfert and check that the unit is a tanker and
            # that the unit is not giving energy to itself
            if list_order != [] and dict_army[player][
                    list_order[0]]['ship_type'] == 'tanker' and list_order[
                        0] != list_order[1]:
                # check manhattan distance
                # get positions
                for c_order in list_order:
                    # get units positions
                    for key, value in dict_board.items():
                        if player in value and c_order in value[player]:
                            case = key.split('-')
                            case_0 = case[0].strip('@')
                            if c_order == list_order[0]:
                                x_shooter, y_shooter = int(case_0), int(
                                    case[1])
                            else:
                                if not receiving:
                                    x_target, y_target = int(case_0), int(
                                        case[1])
                    # get hub position
                    if receiving:
                        xy_target = list_order[1].split('-')
                        x_target, y_target = int(xy_target[0]), int(
                            xy_target[1])

                if compute_manhattan_distance(x_shooter, y_shooter, x_target,
                                              y_target):
                    # check that the targeted case is in the board
                    if x_target <= width and x_target >= 1 and y_target <= height and y_target >= 1:
                        # receiving
                        if receiving:
                            # check that there is a peak on the case
                            if 'peak' in dict_board['@' + list_order[1]]:
                                energy_receiver = dict_army[player][list_order[0]]['energy_capacity'] - \
                                    dict_army[player][list_order[0]
                                                    ]['current_energy']
                                energy_giver = dict_board[
                                    '@' + list_order[1]]['peak']['energy']
                                if energy_giver <= energy_receiver:
                                    energy = energy_giver
                                else:
                                    energy = energy_receiver
                                # do the energy transfert
                                dict_board[
                                    '@' +
                                    list_order[1]]['peak']['energy'] -= energy
                                dict_army[player][
                                    list_order[0]]['current_energy'] += energy
                                # if peak's energy reach 0, remove the peak
                                if dict_board[
                                        '@' +
                                        list_order[1]]['peak']['energy'] == 0:
                                    del dict_board['@' + list_order[1]]['peak']
                            # hub
                            if player in dict_board['@' + list_order[1]]:
                                if 'hub' in dict_board['@' +
                                                       list_order[1]][player]:
                                    energy_giver = dict_army[player]['hub'][
                                        'current_energy']
                                    energy_receiver = dict_army[player][list_order[0]]['energy_capacity'] - \
                                        dict_army[player][list_order[0]]['current_energy']
                                    if energy_giver <= energy_receiver:
                                        energy = energy_giver
                                    else:
                                        energy = energy_receiver
                                    # do the energy transfert
                                    dict_army[player]['hub'][
                                        'current_energy'] -= energy
                                    dict_army[player][list_order[0]][
                                        'current_energy'] += energy

                        # hub or unit
                        else:
                            energy_receiver = dict_army[player][list_order[1]]['energy_capacity'] - \
                                dict_army[player][list_order[1]]['current_energy']
                            energy_giver = dict_army[player][
                                list_order[0]]['current_energy']
                            if energy_giver <= energy_receiver:
                                energy = energy_giver
                            else:
                                energy = energy_receiver
                            # do the energy transfert
                            dict_army[player][
                                list_order[0]]['current_energy'] -= energy
                            dict_army[player][
                                list_order[1]]['current_energy'] += energy
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
        empty = dict_army[player]['hub']['energy_capacity'] - \
            dict_army[player]['hub']['current_energy']
        if empty < regen:
            regen = empty
        dict_army[player]['hub']['current_energy'] += regen
    return dict_army


def compute_manhattan_distance(x_shooter,
                               y_shooter,
                               x_target,
                               y_target,
                               shooting_range=1):
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
    else:
        return False


def send_orders(order_player1, height, width):
    """change de coordinates of orders

    Parameters
    ----------
    order_player1 : order of player 1(str)
    height: height of the board(int)
    width: width of the board(int)

    returns
    -------
    order_player1 : order of player 1(str)

    """
    # formula
    # |x -widht|+1
    # |y -height|+1
    print(order_player1)
    if order_player1 != '':
        order_player1 = order_player1.split()
        changing_list = []
        changed = ''
        # extract the orders with positions to change
        orders = []
        for i in range(len(order_player1)):
            if ('@' in order_player1[i] or '*' in order_player1[i] or '<' in order_player1[i]):
                changing_list.append(order_player1[i])
                orders.append(order_player1[i])
        for i in orders:
            print(i)
            order_player1.remove(i)
        # adapt the positions
        for order in range(len(changing_list)):
            # move orders
            if '@' in changing_list[order]:
                # alpha:@5-3
                move = changing_list[order].split('@')
                coordinates = move[1].split('-')
                x = abs(int(coordinates[0]) - height) + 1
                y = abs(int(coordinates[1]) - width) + 1
                move = move[0] + '@%d-%d' % (x , y)
                changed += ' %s ' % move
            # attack orders
            elif '*' in changing_list[order]:
                # alpha:*5-2=20
                attack = changing_list[order].split('*')
                damage = attack[1].split('=')
                coordinates = damage[0].split('-')
                x = abs(int(coordinates[0]) - height) + 1
                y = abs(int(coordinates[1]) - width) + 1
                attack = attack[0] + '*%d-%d=%s' % (x , y, damage[1])
                changed += ' %s ' % attack
            # transfer orders
            elif '<' in changing_list[order]:
                # alpha:<5-2
                transfer = changing_list[order].split('<')
                coordinates = transfer[1].split('-')
                x = abs(int(coordinates[0]) - height) + 1
                y = abs(int(coordinates[1]) - width) + 1
                transfer = transfer[0] + '<%d-%d' % (x, y)
                changed += ' %s ' % transfer
        final_orders = ""
        for order in order_player1:
            final_orders += " %s " % order
        order_player1 = final_orders + changed
    print(order_player1)
    return order_player1
