"""STRUCTURES

#Dict1(board) :
 dict_board = {'case_1' : {’croiseur_1’,’ravitailleur _1’},'case_2' : {‘hub_1’},'case_3' : {'peak_1'}}

#Dict2(players units) : 
 dict_army = {'player_1':{'alpha' : {‘type’ :’croiseur’, ‘PS’ :300, ‘Energie’ :200, ‘portée’ :2, …}, 'tango' : {‘type’ :’ravitailleur’, ‘PS’ :100, ‘Energie’ :500, ‘, …}} 'player_2' :{'bravo' : {'type' : 'croisseur, 'PS' : 200}}}

#Dict3(available units to recruit -> one for each player) :
 player_1_recruit = {‘croiseur’ : {‘PS’ :300, ‘capacité d’énergie’ :200, ‘portée’ :2, ‘cout’ :1000…} ‘ravitailleur : {, ‘PS’ :200, ‘capacité d’énergie’ :600, ‘cout’ :500, …}}}
 player_2_recruit = {‘croiseur’ : {‘PS’ :600, ‘capacité d’énergie’ :300, ‘portée’ :2, ‘cout’ :1000…} ‘ravitailleur : {, ‘PS’ :200, ‘capacité d’énergie’ :600, ‘cout’ :500, …}}}

#Dict4(orders) :
 dict_ordre = {‘joueur_1’ : {‘recrue’ : {},’amélioration’ : {}, …}‘Joueur_2’ : : {‘recrue’ : {},’amélioration’ : {}, …}}

"""
def display_board(dict_board):
    """Display the board at the beginning of the game

    Parameters
    ----------
    dict_board: dictionnary with all the characteristic of the board (dict)

    Returns
    -------

    Versions
    -------

    """
def game(color=True):
    """Start the game and play it

    Parameters
    ----------
    color: use color overall or not(bool)

    Returns
    -------

    Versions
    --------

    """

def play_turn():

def get_order():
    """Ask the player for orders

    Parameters
    ----------

    Returns
    -------
    dict_order :dictionnary with all the order

    Versions
    --------
    """
def create_board(fichier_source):
    """
    """
    return dict_plat
    
def attack(dict_order[attack],dict_army):
    """Execute attack order of each player

    Parameters
    ----------
    dict_order[attack]: dictionnary of attack order(dict)
    dict_army : dictionnary with the unit of the two player(dict)
    
    Returns
    -------
    dict_army: dictionnary of the 2 army modified in result of the attack(dict)

    Versions
    -------
    """

def move(dict_order[move],dict_board):
    """Moves the units on the board

    Parameters
    ----------
    dict_order[move]: dictionnary of move order(dict)
    dict_board : dictionnary with the units emplacements(dict)
    Returns
    -------
    dict_board : dictionnary with the cases modified in result of the move(dict)
    Versions
    --------
    """

def upgrade():
    """
    """
def energy_transfert():
    """
    """
def regenerate():
    """
    """
def recruit_units():
    """
    """

def mining():
    """Transfer energy from energy cases to player
    """

def compute_manhattan_distance():
    """Compute the manhattan distance 

    Parameters
    ----------

    Returns
    -------

    Versions
    --------

    """