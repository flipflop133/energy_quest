from equest_namur_gr_50 import game

# Ask player for colors
i = False
while i is False:
    color = input("Do you want to play with colors(y/n)? ")
    if color.upper() == 'Y':
        color = True
        i = True
    elif color.upper() == 'N':
        color = False
        i = True
    else:
        i = False

# Ask player for game mode (single or multiplayer)
print("1:singleplayer")
print("2:multiplayer")
game_mode = input("Choose game mode:")
if game_mode == '2':
    players = [' ', ' ']
    while players[0].isspace():
        j = False
        while j is False:
            ai = input("Do you want the local player to be an ai(y/n)? ")
            if ai.upper() == 'Y':
                ai = True
                j = True
                print(j)
            elif ai.upper() == 'N':
                players[0] = input("who is local player : ")
                j = True
            else:
                j = False
    while players[1].isspace() or (players[1] == players[0]):
        players[1] = input("who is remote player : ")
    game('test.eq', int(players[0]), int(players[1]), '127.0.0.1', ai, color)
elif game_mode == '1':
    players = [' ', 'ai']
    while players[0].isspace():
        players[0] = input("who is player 1 : ")
    game('test.eq', players[0], players[1], '127.0.0.1', color, )
