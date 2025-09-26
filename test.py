
### WORK ON MOVEMENT RULES

# 09-23-2025 # 3 hours
# made base board to use with icons

# 09-24-2025 # 13 hours
# made pieces movable + point system

# 09-25-2025 # 7 hours
# added checkmate (bad (gotta take king to win))
# added movement math
# added crowning pawns on reaching end of the board
# added movement and attacking calculation for pawns, rooks, bishops and kings

# 09-26-2025 # 1 hour
# added movement and attacking calculations for queens

vertical = ["a","b","c","d","e","f","g","h"]
horizontal = ["8","7","6","5","4","3","2","1"]
checkMate = False
forfeit = False
lost = False
plyr1 = ""
plyr2 = ""
symbol = ""
winner = ""
turn = 1
pointsW = 0
pointsB = 0

pieces = [
    # [color,piece,verti,hori,points,moved]
    ['w','♘','d','4',3,'n'],  # testing piece
    ['w','♙','a','6',1,'n'],  # white pawn 1
]

### FUNCTIONS
def startGame():
    global plyr1, plyr2, pieces
    print("")
    print("  # # # PYTHON 1v1 CHESS # # #  ")
    print("")
    print("To select pices to move, type out the position they are in, eg. e2 or a1, follow by their destination.")
    print("If you wish to cancel picking a piece, type out \"X\" as your destination.")
    print("To forfeit a game, type out \"FORFEIT\" as the piece you wish to move.")
    print("To land checkmate, \"take\" your opponent's King; this'll end the game.")
    print("Pieces are represented by the following icons:")
    print("♔ ♚ - King (invaluable)")
    print("♕ ♛ - Queen (9 points)")
    print("♖ ♜ - Rook (5 points)")
    print("♗ ♝ - Bishop (3 points)")
    print("♘ ♞ - Knight (3 points)")
    print("♙ ♟ - Pawn (1 point, can be crowned upon reaching the end of the board)")
    print("White moves first, players alternate turns.")
    print("Good luck and have fun!")
    print("")
    try:
        while True:
            inp = "Y" #input("START THE GAME? Y/N: ").strip().upper()
            if inp == "Y":
                plyr1 = "White" # input("Name player 1 (white): ")
                plyr2 = "Black" # input("Name player 2 (black): ")
                plyr1 = plyr1 + " (white)"
                plyr2 = plyr2 + " (black)"
                return True
            elif inp == "N":
                print("Then why boot up the program?")
                return False
            else:
                print("Please enter either Y or N.")
    except e:
        print("Something went wrong:", e)
        return False

def checkPiece(A):
    global selectedPiece, forfeit
    #try:
    A = A.upper()
    if not A == "FORFEIT":
        if not A == "" and not A == "00" and len(A) == 2:
            a,b = list(A)
            a = a.lower()
            for p in pieces:
                if p[2] == a and p[3] == b:
                    if turn % 2:
                        if p[0] == "w":
                            selectedPiece = p[1]
                            return True
                        else:
                            print("That's not your piece!")
                            return False
                    else:
                        if p[0] == "b":
                            selectedPiece = p[1]
                            return True
                        else:
                            print("That's not your piece!")
                            return False
            print("No input found/wrong input given, try again.")
            return False
        else:
            print("Your input needs to be a position on the board!")
            return False
    else:
        forfeit = True
        return "Forfeit"
    #except:
    #    print("An unexpected error occurred, try again.")
    #    return False

def makeMovement(A,B):
    global pieces, pointsW, pointsB, winner, checkMate
    #try:
    if not A == "":
        A = A.lower()
        if not B == "x":
            if not forfeit:
                try:
                    Aa,Ab = list(A)
                    Ba,Bb = list(B)
                except:
                    print("Wrong input")
                    return False
                # check if input is in legal range
                if Aa in vertical and Ab in horizontal and Ba in vertical and Bb in horizontal:
                    # check if destination isnt same as selected
                    if not (Aa == Ba and Ab == Bb):
                            # loop to try and find if a piece exists on destination
                            for p in pieces:
                                if p[2] == Ba and p[3] == Bb:
                                    if turn % 2:
                                        if p[0] == "w":
                                            print("You cannot take your own piece!")
                                            return False
                                        else:
                                            if not canMove(Aa,Ab,Ba,Bb):
                                                return False
                                            else:
                                                if p[1] == "♚":
                                                    winner = "White"
                                                    checkMate = True
                                                    return True
                                                else:
                                                    p[2] = "0"
                                                    p[3] = "0"
                                                    pointsW += p[4]
                                                    for q in pieces:
                                                        if q[2] == Aa and q[3] == Ab:
                                                            q[2] = Ba
                                                            q[3] = Bb
                                                            q[5] = "y"
                                                    return True
                                    else:
                                        if p[0] == "b":
                                            print("You cannot take your own piece!")
                                            return False
                                        else:
                                            if not canMove(Aa,Ab,Ba,Bb):
                                                return False
                                            else:
                                                if p[1] == "♔":
                                                    winner = "Black"
                                                    checkMate = True
                                                    return True
                                                else:
                                                    p[2] = "0"
                                                    p[3] = "0"
                                                    pointsB += p[4]
                                                    for q in pieces:
                                                        if q[2] == Aa and q[3] == Ab:
                                                            q[2] = Ba
                                                            q[3] = Bb
                                                            q[5] = "y"
                                                    return True
                            if not canMove(Aa,Ab,Ba,Bb):
                                return False
                            else:
                                for p in pieces:
                                    # if piece doesnt exist on destination, move your piece
                                    if p[2] == Aa and p[3] == Ab:
                                        p[2] = Ba
                                        p[3] = Bb
                                        p[5] = "y"
                                        return True
                    else:
                        print("If you want to cancel moving the selected piece, type \"X\" instead.")
                else:
                    print("Wrong inputs.")
            else:
                if turn % 2:
                    winner = "Black"
                else:
                    winner = "White"
                return True
        else:
            return "Cancel"
    else:
        print("You cannot leave your input blank!")
        return False

# piece movement rules
def canMove(Aa,Ab,Ba,Bb):
    target = False
    finalSpace = False
    moves = ""
    
    for q in pieces:
        # are you targeting an enemy? (only for pawns (i think))
        if q[2] == Ba and q[3] == Bb:
            target = True
        
        # are you targeting the final row? (only for pawns)
        if Bb == "8" or Bb == "1":
            finalSpace = True

    for p in pieces:
        # determine what piece is moving
        if p[2] == Aa and p[3] == Ab:
            Aa,Ab,Ba,Bb = calcPosition(Aa,Ab,Ba,Bb)
            movesHor = Ab - Bb
            movesVer = Aa - Ba
            movesHor = abs(movesHor)
            movesVer = abs(movesVer)
            print(Aa,Ab,Ba,Bb, movesHor, movesVer)
            # king logic
            if p[1] == "♔" or p[1] == "♚":
                if (0 <= movesHor <= 1 and 0 <= movesVer <= 1):
                    return True
                else:
                    print("Kings can only move 1 tile in any direction!")
            # queen logic
            elif p[1] == "♕" or p[1] == "♛":
                if movesVer == movesHor:
                    return True
                elif movesVer <= 1 and movesHor <= 1:
                    return True
                elif movesHor > 1:
                    if movesVer < 1:
                        return True
                elif movesVer > 1:
                    if movesHor < 1:
                        return True
                print("Queens can move omnidirectional, but only in lines!")
            # rook logic
            elif p[1] == "♖" or p[1] == "♜":
                if Aa == Ba or Ab == Bb:
                    return True
                else:
                    print("Rooks can move either horizontal or vertical!!")
            # bishop logic
            elif p[1] == "♗" or p[1] == "♝":
                if movesHor == movesVer:
                    return True
                else:
                    print("Bishops can only move sideways!")
            # knight logic
            elif p[1] == "♘" or p[1] == "♞":
                if movesHor == movesVer:
                    return True
                else:
                    print("Bishops can only move sideways!")
            # pawn logic
            elif p[1] == "♙" or p[1] == "♟":
                aa = Aa
                ab = Ab
                
                if p[1] == "♙": #white
                    movesHor = Ab - Bb
                    movesVer = Aa - Ba
                elif p[1] == "♟": #black
                    movesHor = Bb - Ab
                    movesVer = Ba - Aa

                if target:
                    if movesHor == 1 and abs(movesVer) == 1:
                        if finalSpace:
                            finalSpaceF(aa,ab)
                        return True
                    else:
                        print("Pawns can only attack to the left or right infront of them!")
                elif Aa == Ba:
                    if not p[5] == "y":
                        if (0 <= movesHor <= 2):
                            if finalSpace:
                                finalSpaceF(aa,ab)
                            return True
                        else:
                            print("Pawns cannot move more than 2 tiles if they haven't been moved before!")
                    else:
                        if (0 <= movesHor <= 1):
                            if finalSpace:
                                finalSpaceF(aa,ab)
                            return True
                        else:
                            print("Pawns cannot move more than 1 tile!")
                else:
                    print("Can only move forward, unless attacking!: ", p)
            else:
                return True

# calculate the location of the pieces, and their targets
def calcPosition(Aa,Ab,Ba,Bb):
    for p in pieces:
        if p[2] == Aa and p[3] == Ab:
            locAa = p[2]
            indAa = vertical.index(locAa)
            
            locAb = p[3]
            indAb = horizontal.index(locAb)
            
            indBa = vertical.index(Ba)
            indBb = horizontal.index(Bb)
            
            Aa = int(indAa)
            Ab = int(indAb)
            Ba = int(indBa)
            Bb = int(indBb)
            return Aa,Ab,Ba,Bb

def finalSpaceF(aa,ab):
    for p in pieces:
        if p[2] == aa and p[3] == ab:
            while True:
                print("You can change your pawn to any of the following: (Q)ueen, (R)ook, (B)ishop, (K)night.")
                inp = input("Choose one of the pieces (type in the initial): ")
                inp = inp.upper()
                
                if p[0] == "w":
                    if inp == "Q":
                        p[1] = '♕'
                        p[4] = 9
                        return True
                    elif inp == "R":
                        p[1] = '♖'
                        p[4] = 5
                        return True
                    elif inp == "B":
                        p[1] = '♗'
                        p[4] = 3
                        return True
                    elif inp == "K":
                        p[1] = '♘'
                        p[4] = 3
                        return True
                elif p[0] == "b":
                    if inp == "Q":
                        p[1] = '♛'
                        p[4] = 9
                        return True
                    elif inp == "R":
                        p[1] = '♜'
                        p[4] = 5
                        return True
                    elif inp == "B":
                        p[1] = '♝'
                        p[4] = 3
                        return True
                    elif inp == "K":
                        p[1] = '♞'
                        p[4] = 3
                        return True

# return symbol for given piece (if any)
def symbolCheck(a, b):
    for p in pieces:
        if p[2] == a and p[3] == b:
            return p[1]
    return None

# could be done easier but i cant be arsed
def colorCheck(A,N):
    pos = 0

    A = A.upper()
    
    if A in ["A","C","E","G"]:
        pos += 0
    elif A in ["B","D","F","H"]:
        pos += 1
    else:
        print("Error: Invalid A")
        exit()
        
    if N in ["1","3","5","7"]:
        pos += 0
    elif N in ["2","4","6","8"]:
        pos += 1
    else:
        print("Error: Invalid N")
        exit()
        
    if pos % 2 == 0:
        return "white"
    else:
        return "black"

### MECHANICS
if startGame():
    ### BOARD DRAWING
    while True:
        selectedPiece = "PIECE ERROR"
        select = False
        move = False
            
        # top row
        print()
        print("-------------------------")
        print()
        for hor1 in horizontal:
            # left row only
            print(hor1, end=" ")
            # inner board each tile
            for ver2 in vertical:
                out = ver2+hor1
                outL = list(out)
                symbol = symbolCheck(outL[0], outL[1])
                # check if a piece on a tile exists
                if symbol:
                    print(symbol, end=" ")
                # if it doesnt exist, print a square of corresponding color
                else:
                    if colorCheck(outL[0], outL[1]) == "white":
                        print("■", end=" ")
                    else:
                        print("□", end=" ")
                    # print(out, end=" ") # board positions
            print()
        print(" ", end=" ")
        for ver1 in vertical:
            print(ver1, end=" ")
        print()
        print()
        
        # turn announcement
        if turn % 2:
            print("Turn " + str(turn) + " : " + plyr1)
        else:
            print("Turn " + str(turn) + " : " + plyr2)
        
        if pointsW == pointsB:
            symbol = "="
        elif pointsW > pointsB and pointsW - pointsB <= 9:
            symbol = "+/="
        elif pointsW > pointsB and pointsW - pointsB > 9:
            symbol = "+/-"
        elif pointsB > pointsW and pointsB - pointsW <= 9:
            symbol = "=/+"
        elif pointsB > pointsW and pointsB - pointsW > 9:
            symbol = "-/+"
        else:
            symbol = "?"
        print("White : " + str(pointsW), symbol, str(pointsB) + " : Black")
        
        while True:
            # ask and check for player input (selecting piece)
            while True:
                selPiece = input("Pick the piece to move: ")
                output = checkPiece(selPiece)
                if output or output == "Forfeit":
                    select = True
                    break
            
            # ask and check for player input (destination)
            while True:
                if not forfeit:
                    movePiece = input("Select your " + selectedPiece + "'s destination: ")
                else:
                    movePiece = "FORFEIT"
                output = makeMovement(selPiece,movePiece)
                if output == True:
                    move = True
                    break
                elif output == "Cancel":
                    break
            
            # if all inputs are correct start next turn
            if select and move:
                if not checkMate:
                    turn += 1
                break
        if checkMate or forfeit:
            break
    
    # winner announcing
    if not winner == "":
        print()
        print("-------------------------")
        print()
        if forfeit:
            print("Player " + (plyr2 if turn % 2 else plyr1) + " has forfeited the game!")
        if winner == "White":
            print("Winner is " + plyr1 + " with " + str(pointsW) + " to " + str(pointsB) + "!")
            if not forfeit:
                print("Taken pieces include the following: ")
                print("♚", end="")
                for ps in pieces:
                    if ps[0] == "b" and ps[2] == "0" and ps[3] == "0":
                        print(ps[1], end="")
                print("")
                print("Lost pieces include the following: ")
                for ps in pieces:
                    if ps[0] == "w" and ps[2] == "0" and ps[3] == "0":
                        print(ps[1], end="")
                        lost = True
                if not lost:
                    print("None lost!")
                print("")
        elif winner == "Black":
            print("Winner is " + plyr2 + " with " + str(pointsB) + " to " + str(pointsW) + "!")
            if not forfeit:
                print("Taken pieces include the following: ")
                print("♔", end="")
                for ps in pieces:
                    if ps[0] == "w" and ps[2] == "0" and ps[3] == "0":
                        print(ps[1], end="")
                print("")
                print("Lost pieces include the following: ")
                for ps in pieces:
                    if ps[0] == "b" and ps[2] == "0" and ps[3] == "0":
                        print(ps[1], end="")
                        lost = True
                if not lost:
                    print("None lost!")
                print("")
        print("Thanks for playing!")
