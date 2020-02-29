def display_board(dict_board,height,width):
    """display the board at the beginning of the game

    parameters
    ----------
    dict_board: dictionnary with all the characteristic of the board (dict)

    Version
    −−−−−−−
    specification: Dominik Everaert (v.1 24/02/20)

    """
    dict_board['case[3,4]']
    for x in range(height):
        for y in range(width):
            if dict_board['case[%d,%d]'%(x+1,y+1)] == {''}:
                print('.',end='')
            else:
                if dict_board['case[%d,%d]'%(x+1,y+1)]['ship_name'] == 'cruiser':
                    print('O')
        print('')
        
def game():
    """start the game and play it

    Version
    −−−−−−−
    specification: François Bechet (v.1 24/02/20)

    """
    board_values = create_board("board.txt")
    dict_board = board_values[0]
    height = board_values[1]
    width = board_values[2]
    display_board(dict_board,height,width)

def get_order():
    """ask the player for orders

    return
    ------
    dict_order: dictionnary with all the order
    
    Version
    −−−−−−−
    specification: Dominik Everaert (v.1 24/02/20)
    """

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
    """

    # open the board file and save it's content
    with open (board_file,"r") as f:
        data = f.readlines()

    # create a dict and store all board file infos in it
    dict_board={}
    key_1=0
    for line in data :
        if ':' in line:
            idx = line.find(':')
            key_1=line[:idx]
            dict_board[key_1]=[]
        else:
            dict_board[key_1].append(line.split())

    # get map width and height
    sizes = dict_board['map'][0]
    width = int(sizes[0])
    height = int(sizes[1])

    # create a dictionnary of the board with keys as cases
    case = ''
    for x in range(height):
        for y in range(width):
            case = 'case[%d,%d]'%(x+1,y+1)
            dict_board[case]={''}
    return dict_board,height,width
    
def attack(dict_order[attack],dict_army):
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

def move(dict_order[move],dict_board,dict_army):
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

def upgrade(dict_order[upgrade],dict_army,dict_recruit):
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
def energy_transfert(dict_army,dict_order[energy_transfert]):
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
def recruit_units(dict_recruit,dict_order[recruit],dict_army):
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
    """
def energy_mining(dict_army,dict_order[energy_mining],dict_board):
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