
### WORK ON DETECTING AND ACCOUNTING FOR CHECK/CHECKMATE
### WORK ON STALEMATE/TIE
### WORK ON EN PASSANT
### WORK ON CASTLING
### WORK ON TIMER

# 09-23-2025 # 3 hours
# made base board to use with icons

# 09-24-2025 # 13 hours
# made pieces movable + point system

# 09-25-2025 # 7 hours
# added checkmate (bad (gotta take king to win))
# added movement math
# added crowning pawns logic on reaching end of the board
# added movement logic for pawns, rooks, bishops and kings

# 09-26-2025 # 5 hours
# added movement logic for queens and knights
# added forfeit option
# added piece clipping (cant move through pieces)

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
    ['w','♔','e','1',0,'n'],  # white king 1
    ['w','♕','d','1',9,'n'],  # white queen 1
    ['w','♖','a','1',5,'n'],  # white rook 1
    ['w','♖','h','1',5,'n'],  # white rook 2
    ['w','♗','c','1',3,'n'],  # white bishop 1
    ['w','♗','f','1',3,'n'],  # white bishop 2
    ['w','♘','b','1',3,'n'],  # white knight 1
    ['w','♘','g','1',3,'n'],  # white knight 2
    
    ['w','♙','a','2',1,'n'],  # white pawn 1
    ['w','♙','b','2',1,'n'],  # white pawn 2
    ['w','♙','c','2',1,'n'],  # white pawn 3
    ['w','♙','d','2',1,'n'],  # white pawn 4
    ['w','♙','e','2',1,'n'],  # white pawn 5
    ['w','♙','f','2',1,'n'],  # white pawn 6
    ['w','♙','g','2',1,'n'],  # white pawn 7
    ['w','♙','h','2',1,'n'],  # white pawn 8
    
    ['b','♚','e','8',0,'n'],  # black king 1
    ['b','♛','d','8',9,'n'],  # black queen 1
    ['b','♜','a','8',5,'n'],  # black rook 1
    ['b','♜','h','8',5,'n'],  # black rook 2
    ['b','♝','c','8',3,'n'],  # black bishop 1
    ['b','♝','f','8',3,'n'],  # black bishop 2
    ['b','♞','b','8',3,'n'],  # black knight 1
    ['b','♞','g','8',3,'n'],  # black knight 2
    
    ['b','♟','a','7',1,'n'],  # black pawn 1
    ['b','♟','b','7',1,'n'],  # black pawn 2
    ['b','♟','c','7',1,'n'],  # black pawn 3
    ['b','♟','d','7',1,'n'],  # black pawn 4
    ['b','♟','e','7',1,'n'],  # black pawn 5
    ['b','♟','f','7',1,'n'],  # black pawn 6
    ['b','♟','g','7',1,'n'],  # black pawn 7
    ['b','♟','h','7',1,'n'],  # black pawn 8
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
    print("♔ ♚ - King (game ends if taken)")
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
            inp = input("START THE GAME? Y/N: ").strip().upper()
            if inp == "Y":
                plyr1 = input("Name player 1 (white): ")
                plyr2 = input("Name player 2 (black): ")
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

# boring input checks
def checkPiece(A):
    global selectedPiece, forfeit
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

def makeMovement(A,B):
    global pieces, pointsW, pointsB, winner, checkMate
    # basic input checks
    if not A == "":
        A = A.lower()
        if not B == "x":
            if not forfeit:
                try:
                    Aa,Ab = list(A)
                    Ba,Bb = list(B)
                except:
                    print("Your input needs to be a position on the board!")
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
                                            if canMove(Aa,Ab,Ba,Bb):
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
                                                return False
                                    else:
                                        if p[0] == "b":
                                            print("You cannot take your own piece!")
                                            return False
                                        else:
                                            if canMove(Aa,Ab,Ba,Bb):
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
                                            else:
                                                return False
                            if canMove(Aa,Ab,Ba,Bb):
                                if willClip(Aa,Ab,Ba,Bb):
                                    for p in pieces:
                                        # if piece doesnt exist on destination, move your piece
                                        if p[2] == Aa and p[3] == Ab:
                                            p[2] = Ba
                                            p[3] = Bb
                                            p[5] = "y"
                                            return True
                                    else:
                                        return False
                                else:
                                    return False
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
    CAa = Aa
    CAb = Ab
    
    # more pawn logic
    for q in pieces:
        if q[2] == Ba and q[3] == Bb:
            target = True
        
        if Bb == "8" or Bb == "1":
            finalSpace = True

    # determine what piece is moving
    for p in pieces:
        if p[2] == Aa and p[3] == Ab:
            Aa,Ab,Ba,Bb = calcPosition(Aa,Ab,Ba,Bb)
            movesHor = Ab - Bb
            movesVer = Aa - Ba
            movesHor = abs(movesHor)
            movesVer = abs(movesVer)
            
            # king logic
            if p[1] == "♔" or p[1] == "♚":
                if (movesHor <= 1 and movesVer <= 1):
                    return True
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
                print("Rooks can move either horizontal or vertical!!")
            # bishop logic
            elif p[1] == "♗" or p[1] == "♝":
                if movesHor == movesVer:
                    return True
                print("Bishops can only move sideways!")
            # knight logic
            elif p[1] == "♘" or p[1] == "♞":
                if movesHor == 2:
                    if movesVer == 1:
                        return True
                elif movesVer == 2:
                    if movesHor == 1:
                        return True
                print("Knights move in an L shape!")
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
                            finalSpaceF(CAa,CAb)
                        return True
                    else:
                        print("Pawns can only attack to the left or right infront of them!")
                elif Aa == Ba:
                    if not p[5] == "y":
                        if (0 <= movesHor <= 2):
                            if finalSpace:
                                finalSpaceF(CAa,CAb)
                            return True
                        else:
                            print("Pawns cannot move more than 2 tiles if they haven't been moved before!")
                    else:
                        if (0 <= movesHor <= 1):
                            if finalSpace:
                                finalSpaceF(CAa,CAb)
                            return True
                        else:
                            print("Pawns cannot move more than 1 tile!")
            else:
                return True

# piece clipping (cant move through other pieces)
def willClip(Aa,Ab,Ba,Bb):
    # determine what piece is moving
    for p in pieces:
        if p[2] == Aa and p[3] == Ab:
            Aa,Ab,Ba,Bb = calcPosition(Aa,Ab,Ba,Bb)
            hor = []
            ver = []
            
            # list crossed tiles (not including starting and ending tiles)
            if Ab > Bb:
                for r in range(Bb+1,Ab):
                    hor.append(r)
            elif Ab < Bb:
                for r in range(Ab+1,Bb):
                    hor.append(r)
            if Aa > Ba:
                for r in range(Ba+1,Aa):
                    ver.append(r)
            elif Aa < Ba:
                for r in range(Aa+1,Ba):
                    ver.append(r)
            
            # moved 1 tile
            if hor == [] and ver == []:
                return True
            
            # moved straight line
            if hor == []:
                hor.append(Ab)
            if ver == []:
                ver.append(Aa)
            
            # knight jumps over
            if p[1] == "♘" or p[1] == "♞":
                return True
            
            # check if any pieces are on crossed tiles
            for h in hor:
                for v in ver:
                    h = int(h)
                    v = int(v)
                    h = horizontal[h]
                    v = vertical[v]
                    for q in pieces:
                        if q[2] == v and q[3] == h:
                            print("You cannot move through other pieces!")
                            return False
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

# crowning pawns logic (i hate trees like this)
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
def symbolCheck(a,b):
    for p in pieces:
        if p[2] == a and p[3] == b:
            return p[1]
    return None

# tile color check (could be done easier but i cant be arsed as of yet)
def colorCheck(A,N):
    pos = 0

    A = A.upper()
    
    if A in ["A","C","E","G"]:
        pos += 0
    elif A in ["B","D","F","H"]:
        pos += 1
        
    if N in ["1","3","5","7"]:
        pos += 0
    elif N in ["2","4","6","8"]:
        pos += 1
        
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
        # bottom row
        for ver1 in vertical:
            print(ver1, end=" ")
        print()
        print()
        
        # turn announcement
        if turn % 2:
            print("Turn " + str(turn) + " : " + plyr1)
        else:
            print("Turn " + str(turn) + " : " + plyr2)
        
        # points announcement
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
                output = False
                selPiece = input("Pick the piece to move: ")
                output = checkPiece(selPiece)
                if output == True or output == "Forfeit":
                    select = True
                    break
            
            # ask and check for player input (destination)
            while True:
                output = False
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
            print("")
        if winner == "White":
            print("Winner is " + plyr1 + " with " + str(pointsW) + " points to " + str(pointsB) + "!")
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
