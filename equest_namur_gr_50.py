# imports
import colored

def display_board(dict_board,height,width):
    """display the board at the beginning of the game

    parameters
    ----------
    dict_board: dictionnary with all the characteristic of the board (dict)

    Version
    −−−−−−−
    specification: Dominik Everaert (v.1 24/02/20)
    implementation: François Bechet (v.1 01/03/20)

    """
    # define colored colors
    default_color = colored.fg('#000000')
    green = colored.fg('#00ff00')
    red = colored.fg('#ff0000')
    blue = colored.fg('#0000ff')

    # display the board
    for x in range(width):
        for y in range(height):      
            if dict_board['case[%d,%d]'%(x+1,y+1)] == {'hub':'hub_1'} :
                print(green + '⌂' + default_color,end='')
            elif dict_board['case[%d,%d]'%(x+1,y+1)] == {'hub':'hub_2'} :
                print(red + '⌂' + default_color,end='')
            elif 'peak' in dict_board['case[%d,%d]'%(x+1,y+1)]:
                print(blue + '⚐' + default_color,end='')
            else:
                print(".",end='')
        print('')

def game(play_game):
    """start the game and play it

    Version
    −−−−−−−
    specification: François Bechet (v.1 24/02/20)
    implementation: François Bechet (v.1 01/03/20)

    """
    # create the players
    player1 = input("who is player1 : ")
    player2 = input("who is player2 : ")
    # call the create_board function and store its return values
    board_values = create_board("board.txt")
    dict_board = board_values[0]
    height = board_values[1]
    width = board_values[2]

    # call the display_board function
    display_board(dict_board,height,width)

    # create dictionnary of the army
    dict_army = {player1:{},player2:{}}

    #get_order()
    # start the main game loop
    while play_game != False:
        dict_order = get_order(player1,player2)
        recruit_units(dict_order,dict_army,player1,player2)

def get_order(player1,player2):
    """ask the player for orders

    Orders must respect this syntax :
        RECRUIT ORDER : 'alpha:tanker bravo:cruiser'
        UPGRADE ORDER : 'upgrade:regeneration; upgrade:storage; upgrade:range; upgrade:move'
        MOVE ORDER(name:@r-c where r is row and c is column) : 'alpha:@30-31'
        ATTACK ORDER(nom:*r-c=q where r,c is position of target and q are damages) : 'charlie:*10-15=23' 
        TRANSFER ORDER(nom:<r-c where the tanker take energy in the targeted hub; name1:>name2 where name1(tanker) gives energy to name2(cruiser or hub)) : alpha:<30-31 bravo:>charlie delta:>hub

    return
    ------
    dict_order: dictionnary with all the order
    
    Version
    −−−−−−−
    specification: Dominik Everaert (v.1 24/02/20)
    implementation: François Bechet (v.1 01/03/20)
    """

    # ask the user's orders
    print(player1 + ", please enter your orders : ")
    player1_orders = input()
    print(player2 + ", please enter your orders : ")
    player2_orders = input()

    # add orders to the dict_order list
    list_order_player1 = player1_orders.split()
    list_order_player2 = player2_orders.split()

    # convert list_oder to dict_order
    dict_order = {player1:{'move':[],'attack':[],'upgrade':[],'recruit':[],'transfer':[]},player2:{'move':[],'attack':[],'upgrade':[],'recruit':[],'transfer':[]}}
    # add player1 orders to dict_order
    for i in range(len(list_order_player1)):
        if '@' in list_order_player1[i]:
            dict_order[player1]['move'].append(list_order_player1[i])
        elif '*' in list_order_player1[i]:
            dict_order[player1]['attack'].append(list_order_player1[i])
        elif 'upgrade' in list_order_player1[i]:
            dict_order[player1]['upgrade'].append(list_order_player1[i])
        elif '>' in list_order_player1[i] or '<' in list_order_player1[i]:
            dict_order[player1]['transfer'].append(list_order_player1[i])
        else:
            dict_order[player1]['recruit'].append(list_order_player1[i])
    
    # add player2 orders to dict_order
    for i in range(len(list_order_player2)):
        if '@' in list_order_player2[i]:
            dict_order[player2]['move'].append(list_order_player2[i])
        elif '*' in list_order_player2[i]:
            dict_order[player2]['attack'].append(list_order_player2[i])
        elif 'upgrade' in list_order_player2[i]:
            dict_order[player2]['upgrade'].append(list_order_player2[i])
        elif '>' in list_order_player2[i] or '<' in list_order_player2[i]:
            dict_order[player2]['transfer'].append(list_order_player2[i])
        else:
            dict_order[player2]['recruit'].append(list_order_player2[i])

    # return dictionnary of orders
    print(dict_order)
    return dict_order

def create_board(board_file):
    """take a file and change it into a board

    parameters
    ----------
    board_file: file in which all the element needed for the board are(path)
    
    return
    ------
    dict_board: dictionnary with all the characteristic of the board (dict)

    Version
    −−−−−−−
    specification: Dominik Everaert (v.1 24/02/20)
    implementation: François Bechet (v.1 01/03/20)
    """

    # open the board file and save it's content
    with open (board_file,"r") as f:
        data = f.readlines()

    # create a dict and store all board file infos in it
    dictFile={}
    key_1=0
    for line in data :
        if ':' in line:
            idx = line.find(':')
            key_1=line[:idx]
            dictFile[key_1]=[]
        else:
            dictFile[key_1].append(line.split())

    # get map width and height
    sizes = dictFile['map'][0]
    width = int(sizes[0])
    height = int(sizes[1])

    # create a dictionnary of the board with keys as cases
    dict_board = {}
    for x in range(width):
        for y in range(height):
            dict_board['case[%d,%d]'%(x+1,y+1)] = ''
    
    # add hubs to the board's dictionnary
    hub_1 = dictFile['hubs'][0]
    hub_2 = dictFile['hubs'][1]
    key1_hub_1 = int(hub_1[0])
    key2_hub_1 = int(hub_1[1])
    key1_hub_2 = int(hub_2[0])
    key2_hub_2 = int(hub_2[1])
    dict_board['case[%d,%d]'%(key1_hub_1,key2_hub_1)] = {'hub':'hub_1'}
    dict_board['case[%d,%d]'%(key1_hub_2,key2_hub_2)] = {'hub':"hub_2"}

    # add peaks to the board's dictionnary
    for i in range(len(dictFile['peaks'])):
        peak = 'peak_'
        peak = peak + str(i)
        print(peak)
        list_peak = dictFile['peaks'][i]
        print(list_peak)
        energy = int(list_peak[2])
        dict_board['case[%d,%d]'%(int(list_peak[0]),int(list_peak[1]))] = {'peak':{peak:{'energy':energy}}}

    # returns
    return dict_board,height,width
    
def attack(dict_order,dict_army):
    """execute attack order of each player and modify stats of each effected unit

    parameters
    ----------
    dict_order[attack]: dictionnary of attack order(dict)
    dict_army: dictionnary with the unit of the two player(dict)
    
    return
    ------
    dict_army: dictionnary of the 2 army modified in result of the attack(dict)

    Version
    −−−−−−−
    specification: Dominik Everaert (v.1 24/02/20)
    """

def move(dict_order,dict_board,dict_army):
    """execute move order of each player and modify board and stats of moving units
    
    prameters
    ---------
    dict_order[move]: dictionnary of move order(dict)
    dict_board: dictionnary with all the characteristic of the board (dict)
    dict_army: dictionnary with the unit of the two player(dict)
    
    return
    ------
    dict_board: dictionnary with all the characteristic of the board (dict)

    Version
    −−−−−−−
    specification: François Bechet (v.1 24/02/20)
    """

def upgrade(dict_order,dict_army,dict_recruit):
    """execute the upgrage order of each player and modify the stats of each affected unit

    parameters
    ----------
    dict_order[upgrade]: dictionnary of upgrade order(dict)
    dict_army: dictionnary with the unit of the two player(dict)
    dict_recruit: dictionnary with research and stat of new ship

    return
    ------
    dict_army: dictionnary with the unit of the two player(dict)
    dict_recruit: dictionnary with research and stat of new ship(dict)

    Version
    −−−−−−−
    specification: François Bechet (v.1 24/02/20)

    """
def energy_transfert(dict_army,dict_order):
    """execute transfert order and modify affected unit's stat
    
    parameters
    ----------
    dict_army: dictionnary with the unit of the two player(dict)
    dict_order[energy_transfert]:dictionnary of energy transfert order(dict)
    
    return
    ------
    dict_army: dictionnary with the unit of the two player(dict)

    Version
    −−−−−−−
    specification: Dominik Everaert (v.1 24/02/20)
    """
def regenerate(dict_army):
    """makes hub regenerate energy(at the end of the turn)

    parameters
    ----------
    dict_army: dictionnary with the unit of the two player(dict)

    return
    ------
    dict_army: dictionnary with the unit of the two player(dict)

    Version
    −−−−−−−
    specification: Dominik Everaert (v.1 24/02/20)
    """

def recruit_units(dict_order,dict_army,player1,player2):
    """execute recruit order and add unit to the army

    parameters
    ----------
    dict_army: dictionnary with the unit of the two player(dict)
    dict_recruit: dictionnary with research and stat of new ship(dict)
    dict_order[recruit]: dictionnary of upgrade order(dict)

    return
    ------
    dict_army: dictionnary with the unit of the two player(dict)
    
    Version
    −−−−−−−
    specification: Dominik Everaert (v.1 24/02/20)
    implementation: François Bechet (v.1 01/03/20)
    """

    # extract the units from dict_order and place them into dict_army
    # player1
    for i in range(len(dict_order[player1]['recruit'])):
        unit = dict_order[player1]['recruit'][i]
        unitList = unit.split(':')
        dict_army[player1][unitList[0]] = {'ship_type':unitList[1]}

    # player2
    for i in range(len(dict_order[player2]['recruit'])):
        unit = dict_order[player2]['recruit'][i]
        unitList = unit.split(':')
        dict_army[player2][unitList[0]] = {'ship_type':unitList[1]}

    print(dict_army)
    return dict_army

def energy_mining(dict_army,dict_order,dict_board):
    """execute mining order and modify affected unit's stat and energy peak's stat
    
    parameters
    ----------
    dict_army: dictionnary with the unit of the two player(dict)
    dict_order[energy_mining]: dictionnary of energy mining order(dict)
    dict_board: dictionnary with all the characteristic of the board (dict)
    
    return
    ------
    dict_army: dictionnary with the unit of the two player(dict)
    dict_board: dictionnary with all the characteristic of the board (dict)

    Version
    −−−−−−−
    specification: François Bechet (v.1 24/02/20)
    """

def compute_manhattan_distance(x_shooter,y_shooter,x_target,y_target):
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
    """
def play_turn(dict_board,dict_army,dict_recruit,dict_ordre):
    """ manage each turn of the game by receiving the commands of each player

    Parameters
    ----------
    dict_army: dictionnary with the unit of the two player(dict)
    dict_order:dictionnary of players orders(dict)
    dict_board: dictionnary with all the characteristic of the board (dict)
    dict_recruit: dictionnary with research and stat of new ship(dict)

    Version
    -------
    specification: François Bechet (v.1 24/02/20)
    """
game(True)