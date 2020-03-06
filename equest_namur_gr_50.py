# imports
import colored

def display_board(dict_board,height,width,player1,player2,dict_army):
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
    print(' ',end='')
    for i in range(1,height+1):
        if i < 10:
            print(i,end='  ')
        else:
            print(i,end=' ')
    print('')
    n=0
    for x in range(width):
        n = 1
        for y in range(height):      
            if player1 in dict_board['@%d-%d'%(x+1,y+1)]:
                tempDict = dict_board['@%d-%d'%(x+1,y+1)][player1]
                if 'hub' in tempDict:
                    print(green + ' ⌂ ' + default_color,end='')
                else:
                    for key in tempDict:
                        unit = tempDict[key]
                        if 'cruiser' in unit['ship_type']:
                            print(green + ' ☿ ' + default_color,end='')
                        if 'tanker' in unit['ship_type']:
                            print(green + ' * ' + default_color,end='')
            elif player2 in dict_board['@%d-%d'%(x+1,y+1)]:
                tempDict = dict_board['@%d-%d'%(x+1,y+1)][player2]
                if 'hub' in tempDict:
                    print(red + ' ⌂ ' + default_color,end='')
                else:
                    for key in tempDict:
                        unit = tempDict[key]
                        if 'cruiser' in unit['ship_type']:
                            print(red + ' ☿ ' + default_color,end='')
                        if 'tanker' in unit['ship_type']:
                            print(red + ' * ' + default_color,end='')
            elif 'peak' in dict_board['@%d-%d'%(x+1,y+1)]:
                print(blue + ' ⚐ ' + default_color,end='')
            else:
                print(" . ",end='')
        n = n + x
        print(' ' + str(n))

    print('player1:' + str(dict_army[player1]))
    print('player2:' + str(dict_army[player2]))
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
    # create dict_recruit
    dict_recruit = {player1:{'cruiser':{'ship_type':'cruiser','hp':300,'energy-capacity':200, 'distance':2, 'cost':1000},'tanker':{'ship_type':'tanker','hp':200, 'energy-capacity':600, 'cost':500},'research':{'ship_type':'research','energy_regen':0,'move_cost':2}},player2:{'cruiser':{'ship_type':'cruiser','hp':300,'energy-capacity':200, 'distance':2, 'cost':1000},'tanker':{'ship_type':'tanker','hp':200, 'energy-capacity':600, 'cost':500},'research':{'ship_type':'research','energy_regen':0,'move_cost':2}}}
    # call the create_board function and store its return values
    board_values = create_board("board.txt",player1,player2)
    dict_board = board_values[0]
    height = board_values[1]
    width = board_values[2]
    
    # create dictionnary of the army
    dict_army = {player1:{},player2:{}}

    # call the display_board function
    display_board(dict_board,height,width,player1,player2,dict_army)

    #get_order()
    # start the main game loop
    while play_game != False:
        dict_order = get_order(player1,player2)
        dict_army,dict_board = recruit_units(dict_order,dict_army,player1,player2,dict_board,dict_recruit)
        dict_board = move(dict_order,dict_board,dict_army,player1,player2)
        display_board(dict_board,height,width,player1,player2,dict_army)
        upgrade(dict_order,dict_army,dict_recruit,player1,player2)

def get_order(player1,player2):
    """ask the player for orders

    Orders must respect this syntax :
        RECRUIT ORDER : 'alpha:tanker bravo:cruiser'
        UPGRADE ORDER : 'upgrade:regeneration; upgrade:storage; upgrade:shooting_range; upgrade:move_cost'
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
    player1_orders = input("%s, please enter your orders : "%player1)
    player2_orders = input("%s, please enter your orders : "%player2)

    # add orders to the dict_order list
    list_order_player1 = player1_orders.split()
    list_order_player2 = player2_orders.split()

    # convert list_oder to dict_order
    dict_order = {player1:{'move':[],'attack':[],'upgrade':[],'recruit':[],'transfer':[]},player2:{'move':[],'attack':[],'upgrade':[],'recruit':[],'transfer':[]}}
    # add orders of players to dict_order
    for j in range(1,3): #j is to loop through player1 and player2
        if j == 1:
            player = player1
            list_order_player = list_order_player1
        else:
            player = player2
            list_order_player = list_order_player2
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
    return dict_order

def create_board(board_file,player1,player2):
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
            dict_board['@%d-%d'%(x+1,y+1)] = {}

    print(dictFile)
    # add hubs to the board's dictionnary
    hub_1 = dictFile['hubs'][0]
    hub_2 = dictFile['hubs'][1]
    key1_hub_1 = int(hub_1[0])
    key2_hub_1 = int(hub_1[1])
    key1_hub_2 = int(hub_2[0])
    key2_hub_2 = int(hub_2[1])
    dict_board['@%d-%d'%(key1_hub_1,key2_hub_1)] = {player1:{'hub':''}}
    dict_board['@%d-%d'%(key1_hub_2,key2_hub_2)] = {player2:{'hub':''}}

    # create dict_army
    dic
    # add peaks to the board's dictionnary
    for i in range(len(dictFile['peaks'])):
        peak = 'peak_'
        peak = peak + str(i)
        list_peak = dictFile['peaks'][i]
        energy = int(list_peak[2])
        dict_board['@%d-%d'%(int(list_peak[0]),int(list_peak[1]))] = {'peak':{peak:{'energy':energy}}}

    # returns
    return dict_board,height,width
    
def attack(dict_order,dict_army,player1,player2):
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

def move(dict_order,dict_board,dict_army,player1,player2):
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
    # extract the move order from dict_order and change the position unit in dict_board
    moveList = ''
    for j in range(1,3):
        if j == 1:
            player = player1
        else:
            player = player2
        
        # extract the move order
        for i in range(len(dict_order[player]['move'])):
            move = dict_order[player]['move'][i]
            moveList = move.split(':')
            moveList.append(player)

        # move the unit position in dict_board
        for i in dict_board:
            if moveList != '':
                #store the case position
                case = moveList[1]
                # change the position of the unit in dict_board
                if player in dict_board[i]:
                    tempBoard = dict_board[i][player]
                    if moveList[0] in tempBoard:
                        unit = (dict_board[i][player][moveList[0]])
                        tempDict = {player:{moveList[0]:{}}}
                        tempDict[player][moveList[0]].update(unit)
                        dict_board[case].update(tempDict)
    
    return dict_board
    
def upgrade(dict_order,dict_army,dict_recruit,player1,player2):
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
    implementation: Dominik Everaert (v.1 05/03/20)
    """
     # extract the upgrade order from dict_order and change the stat of unit
    upgradeList = ''
    for j in range(1,3):
        if j == 1:
            player = player1
        else:
            player = player2
        
        # extract the upgrade order
        for i in range(len(dict_order[player]['upgrade'])):
            upgrade = dict_order[player]['upgrade'][i]
            upgradeList = upgrade.split(':')
            upgradeList.append(player)
            print(upgradeList)

            # choose which upgrade must be done
            if upgradeList[1] == 'regeneration':
                if dict_army[player][hub][1]>=750 and dict_recruit[player][research][energy_regen] < 10 :
                     dict_army[player][hub][4]+=5
                     dict_recruit[player][research][energy_regen]+=1

                else:
                    print("you can't upgrade energy regenaretion")
                
            elif upgradeList[1] == 'storage':
                print(dict_army)
                if dict_army[player][hub][1]>=600 and dict_recruit[player][research][energy_capacity] < 12 :
                    dict_recruit[player][research][energy_capacity]+=1
                    dict_recruit[player][tanker][energy_capacity]+=100
                    for i in range(len(dict_army[player])):
                        if dict_army[player][i][ship_type] == 'tanker' :
                            dict_army[player][i][energy_capacity]+=100

                else:
                    print('you can\'t  upgrade energy capacity')
                
            elif upgradeList[1] == range:
                if dict_army[player][hub][1]>=400 and dict_recruit[player][research][shooting_range] < 5 :
                    dict_recruit[player][research][shooting_range]+=1
                    dict_recruit[player][cruiser][shooting_range]+=1
                    for i in range(len(dict_army[player])):
                        if dict_army[player][i][ship_type] == 'cruiser' :
                            dict_army[player][i][shooting_range]+=1

                else:
                    print('you can\'t  upgrade shooting range')

            elif upgradeList[1] == move:
                if dict_army[player][hub][1]>=500 and dict_recruit[player][research][move_cost] < 5 :
                    dict_recruit[player][research][move_cost]+=1
                    dict_recruit[player][cruiser][move_cost]-=1
                    for i in range(len(dict_army[player])):
                        if dict_army[player][i][ship_type] == 'cruiser' :
                            dict_army[player][i][move_cost]-=1

                else:
                    print('you can\'t  upgrade movement ')

    return dict_army,dict_recruit 

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

def recruit_units(dict_order,dict_army,player1,player2,dict_board,dict_recruit):
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

    # extract the units from dict_order and place them into dict_board and dict_army
    for j in range(1,3):
        if j == 1:
            player = player1
        else:
            player = player2
        # extract the order from dict_order
        for i in range(len(dict_order[player]['recruit'])):
            unit = dict_order[player]['recruit'][i]
            unitList = unit.split(':')
            # add the unit to dict_board
            # {'alpha': {'ship_type': 'tanker'}}
            for case, value in dict_board.items():
                current_string = value
                unitDict = {unitList[0]:{'ship_type':unitList[1]}}
                if player in current_string:
                    dict_board[case][player].update(unitDict)
            # add the unit to dict_army
            if unitList[0] not in dict_army[player]: # verify that the unit is not already in dict_army
                if 'cruiser' in unitList: 
                    dict_army[player][unitList[0]] = dict_recruit[player]['cruiser']
                elif 'tanker' in unitList:
                    dict_army[player][unitList[0]] = dict_recruit[player]['tanker']
            
    return dict_army, dict_board

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