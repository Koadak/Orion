from board.move import move
from pieces.nullpiece import nullpiece
from pieces.queen import queen
import random


class AI:
    global tp
    tp = []

    def __init__(self):
        pass

    def evaluate(self, gametiles):
        min = 100000
        count = 0
        count2 = 0
        chuk = []
        movex = move()
        tp.clear()
        xp = self.minimax(gametiles, 3, -1000000000, 1000000000, False)

        for zoom in tp:
            if zoom[4] < min:
                chuk.clear()
                chuk.append(zoom)
                min = zoom[4]
            if zoom[4] == min:
                chuk.append(zoom)
        fx = random.randrange(len(chuk))
        print(tp)
        return chuk[fx][0], chuk[fx][1], chuk[fx][2], chuk[fx][3]

    def reset(self, gametiles):
        for x in range(8):
            for y in range(8):
                if gametiles[x][y].pieceonTile.tostring() == 'k' or gametiles[x][y].pieceonTile.tostring() == 'r':
                    gametiles[x][y].pieceonTile.moved = False

    def updateposition(self, x, y):
        a = x * 8
        b = a + y
        return b

    def checkmate(self, gametiles):
        movex = move()
        if movex.checkw(gametiles)[0] == 'checked':
            array = movex.movesifcheckedw(gametiles)
            if len(array) == 0:
                return True

        if movex.checkb(gametiles)[0] == 'checked':
            array = movex.movesifcheckedb(gametiles)
            if len(array) == 0:
                return True

    def stalemate(self, gametiles, player):
        movex = move()
        if player == False:
            if movex.checkb(gametiles)[0] == 'notchecked':
                check = False
                for x in range(8):
                    for y in range(8):
                        if gametiles[y][x].pieceonTile.alliance == 'Black':
                            moves1 = gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                            lx1 = movex.pinnedb(gametiles, moves1, y, x)
                            if len(lx1) == 0:
                                continue
                            else:
                                check = True
                            if check == True:
                                break
                    if check == True:
                        break

                if check == False:
                    return True

        if player == True:
            if movex.checkw(gametiles)[0] == 'notchecked':
                check = False
                for x in range(8):
                    for y in range(8):
                        if gametiles[y][x].pieceonTile.alliance == 'White':
                            moves1 = gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                            lx1 = movex.pinnedw(gametiles, moves1, y, x)
                            if len(lx1) == 0:
                                continue
                            else:
                                check = True
                            if check == True:
                                break
                    if check == True:
                        break

                if check == False:
                    return True

    def minimax(self, gametiles, depth, alpha, beta, player):
        if depth == 0 or self.checkmate(gametiles) == True or self.stalemate(gametiles, player) == True:
            return self.calculateb(gametiles)
        if not player:
            minEval = 100000000
            kp, ks = self.eva(gametiles, player)
            for lk in kp:
                for move in lk:
                    mts = gametiles[move[2]][move[3]].pieceonTile
                    gametiles = self.move(gametiles, move[0], move[1], move[2], move[3])
                    evalk = self.minimax(gametiles, depth - 1, alpha, beta, True)
                    if evalk < minEval and depth == 3:
                        tp.clear()
                        tp.append(move)
                    if evalk == minEval and depth == 3:
                        tp.append(move)
                    minEval = min(minEval, evalk)
                    beta = min(beta, evalk)
                    gametiles = self.revmove(gametiles, move[2], move[3], move[0], move[1], mts)
                    if beta <= alpha:
                        break

                if beta <= alpha:
                    break
            return minEval

        else:
            maxEval = -100000000
            kp, ks = self.eva(gametiles, player)
            for lk in ks:
                for move in lk:
                    mts = gametiles[move[2]][move[3]].pieceonTile
                    gametiles = self.movew(gametiles, move[0], move[1], move[2], move[3])
                    evalk = self.minimax(gametiles, depth - 1, alpha, beta, False)
                    maxEval = max(maxEval, evalk)
                    alpha = max(alpha, evalk)
                    gametiles = self.revmove(gametiles, move[2], move[3], move[0], move[1], mts)
                    if beta <= alpha:
                        break
                if beta <= alpha:
                    break

            return maxEval

    def printboard(self, gametilles):
        count = 0
        for rows in range(8):
            for column in range(8):
                print('|', end=gametilles[rows][column].pieceonTile.tostring())
            print("|", end='\n')

    def checkeva(self, gametiles, moves):
        arr = []
        for move in moves:
            lk = [[move[2], move[3]]]
            arr.append(self.calci(gametiles, move[0], move[1], lk))

        return arr

    def eva(self, gametiles, player):
        lx = []
        moves = []
        kp = []
        ks = []
        movex = move()
        for x in range(8):
            for y in range(8):
                if gametiles[y][x].pieceonTile.alliance == 'Black' and player == False:
                    if movex.checkb(gametiles)[0] == 'checked':
                        moves = movex.movesifcheckedb(gametiles)
                        arr = self.checkeva(gametiles, moves)
                        kp = arr
                        return kp, ks
                    moves = gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                    if len(moves) == 0:
                        continue
                    else:
                        if (gametiles[y][x].pieceonTile.tostring() == 'K'):
                            ax = movex.castlingb(gametiles)
                            if not len(ax) == 0:
                                for l in ax:
                                    if l == 'ks':
                                        moves.append([0, 6])
                                    if l == 'qs':
                                        moves.append([0, 2])
                    if gametiles[y][x].pieceonTile.alliance == 'Black':
                        lx = movex.pinnedb(gametiles, moves, y, x)
                    moves = lx
                    if len(moves) == 0:
                        continue
                    kp.append(self.calci(gametiles, y, x, moves))

                if gametiles[y][x].pieceonTile.alliance == 'White' and player == True:
                    if movex.checkw(gametiles)[0] == 'checked':
                        moves = movex.movesifcheckedw(gametiles)
                        arr = self.checkeva(gametiles, moves)
                        ks = arr
                        return kp, ks
                    moves = gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                    if moves == None:
                        print(y)
                        print(x)
                        print(gametiles[y][x].pieceonTile.position)
                    if len(moves) == 0:
                        continue
                    else:
                        if (gametiles[y][x].pieceonTile.tostring() == 'k'):
                            ax = movex.castlingw(gametiles)
                            if not len(ax) == 0:
                                for l in ax:
                                    if l == 'ks':
                                        moves.append([7, 6])
                                    if l == 'qs':
                                        moves.append([7, 2])
                    if gametiles[y][x].pieceonTile.alliance == 'White':
                        lx = movex.pinnedw(gametiles, moves, y, x)
                    moves = lx
                    if len(moves) == 0:
                        continue
                    ks.append(self.calci(gametiles, y, x, moves))

        return kp, ks

    def calci(self, gametiles, y, x, moves):
        arr = []
        jk = object
        for move in moves:
            jk = gametiles[move[0]][move[1]].pieceonTile
            gametiles[move[0]][move[1]].pieceonTile = gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile = nullpiece()
            mk = self.calculateb(gametiles)
            gametiles[y][x].pieceonTile = gametiles[move[0]][move[1]].pieceonTile
            gametiles[move[0]][move[1]].pieceonTile = jk
            arr.append([y, x, move[0], move[1], mk])
        return arr

    def count_blanks(self, gametiles):
        count = 0
        for x in range(8):
            for y in range(8):
                if gametiles[y][x].pieceonTile.tostring() == '-':
                    count += 1
        return count

    def center_control(self, gametiles, blanks):
        value = 0
        e4 = (4, 4)
        d4 = (4, 3)
        e5 = (3, 4)
        d5 = (3, 3)
        scale = 4 / blanks
        if gametiles[e4[0]][e4[1]].pieceonTile.tostring().isupper():
            value -= 1000
        if gametiles[d4[0]][d4[1]].pieceonTile.tostring().isupper():
            value -= 1000
        if gametiles[e5[0]][e5[1]].pieceonTile.tostring().isupper():
            value -= 1000
        if gametiles[d5[0]][d5[1]].pieceonTile.tostring().isupper():
            value -= 1000

        if gametiles[e4[0]][e4[1]].pieceonTile.tostring().islower():
            value += 1000
        if gametiles[d4[0]][d4[1]].pieceonTile.tostring().islower():
            value += 1000
        if gametiles[e5[0]][e5[1]].pieceonTile.tostring().islower():
            value += 1000
        if gametiles[d5[0]][d5[1]].pieceonTile.tostring().islower():
            value += 1000
        return scale * value

    def legalmoveKnight(self, gametiles, x, y):
        legalmoves = []

        if (gametiles[x][y].pieceonTile.alliance == 'Black'):

            if (x - 2 >= 0 and y + 1 < 8 and not gametiles[x - 2][y + 1].pieceonTile.alliance == 'Black'):
                legalmoves.append([x - 2, y + 1])

            if (x - 1 >= 0 and y + 2 < 8 and not gametiles[x - 1][y + 2].pieceonTile.alliance == 'Black'):
                legalmoves.append([x - 1, y + 2])

            if (x - 2 >= 0 and y - 1 >= 0 and not gametiles[x - 2][y - 1].pieceonTile.alliance == 'Black'):
                legalmoves.append([x - 2, y - 1])

            if (x - 1 >= 0 and y - 2 >= 0 and not gametiles[x - 1][y - 2].pieceonTile.alliance == 'Black'):
                legalmoves.append([x - 1, y - 2])

            if (x + 2 < 8 and y + 1 < 8 and not gametiles[x + 2][y + 1].pieceonTile.alliance == 'Black'):
                legalmoves.append([x + 2, y + 1])

            if (x + 1 < 8 and y + 2 < 8 and not gametiles[x + 1][y + 2].pieceonTile.alliance == 'Black'):
                legalmoves.append([x + 1, y + 2])

            if (x + 2 < 8 and y - 1 >= 0 and not gametiles[x + 2][y - 1].pieceonTile.alliance == 'Black'):
                legalmoves.append([x + 2, y - 1])

            if (x + 1 < 8 and y - 2 >= 0 and not gametiles[x + 1][y - 2].pieceonTile.alliance == 'Black'):
                legalmoves.append([x + 1, y - 2])

            return legalmoves

        else:
            if (x - 2 >= 0 and y + 1 < 8 and not gametiles[x - 2][y + 1].pieceonTile.alliance == 'White'):
                legalmoves.append([x - 2, y + 1])

            if (x - 1 >= 0 and y + 2 < 8 and not gametiles[x - 1][y + 2].pieceonTile.alliance == 'White'):
                legalmoves.append([x - 1, y + 2])

            if (x - 2 >= 0 and y - 1 >= 0 and not gametiles[x - 2][y - 1].pieceonTile.alliance == 'White'):
                legalmoves.append([x - 2, y - 1])

            if (x - 1 >= 0 and y - 2 >= 0 and not gametiles[x - 1][y - 2].pieceonTile.alliance == 'White'):
                legalmoves.append([x - 1, y - 2])

            if (x + 2 < 8 and y + 1 < 8 and not gametiles[x + 2][y + 1].pieceonTile.alliance == 'White'):
                legalmoves.append([x + 2, y + 1])

            if (x + 1 < 8 and y + 2 < 8 and not gametiles[x + 1][y + 2].pieceonTile.alliance == 'White'):
                legalmoves.append([x + 1, y + 2])

            if (x + 2 < 8 and y - 1 >= 0 and not gametiles[x + 2][y - 1].pieceonTile.alliance == 'White'):
                legalmoves.append([x + 2, y - 1])

            if (x + 1 < 8 and y - 2 >= 0 and not gametiles[x + 1][y - 2].pieceonTile.alliance == 'White'):
                legalmoves.append([x + 1, y - 2])

            return legalmoves

    def legalmoveBishop(self, gametiles, x, y):
        legalmoves = []
        a = 0
        b = 0
        count = 0
        if (gametiles[x][y].pieceonTile.alliance == 'Black'):
            while True:
                if (count == 0):
                    a = x + 1
                    b = y + 1
                    count = count + 1
                else:
                    a = a + 1
                    b = b + 1
                if (a < 8 and b < 8 and gametiles[a][b].pieceonTile.alliance is None):
                    legalmoves.append([a, b])
                    continue
                elif (a < 8 and b < 8 and gametiles[a][b].pieceonTile.alliance == 'White'):
                    legalmoves.append([a, b])
                    break
                else:
                    break

            count = 0
            while True:

                if (count == 0):
                    a = x - 1
                    b = y - 1
                    count = count + 1
                else:
                    a = a - 1
                    b = b - 1
                if (a >= 0 and b >= 0 and gametiles[a][b].pieceonTile.alliance is None):
                    legalmoves.append([a, b])
                    continue
                elif (a >= 0 and b >= 0 and gametiles[a][b].pieceonTile.alliance == 'White'):
                    legalmoves.append([a, b])
                    break
                else:
                    break

            count = 0
            while True:
                if (count == 0):
                    a = x + 1
                    b = y - 1
                    count = count + 1
                else:
                    a = a + 1
                    b = b - 1
                if (a < 8 and b >= 0 and gametiles[a][b].pieceonTile.alliance is None):
                    legalmoves.append([a, b])
                    continue
                elif (a < 8 and b >= 0 and gametiles[a][b].pieceonTile.alliance == 'White'):
                    legalmoves.append([a, b])
                    break
                else:
                    break

            count = 0
            while True:
                if (count == 0):
                    a = x - 1
                    b = y + 1
                    count = count + 1
                else:
                    a = a - 1
                    b = b + 1
                if (a >= 0 and b < 8 and gametiles[a][b].pieceonTile.alliance is None):
                    legalmoves.append([a, b])
                    continue
                elif (a >= 0 and b < 8 and gametiles[a][b].pieceonTile.alliance == 'White'):
                    legalmoves.append([a, b])
                    break
                else:
                    break

            return legalmoves

        if (gametiles[x][y].pieceonTile.alliance == 'White'):
            while True:
                if (count == 0):
                    a = x + 1
                    b = y + 1
                    count = count + 1
                else:
                    a = a + 1
                    b = b + 1
                if (a < 8 and b < 8 and gametiles[a][b].pieceonTile.alliance is None):
                    legalmoves.append([a, b])
                    continue
                elif (a < 8 and b < 8 and gametiles[a][b].pieceonTile.alliance == 'Black'):
                    legalmoves.append([a, b])
                    break
                else:
                    break

            count = 0
            while True:

                if (count == 0):
                    a = x - 1
                    b = y - 1
                    count = count + 1
                else:
                    a = a - 1
                    b = b - 1
                if (a >= 0 and b >= 0 and gametiles[a][b].pieceonTile.alliance is None):
                    legalmoves.append([a, b])
                    continue
                elif (a >= 0 and b >= 0 and gametiles[a][b].pieceonTile.alliance == 'Black'):
                    legalmoves.append([a, b])
                    break
                else:
                    break

            count = 0
            while True:
                if (count == 0):
                    a = x + 1
                    b = y - 1
                    count = count + 1
                else:
                    a = a + 1
                    b = b - 1
                if (a < 8 and b >= 0 and gametiles[a][b].pieceonTile.alliance is None):
                    legalmoves.append([a, b])
                    continue
                elif (a < 8 and b >= 0 and gametiles[a][b].pieceonTile.alliance == 'Black'):
                    legalmoves.append([a, b])
                    break
                else:
                    break

            count = 0
            while True:
                if (count == 0):
                    a = x - 1
                    b = y + 1
                    count = count + 1
                else:
                    a = a - 1
                    b = b + 1
                if (a >= 0 and b < 8 and gametiles[a][b].pieceonTile.alliance is None):
                    legalmoves.append([a, b])
                    continue
                elif (a >= 0 and b < 8 and gametiles[a][b].pieceonTile.alliance == 'Black'):
                    legalmoves.append([a, b])
                    break
                else:
                    break

            return legalmoves

    def legalmoveKing(self, gametiles, x, y):
        legalmoves = []

        if (gametiles[x][y].pieceonTile.alliance == 'Black'):

            if (x + 1 < 8 and y + 1 < 8 and not gametiles[x + 1][y + 1].pieceonTile.alliance == 'Black'):
                legalmoves.append([x + 1, y + 1])

            if (x + 1 < 8 and y - 1 >= 0 and not gametiles[x + 1][y - 1].pieceonTile.alliance == 'Black'):
                legalmoves.append([x + 1, y - 1])

            if (x + 1 < 8 and not gametiles[x + 1][y].pieceonTile.alliance == 'Black'):
                legalmoves.append([x + 1, y])

            if (y - 1 >= 0 and not gametiles[x][y - 1].pieceonTile.alliance == 'Black'):
                legalmoves.append([x, y - 1])

            if (y + 1 < 8 and not gametiles[x][y + 1].pieceonTile.alliance == 'Black'):
                legalmoves.append([x, y + 1])

            if (x - 1 >= 0 and not gametiles[x - 1][y].pieceonTile.alliance == 'Black'):
                legalmoves.append([x - 1, y])

            if (x - 1 >= 0 and y - 1 >= 0 and not gametiles[x - 1][y - 1].pieceonTile.alliance == 'Black'):
                legalmoves.append([x - 1, y - 1])

            if (x - 1 >= 0 and y + 1 < 8 and not gametiles[x - 1][y + 1].pieceonTile.alliance == 'Black'):
                legalmoves.append([x - 1, y + 1])

            return legalmoves

        else:
            if (x + 1 < 8 and y + 1 < 8 and not gametiles[x + 1][y + 1].pieceonTile.alliance == 'White'):
                legalmoves.append([x + 1, y + 1])

            if (x + 1 < 8 and y - 1 >= 0 and not gametiles[x + 1][y - 1].pieceonTile.alliance == 'White'):
                legalmoves.append([x + 1, y - 1])

            if (x + 1 < 8 and not gametiles[x + 1][y].pieceonTile.alliance == 'White'):
                legalmoves.append([x + 1, y])

            if (y - 1 >= 0 and not gametiles[x][y - 1].pieceonTile.alliance == 'White'):
                legalmoves.append([x, y - 1])

            if (y + 1 < 8 and not gametiles[x][y + 1].pieceonTile.alliance == 'White'):
                legalmoves.append([x, y + 1])

            if (x - 1 >= 0 and not gametiles[x - 1][y].pieceonTile.alliance == "White"):
                legalmoves.append([x - 1, y])

            if (x - 1 >= 0 and y - 1 >= 0 and not gametiles[x - 1][y - 1].pieceonTile.alliance == 'White'):
                legalmoves.append([x - 1, y - 1])

            if (x - 1 >= 0 and y + 1 < 8 and not gametiles[x - 1][y + 1].pieceonTile.alliance == 'White'):
                legalmoves.append([x - 1, y + 1])

            return legalmoves

    def legalmovePawn(self, gametiles, x, y):
        legalmoves = []
        if (gametiles[x][y].pieceonTile.alliance == 'Black'):

            if (x == 1):
                if (gametiles[x + 1][y].pieceonTile.tostring() == '-'):
                    legalmoves.append([x + 1, y])
                    if (gametiles[x + 2][y].pieceonTile.tostring() == '-'):
                        legalmoves.append([x + 2, y])
                if (y + 1 > 7):
                    if (gametiles[x + 1][y - 1].pieceonTile.alliance == 'White'):
                        legalmoves.append([x + 1, y - 1])
                if (y - 1 < 0):
                    if (gametiles[x + 1][y + 1].pieceonTile.alliance == 'White'):
                        legalmoves.append([x + 1, y + 1])
                if (y + 1 < 8 and y - 1 >= 0):
                    if (gametiles[x + 1][y - 1].pieceonTile.alliance == 'White'):
                        legalmoves.append([x + 1, y - 1])
                    if (gametiles[x + 1][y + 1].pieceonTile.alliance == 'White'):
                        legalmoves.append([x + 1, y + 1])
                return legalmoves



            else:
                if x < 6:
                    if (gametiles[x + 1][y].pieceonTile.tostring() == '-'):
                        legalmoves.append([x + 1, y])
                    if (y + 1 > 7):
                        if (gametiles[x + 1][y - 1].pieceonTile.alliance == 'White'):
                            legalmoves.append([x + 1, y - 1])
                    if (y - 1 < 0):
                        if (gametiles[x + 1][y + 1].pieceonTile.alliance == 'White'):
                            legalmoves.append([x + 1, y + 1])
                    if (y + 1 < 8 and y - 1 >= 0):
                        if (gametiles[x + 1][y - 1].pieceonTile.alliance == 'White'):
                            legalmoves.append([x + 1, y - 1])
                        if (gametiles[x + 1][y + 1].pieceonTile.alliance == 'White'):
                            legalmoves.append([x + 1, y + 1])

                return legalmoves

        if (gametiles[x][y].pieceonTile.alliance == 'White'):

            if (x == 6):
                if (gametiles[x - 1][y].pieceonTile.tostring() == '-'):
                    legalmoves.append([x - 1, y])
                    if (gametiles[x - 2][y].pieceonTile.tostring() == '-'):
                        legalmoves.append([x - 2, y])
                if (y + 1 > 7):
                    if (gametiles[x - 1][y - 1].pieceonTile.alliance == 'Black'):
                        legalmoves.append([x - 1, y - 1])
                if (y - 1 < 0):
                    if (gametiles[x - 1][y + 1].pieceonTile.alliance == 'Black'):
                        legalmoves.append([x - 1, y + 1])
                if (y + 1 < 8 and y - 1 >= 0):
                    if (gametiles[x - 1][y - 1].pieceonTile.alliance == 'Black'):
                        legalmoves.append([x - 1, y - 1])
                    if (gametiles[x - 1][y + 1].pieceonTile.alliance == 'Black'):
                        legalmoves.append([x - 1, y + 1])
                return legalmoves



            else:
                if x > 0:
                    if (gametiles[x - 1][y].pieceonTile.tostring() == '-'):
                        legalmoves.append([x - 1, y])
                    if (y + 1 > 7):
                        if (gametiles[x - 1][y - 1].pieceonTile.alliance == 'Black'):
                            legalmoves.append([x - 1, y - 1])
                    if (y - 1 < 0):
                        if (gametiles[x - 1][y + 1].pieceonTile.alliance == 'Black'):
                            legalmoves.append([x - 1, y + 1])
                    if (y + 1 < 8 and y - 1 >= 0):
                        if (gametiles[x - 1][y - 1].pieceonTile.alliance == 'Black'):
                            legalmoves.append([x - 1, y - 1])
                        if (gametiles[x - 1][y + 1].pieceonTile.alliance == 'Black'):
                            legalmoves.append([x - 1, y + 1])

                return legalmoves

    def legalmoveQueen(self, gametiles, x, y):
        legalmoves = []
        a = 0
        b = 0
        count = 0
        if (gametiles[x][y].pieceonTile.alliance == 'Black'):
            while True:
                if (count == 0):
                    a = x + 1
                    b = y + 1
                    count = count + 1
                else:
                    a = a + 1
                    b = b + 1
                if (a < 8 and b < 8 and gametiles[a][b].pieceonTile.alliance is None):
                    legalmoves.append([a, b])
                    continue
                elif (a < 8 and b < 8 and gametiles[a][b].pieceonTile.alliance == 'White'):
                    legalmoves.append([a, b])
                    break
                else:
                    break

            count = 0
            while True:

                if (count == 0):
                    a = x - 1
                    b = y - 1
                    count = count + 1
                else:
                    a = a - 1
                    b = b - 1
                if (a >= 0 and b >= 0 and gametiles[a][b].pieceonTile.alliance is None):
                    legalmoves.append([a, b])
                    continue
                elif (a >= 0 and b >= 0 and gametiles[a][b].pieceonTile.alliance == 'White'):
                    legalmoves.append([a, b])
                    break
                else:
                    break

            count = 0
            while True:
                if (count == 0):
                    a = x + 1
                    b = y - 1
                    count = count + 1
                else:
                    a = a + 1
                    b = b - 1
                if (a < 8 and b >= 0 and gametiles[a][b].pieceonTile.alliance is None):
                    legalmoves.append([a, b])
                    continue
                elif (a < 8 and b >= 0 and gametiles[a][b].pieceonTile.alliance == 'White'):
                    legalmoves.append([a, b])
                    break
                else:
                    break

            count = 0
            while True:
                if (count == 0):
                    a = x - 1
                    b = y + 1
                    count = count + 1
                else:
                    a = a - 1
                    b = b + 1
                if (a >= 0 and b < 8 and gametiles[a][b].pieceonTile.alliance is None):
                    legalmoves.append([a, b])
                    continue
                elif (a >= 0 and b < 8 and gametiles[a][b].pieceonTile.alliance == 'White'):
                    legalmoves.append([a, b])
                    break
                else:
                    break

            count = 0
            while True:
                if (count == 0):
                    a = x + 1
                    b = y
                    count = count + 1
                else:
                    a = a + 1
                if (a < 8 and gametiles[a][b].pieceonTile.alliance is None):
                    legalmoves.append([a, b])
                    continue
                elif (a < 8 and gametiles[a][b].pieceonTile.alliance == 'White'):
                    legalmoves.append([a, b])
                    break
                else:
                    break

            count = 0
            while True:
                if (count == 0):
                    a = x - 1
                    b = y
                    count = count + 1
                else:
                    a = a - 1
                if (a >= 0 and gametiles[a][b].pieceonTile.alliance is None):
                    legalmoves.append([a, b])
                    continue
                elif (a >= 0 and gametiles[a][b].pieceonTile.alliance == 'White'):
                    legalmoves.append([a, b])
                    break
                else:
                    break

            count = 0
            while True:
                if (count == 0):
                    a = x
                    b = y + 1
                    count = count + 1
                else:
                    b = b + 1
                if (b < 8 and gametiles[a][b].pieceonTile.alliance is None):
                    legalmoves.append([a, b])
                    continue
                elif (b < 8 and gametiles[a][b].pieceonTile.alliance == 'White'):
                    legalmoves.append([a, b])
                    break
                else:
                    break

            count = 0
            while True:
                if (count == 0):
                    a = x
                    b = y - 1
                    count = count + 1
                else:
                    b = b - 1
                if (b >= 0 and gametiles[a][b].pieceonTile.alliance is None):
                    legalmoves.append([a, b])
                    continue
                elif (b >= 0 and gametiles[a][b].pieceonTile.alliance == 'White'):
                    legalmoves.append([a, b])
                    break
                else:
                    break

            return legalmoves

        else:
            while True:
                if (count == 0):
                    a = x + 1
                    b = y + 1
                    count = count + 1
                else:
                    a = a + 1
                    b = b + 1
                if (a < 8 and b < 8 and gametiles[a][b].pieceonTile.alliance is None):
                    legalmoves.append([a, b])
                    continue
                elif (a < 8 and b < 8 and gametiles[a][b].pieceonTile.alliance == 'Black'):
                    legalmoves.append([a, b])
                    break
                else:
                    break

            count = 0
            while True:

                if (count == 0):
                    a = x - 1
                    b = y - 1
                    count = count + 1
                else:
                    a = a - 1
                    b = b - 1
                if (a >= 0 and b >= 0 and gametiles[a][b].pieceonTile.alliance is None):
                    legalmoves.append([a, b])
                    continue
                elif (a >= 0 and b >= 0 and gametiles[a][b].pieceonTile.alliance == 'Black'):
                    legalmoves.append([a, b])
                    break
                else:
                    break

            count = 0
            while True:
                if (count == 0):
                    a = x + 1
                    b = y - 1
                    count = count + 1
                else:
                    a = a + 1
                    b = b - 1
                if (a < 8 and b >= 0 and gametiles[a][b].pieceonTile.alliance is None):
                    legalmoves.append([a, b])
                    continue
                elif (a < 8 and b >= 0 and gametiles[a][b].pieceonTile.alliance == 'Black'):
                    legalmoves.append([a, b])
                    break
                else:
                    break

            count = 0
            while True:
                if (count == 0):
                    a = x - 1
                    b = y + 1
                    count = count + 1
                else:
                    a = a - 1
                    b = b + 1
                if (a >= 0 and b < 8 and gametiles[a][b].pieceonTile.alliance is None):
                    legalmoves.append([a, b])
                    continue
                elif (a >= 0 and b < 8 and gametiles[a][b].pieceonTile.alliance == 'Black'):
                    legalmoves.append([a, b])
                    break
                else:
                    break

            count = 0
            while True:
                if (count == 0):
                    a = x + 1
                    b = y
                    count = count + 1
                else:
                    a = a + 1
                if (a < 8 and gametiles[a][b].pieceonTile.alliance is None):
                    legalmoves.append([a, b])
                    continue
                elif (a < 8 and gametiles[a][b].pieceonTile.alliance == 'Black'):
                    legalmoves.append([a, b])
                    break
                else:
                    break

            count = 0
            while True:
                if (count == 0):
                    a = x - 1
                    b = y
                    count = count + 1
                else:
                    a = a - 1
                if (a >= 0 and gametiles[a][b].pieceonTile.alliance is None):
                    legalmoves.append([a, b])
                    continue
                elif (a >= 0 and gametiles[a][b].pieceonTile.alliance == 'Black'):
                    legalmoves.append([a, b])
                    break
                else:
                    break

            count = 0
            while True:
                if (count == 0):
                    a = x
                    b = y + 1
                    count = count + 1
                else:
                    b = b + 1
                if (b < 8 and gametiles[a][b].pieceonTile.alliance is None):
                    legalmoves.append([a, b])
                    continue
                elif (b < 8 and gametiles[a][b].pieceonTile.alliance == 'Black'):
                    legalmoves.append([a, b])
                    break
                else:
                    break

            count = 0
            while True:
                if (count == 0):
                    a = x
                    b = y - 1
                    count = count + 1
                else:
                    b = b - 1
                if (b >= 0 and gametiles[a][b].pieceonTile.alliance is None):
                    legalmoves.append([a, b])
                    continue
                elif (b >= 0 and gametiles[a][b].pieceonTile.alliance == 'Black'):
                    legalmoves.append([a, b])
                    break
                else:
                    break

            return legalmoves

    def legalmoveRook(self, gameTiles, x, y):
        legalmoves = []
        a = 0
        b = 0
        count = 0
        if (gameTiles[x][y].pieceonTile.alliance == 'Black'):
            while True:
                if (count == 0):
                    a = x + 1
                    b = y
                    count = count + 1
                else:
                    a = a + 1
                if (a < 8 and gameTiles[a][b].pieceonTile.alliance is None):
                    legalmoves.append([a, b])
                    continue
                elif (a < 8 and gameTiles[a][b].pieceonTile.alliance == 'White'):
                    legalmoves.append([a, b])
                    break
                else:
                    break

            count = 0
            while True:
                if (count == 0):
                    a = x - 1
                    b = y
                    count = count + 1
                else:
                    a = a - 1
                if (a >= 0 and gameTiles[a][b].pieceonTile.alliance is None):
                    legalmoves.append([a, b])
                    continue
                elif (a >= 0 and gameTiles[a][b].pieceonTile.alliance == 'White'):
                    legalmoves.append([a, b])
                    break
                else:
                    break

            count = 0
            while True:
                if (count == 0):
                    a = x
                    b = y + 1
                    count = count + 1
                else:
                    b = b + 1
                if (b < 8 and gameTiles[a][b].pieceonTile.alliance is None):
                    legalmoves.append([a, b])
                    continue
                elif (b < 8 and gameTiles[a][b].pieceonTile.alliance == 'White'):
                    legalmoves.append([a, b])
                    break
                else:
                    break

            count = 0
            while True:
                if (count == 0):
                    a = x
                    b = y - 1
                    count = count + 1
                else:
                    b = b - 1
                if (b >= 0 and gameTiles[a][b].pieceonTile.alliance is None):
                    legalmoves.append([a, b])
                    continue
                elif (b >= 0 and gameTiles[a][b].pieceonTile.alliance == 'White'):
                    legalmoves.append([a, b])
                    break
                else:
                    break

            return legalmoves

        else:
            while True:
                if (count == 0):
                    a = x + 1
                    b = y
                    count = count + 1
                else:
                    a = a + 1
                if (a < 8 and gameTiles[a][b].pieceonTile.alliance is None):
                    legalmoves.append([a, b])
                    continue
                elif (a < 8 and gameTiles[a][b].pieceonTile.alliance == 'Black'):
                    legalmoves.append([a, b])
                    break
                else:
                    break

            count = 0
            while True:
                if (count == 0):
                    a = x - 1
                    b = y
                    count = count + 1
                else:
                    a = a - 1
                if (a >= 0 and gameTiles[a][b].pieceonTile.alliance is None):
                    legalmoves.append([a, b])
                    continue
                elif (a >= 0 and gameTiles[a][b].pieceonTile.alliance == 'Black'):
                    legalmoves.append([a, b])
                    break
                else:
                    break

            count = 0
            while True:
                if (count == 0):
                    a = x
                    b = y + 1
                    count = count + 1
                else:
                    b = b + 1
                if (b < 8 and gameTiles[a][b].pieceonTile.alliance is None):
                    legalmoves.append([a, b])
                    continue
                elif (b < 8 and gameTiles[a][b].pieceonTile.alliance == 'Black'):
                    legalmoves.append([a, b])
                    break
                else:
                    break

            count = 0
            while True:
                if (count == 0):
                    a = x
                    b = y - 1
                    count = count + 1
                else:
                    b = b - 1
                if (b >= 0 and gameTiles[a][b].pieceonTile.alliance is None):
                    legalmoves.append([a, b])
                    continue
                elif (b >= 0 and gameTiles[a][b].pieceonTile.alliance == 'Black'):
                    legalmoves.append([a, b])
                    break
                else:
                    break

            return legalmoves

    def print_debug(self, gametiles, control_list_black):
        count = 0
        for rows in range(8):
            for column in range(8):
                if 0:
                    print('|', end="X")
                else:
                    print('|', end=gametiles[rows][column].pieceonTile.tostring())
            print("|", end='\n')

    def calculateb(self, gametiles):

        begin_weights = {
            'p': [
                0, 0, 0, 0, 0, 0, 0, 0,
                50, 50, 50, 50, 50, 50, 50, 50,
                10, 10, 20, 30, 30, 20, 10, 10,
                5, 5, 10, 25, 25, 10, 5, 5,
                0, 0, 0, 20, 20, 0, 0, 0,
                5, -5, -10, 0, 0, -10, -5, 5,
                5, 10, 10, -20, -20, 10, 10, 5,
                0, 0, 0, 0, 0, 0, 0, 0
            ],
            'n': [
                -50, -40, -30, -30, -30, -30, -40, -50,
                -40, -20, 0, 0, 0, 0, -20, -40,
                -30, 0, 10, 15, 15, 10, 0, -30,
                -30, 5, 15, 20, 20, 15, 5, -30,
                -30, 0, 15, 20, 20, 15, 0, -30,
                -30, 5, 10, 15, 15, 10, 5, -30,
                -40, -20, 0, 5, 5, 0, -20, -40,
                -50, -40, -30, -30, -30, -30, -40, -50,
            ],
            'b': [
                -20, -10, -10, -10, -10, -10, -10, -20,
                -10, 0, 0, 0, 0, 0, 0, -10,
                -10, 0, 5, 10, 10, 5, 0, -10,
                -10, 5, 5, 10, 10, 5, 5, -10,
                -10, 0, 10, 10, 10, 10, 0, -10,
                -10, 10, 10, 10, 10, 10, 10, -10,
                -10, 5, 0, 0, 0, 0, 5, -10,
                -20, -10, -10, -10, -10, -10, -10, -20,
            ],
            'r': [
                0, 0, 0, 0, 0, 0, 0, 0,
                5, 10, 10, 10, 10, 10, 10, 5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                0, 0, 0, 5, 5, 0, 0, 0
            ],
            'q': [
                -20, -10, -10, -5, -5, -10, -10, -20,
                -10, 0, 0, 0, 0, 0, 0, -10,
                -10, 0, 5, 5, 5, 5, 0, -10,
                -5, 0, 5, 5, 5, 5, 0, -5,
                0, 0, 5, 5, 5, 5, 0, -5,
                -10, 5, 5, 5, 5, 5, 0, -10,
                -10, 0, 5, 0, 0, 0, 0, -10,
                -20, -10, -10, -5, -5, -10, -10, -20
            ],
            'k': [
                -20, -10, -10, -10, -10, -10, -10, -20,
                -5, 0, 5, 5, 5, 5, 0, -5, -10, -5,
                20, 30, 30, 20, -5, -10, -15, -10,
                35, 45, 45, 35, -10, -15, -20, -15,
                30, 40, 40, 30, -15, -20, -25, -20,
                20, 25, 25, 20, -20, -25, -30, -25,
                0, 0, 0, 0, -25, -30, -50, -30, -30,
                -30, -30, -30, -30, -50
            ]
        }

        end_weights = {
            'p': [
                1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000,
                80, 80, 80, 80, 80, 80, 80, 80,
                50, 50, 50, 50, 50, 50, 50, 50,
                30, 30, 30, 30, 30, 30, 30, 30,
                20, 20, 20, 20, 20, 20, 20, 20,
                10, 10, 10, 10, 10, 10, 10, 10,
                10, 10, 10, 10, 10, 10, 10, 10,
                0, 0, 0, 0, 0, 0, 0, 0
            ],
            'n': [
                -60, -40, -10, -30, -30, -30, -52, -100,
                -40, -10, -25, -2, -10, -25, -25, -50,
                -40, -20, 10, 10, -1, -10, -20, -40,
                -20, 1, 22, 22, 22, 10, 10, -20,
                -20, -1, 20, 25, 20, 20, 4, -20,
                -20, -1, -1, 15, 10, -3, -20, -22,
                -40, -20, -10, -5, -2, -20, -23, -40,
                -30, -50, -20, -15, -20, -20, -50, -60
            ],
            'b': [
                -20, -10, -10, -10, -10, -10, -10, -20,
                -10, 0, 0, 0, 0, 0, 0, -10,
                -10, 0, 5, 10, 10, 5, 0, -10,
                -10, 5, 5, 10, 10, 5, 5, -10,
                -10, 0, 10, 10, 10, 10, 0, -10,
                -10, 10, 10, 10, 10, 10, 10, -10,
                -10, 5, 0, 0, 0, 0, 5, -10,
                -20, -10, -10, -10, -10, -10, -10, -20,
            ],
            'r': [
                0, 0, 0, 0, 0, 0, 0, 0,
                5, 10, 10, 10, 10, 10, 10, 5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                0, 0, 0, 5, 5, 0, 0, 0
            ],
            'q': [
                -20, -10, -10, -5, -5, -10, -10, -20,
                -10, 0, 0, 0, 0, 0, 0, -10,
                -10, 0, 5, 5, 5, 5, 0, -10,
                -5, 0, 5, 5, 5, 5, 0, -5,
                0, 0, 5, 5, 5, 5, 0, -5,
                -10, 5, 5, 5, 5, 5, 0, -10,
                -10, 0, 5, 0, 0, 0, 0, -10,
                -20, -10, -10, -5, -5, -10, -10, -20
            ],
            'k': [
                -70, 20, 20, -10, -60, -30, 0, 10,
                30, -1, -20, -10, -10, -10, -20, -30,
                -10, 24, 2, -20, -20, 10, 20, -20,
                -20, -20, -12, -30, -30, -25, -15, -40,
                -50, -1, -30, -40, -50, -40, -30, -50,
                -20, -14, -20, -50, -50, -30, -20, -30,
                1, 7, -8, -60, -40, -20, 10, 10,
                -15, 40, 10, -50, 10, -28, 20, 10
            ]
        }


        ## Hyper Parameters
        value = 1

        piece_values = {
            'P': 100,
            'N': 300,
            'B': 400,
            'R': 500,
            'Q': 1000,
            'K': 10000,
            'p': 100,
            'n': 300,
            'b': 400,
            'r': 500,
            'q': 1000,
            'k': 100000
        }
        ##



        piece_values_d = {
            '-': 0,
            'k': 0,
            'p': 1,
            'n': 2,
            'b': 2,
            'r': 2,
            'q': 4,
        }

        duration = 0
        for x in range(8):
            for y in range(8):
                duration += piece_values_d[gametiles[y][x].pieceonTile.tostring().lower()]

        for x in range(8):
            for y in range(8):
                if gametiles[y][x].pieceonTile.tostring() != '-':
                    index_black = (y) * 8 + (7 - x)
                    index_white = y * 8 + x
                    if gametiles[y][x].pieceonTile.alliance == "Black":
                        if duration < 22:
                            value -= begin_weights[gametiles[y][x].pieceonTile.tostring().lower()][
                                index_black]
                        else:
                            value -= end_weights[gametiles[y][x].pieceonTile.tostring().lower()][
                                index_black]
                        value -= 10 * piece_values[gametiles[y][x].pieceonTile.tostring().lower()]

                    if gametiles[y][x].pieceonTile.alliance == "White":
                        if duration < 22:
                            value += begin_weights[gametiles[y][x].pieceonTile.tostring().lower()][
                                index_white]
                        else:
                            value += end_weights[gametiles[y][x].pieceonTile.tostring().lower()][
                                index_white]
                        value += 10 * piece_values[gametiles[y][x].pieceonTile.tostring().lower()]


        control_list_white = []
        control_list_black = []
        piece_control_white = dict()
        piece_control_black = dict()
        ##################################
        # Gathers the spaces that each piece can attack
        for x in range(8):
            for y in range(8):
                if gametiles[y][x].pieceonTile.tostring() != '-':
                    if gametiles[y][x].pieceonTile.alliance == "Black":  ## Legal moves given in [column, row]
                        if gametiles[y][x].pieceonTile.tostring().lower() == 'k':
                            control_list_black = control_list_black + self.legalmoveKing(gametiles, y, x)
                            piece_control_black[gametiles[y][x].pieceonTile.tostring()] = self.legalmoveKing(gametiles,
                                                                                                             y, x)
                        if gametiles[y][x].pieceonTile.tostring().lower() == 'q':
                            control_list_black = control_list_black + self.legalmoveQueen(gametiles, y, x)
                            piece_control_black[gametiles[y][x].pieceonTile.tostring()] = self.legalmoveQueen(gametiles,
                                                                                                              y, x)
                        if gametiles[y][x].pieceonTile.tostring().lower() == 'r':
                            control_list_black = control_list_black + self.legalmoveRook(gametiles, y, x)
                            piece_control_black[gametiles[y][x].pieceonTile.tostring()] = self.legalmoveRook(gametiles,
                                                                                                             y, x)
                        if gametiles[y][x].pieceonTile.tostring().lower() == 'n':
                            control_list_black = control_list_black + self.legalmoveKnight(gametiles, y, x)
                            piece_control_black[gametiles[y][x].pieceonTile.tostring()] = self.legalmoveKnight(
                                gametiles,
                                y, x)
                        if gametiles[y][x].pieceonTile.tostring().lower() == 'b':
                            control_list_black = control_list_black + self.legalmoveBishop(gametiles, y, x)
                            piece_control_black[gametiles[y][x].pieceonTile.tostring()] = self.legalmoveBishop(
                                gametiles,
                                y, x)
                        if gametiles[y][x].pieceonTile.tostring().lower() == 'p':
                            control_list_black = control_list_black + self.legalmovePawn(gametiles, y, x)
                            piece_control_black[gametiles[y][x].pieceonTile.tostring()] = self.legalmovePawn(gametiles,
                                                                                                             y, x)


                    if gametiles[y][x].pieceonTile.alliance == "White":
                        if gametiles[y][x].pieceonTile.tostring().lower() == 'k':
                            control_list_white = control_list_white + self.legalmoveKing(gametiles, y, x)
                            piece_control_white[gametiles[y][x].pieceonTile.tostring()] = self.legalmoveKing(gametiles,
                                                                                                             y, x)
                        if gametiles[y][x].pieceonTile.tostring().lower() == 'q':
                            control_list_white = control_list_white + self.legalmoveQueen(gametiles, y, x)
                            piece_control_white[gametiles[y][x].pieceonTile.tostring()] = self.legalmoveQueen(gametiles,
                                                                                                              y, x)
                        if gametiles[y][x].pieceonTile.tostring().lower() == 'r':
                            control_list_white = control_list_white + self.legalmoveRook(gametiles, y, x)
                            piece_control_white[gametiles[y][x].pieceonTile.tostring()] = self.legalmoveKing(gametiles,
                                                                                                             y, x)
                        if gametiles[y][x].pieceonTile.tostring().lower() == 'n':
                            control_list_white = control_list_white + self.legalmoveKnight(gametiles, y, x)
                            piece_control_white[gametiles[y][x].pieceonTile.tostring()] = self.legalmoveKnight(
                                gametiles,
                                y, x)
                        if gametiles[y][x].pieceonTile.tostring().lower() == 'b':
                            control_list_white = control_list_white + self.legalmoveBishop(gametiles, y, x)
                            piece_control_white[gametiles[y][x].pieceonTile.tostring()] = self.legalmoveBishop(
                                gametiles,
                                y, x)
                        if gametiles[y][x].pieceonTile.tostring().lower() == 'p':
                            control_list_white = control_list_white + self.legalmovePawn(gametiles, y, x)
                            piece_control_white[gametiles[y][x].pieceonTile.tostring()] = self.legalmovePawn(gametiles,
                                                                                                             y, x)
        ############################
        # value += (len(control_list_black) - len(control_list_white)) * space_control
        freq_black = dict()
        for item in control_list_black:
            if tuple(item) in freq_black:
                freq_black[tuple(item)] += 1
            else:
                freq_black[tuple(item)] = 1

        freq_white = dict()
        for item in control_list_white:
            if tuple(item) in freq_white:
                freq_white[tuple(item)] += 1
            else:
                freq_white[tuple(item)] = 1


        xk, yk = 0, 0
        piece_count = 0
        for x in range(8):
            for y in range(8):
                if gametiles[y][x].pieceonTile.tostring() != '-':
                    piece = gametiles[y][x].pieceonTile.tostring()
                    if gametiles[y][x].pieceonTile.alliance == "White":
                        piece_count += 1
                        if piece == 'k':
                            yk = y
                            xk = x

        if piece_count <= 2:
            value -= len(control_list_black) * 5
            if [yk, xk] in control_list_black:
                value -= 5
        # if duration > 23:
        #     for x in range(8):
        #         for y in range(8):
        #             if gametiles[y][x].pieceonTile.tostring() != '-':
        #                 piece = gametiles[y][x].pieceonTile.tostring()
        #                 if gametiles[y][x].pieceonTile.alliance == "Black":
        #
        #
        #                     if [y, x] in control_list_white:  ## disadvantage to black
        #                         value += piece_values[piece]
        #
        #                     if [y, x] in control_list_black:  ## advantage to black
        #                         value -= piece_values[piece] * 2
        #
        #                 # if gametiles[y][x].pieceonTile.alliance == "White":
        #                 #
        #                 #     # if [y, x] in control_list_black:  ## disadvantage to white
        #                 #     #     value -= (piece_values[piece])
        #                 # #
        #                 # #     # if [y, x] in control_list_white:  ## disadvantage to black
        #                 # #     #     value += ((freq_black[(y, x)] + 1)) / piece_values[piece]

        return value

    def move(self, gametiles, y, x, n, m):
        promotion = False
        if gametiles[y][x].pieceonTile.tostring() == 'K' or gametiles[y][x].pieceonTile.tostring() == 'R':
            gametiles[y][x].pieceonTile.moved = True

        if gametiles[y][x].pieceonTile.tostring() == 'K' and m == x + 2:
            gametiles[y][x + 1].pieceonTile = gametiles[y][x + 3].pieceonTile
            s = self.updateposition(y, x + 1)
            gametiles[y][x + 1].pieceonTile.position = s
            gametiles[y][x + 3].pieceonTile = nullpiece()
        if gametiles[y][x].pieceonTile.tostring() == 'K' and m == x - 2:
            gametiles[y][x - 1].pieceonTile = gametiles[y][0].pieceonTile
            s = self.updateposition(y, x - 1)
            gametiles[y][x - 1].pieceonTile.position = s
            gametiles[y][0].pieceonTile = nullpiece()

        if gametiles[y][x].pieceonTile.tostring() == 'P' and y + 1 == n and y == 6:
            promotion = True

        if promotion == False:
            gametiles[n][m].pieceonTile = gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile = nullpiece()
            s = self.updateposition(n, m)
            gametiles[n][m].pieceonTile.position = s

        if promotion == True:

            if gametiles[y][x].pieceonTile.tostring() == 'P':
                gametiles[y][x].pieceonTile = nullpiece()
                gametiles[n][m].pieceonTile = queen('Black', self.updateposition(n, m))
                promotion = False

        return gametiles

    def revmove(self, gametiles, x, y, n, m, mts):
        if gametiles[x][y].pieceonTile.tostring() == 'K':
            if m == y - 2:
                gametiles[x][y].pieceonTile.moved = False
                gametiles[n][m].pieceonTile = gametiles[x][y].pieceonTile
                s = self.updateposition(n, m)
                gametiles[n][m].pieceonTile.position = s
                gametiles[n][7].pieceonTile = gametiles[x][y - 1].pieceonTile
                s = self.updateposition(n, 7)
                gametiles[n][7].pieceonTile.position = s
                gametiles[n][7].pieceonTile.moved = False

                gametiles[x][y].pieceonTile = nullpiece()
                gametiles[x][y - 1].pieceonTile = nullpiece()

            elif m == y + 2:
                gametiles[x][y].pieceonTile.moved = False
                gametiles[n][m].pieceonTile = gametiles[x][y].pieceonTile
                s = self.updateposition(n, m)
                gametiles[n][m].pieceonTile.position = s
                gametiles[n][0].pieceonTile = gametiles[x][y + 1].pieceonTile
                s = self.updateposition(m, 0)
                gametiles[n][0].pieceonTile.position = s
                gametiles[n][0].pieceonTile.moved = False
                gametiles[x][y].pieceonTile = nullpiece()
                gametiles[x][y - 1].pieceonTile = nullpiece()

            else:
                gametiles[n][m].pieceonTile = gametiles[x][y].pieceonTile
                s = self.updateposition(n, m)
                gametiles[n][m].pieceonTile.position = s
                gametiles[x][y].pieceonTile = mts

            return gametiles

        if gametiles[x][y].pieceonTile.tostring() == 'k':
            if m == y - 2:

                gametiles[n][m].pieceonTile = gametiles[x][y].pieceonTile
                s = self.updateposition(n, m)
                gametiles[n][m].pieceonTile.position = s
                gametiles[n][7].pieceonTile = gametiles[x][y - 1].pieceonTile
                s = self.updateposition(n, 7)
                gametiles[n][7].pieceonTile.position = s
                gametiles[x][y].pieceonTile = nullpiece()
                gametiles[x][y - 1].pieceonTile = nullpiece()


            elif m == y + 2:

                gametiles[n][m].pieceonTile = gametiles[x][y].pieceonTile
                s = self.updateposition(n, m)
                gametiles[n][m].pieceonTile.position = s
                gametiles[n][0].pieceonTile = gametiles[x][y + 1].pieceonTile
                s = self.updateposition(n, 0)
                gametiles[n][0].pieceonTile.position = s
                gametiles[x][y].pieceonTile = nullpiece()
                gametiles[x][y - 1].pieceonTile = nullpiece()


            else:
                gametiles[n][m].pieceonTile = gametiles[x][y].pieceonTile
                s = self.updateposition(n, m)
                gametiles[n][m].pieceonTile.position = s
                gametiles[x][y].pieceonTile = mts

            return gametiles

        gametiles[n][m].pieceonTile = gametiles[x][y].pieceonTile
        s = self.updateposition(n, m)
        gametiles[n][m].pieceonTile.position = s
        gametiles[x][y].pieceonTile = mts

        return gametiles

    def movew(self, gametiles, y, x, n, m):
        promotion = False
        if gametiles[y][x].pieceonTile.tostring() == 'k' or gametiles[y][x].pieceonTile.tostring() == 'r':
            pass

        if gametiles[y][x].pieceonTile.tostring() == 'k' and m == x + 2:
            gametiles[y][x + 1].pieceonTile = gametiles[y][x + 3].pieceonTile
            s = self.updateposition(y, x + 1)
            gametiles[y][x + 1].pieceonTile.position = s
            gametiles[y][x + 3].pieceonTile = nullpiece()
        if gametiles[y][x].pieceonTile.tostring() == 'k' and m == x - 2:
            gametiles[y][x - 1].pieceonTile = gametiles[y][0].pieceonTile
            s = self.updateposition(y, x - 1)
            gametiles[y][x - 1].pieceonTile.position = s
            gametiles[y][0].pieceonTile = nullpiece()

        if gametiles[y][x].pieceonTile.tostring() == 'p' and y - 1 == n and y == 1:
            promotion = True

        if promotion == False:
            gametiles[n][m].pieceonTile = gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile = nullpiece()
            s = self.updateposition(n, m)
            gametiles[n][m].pieceonTile.position = s

        if promotion == True:

            if gametiles[y][x].pieceonTile.tostring() == 'p':
                gametiles[y][x].pieceonTile = nullpiece()
                gametiles[n][m].pieceonTile = queen('White', self.updateposition(n, m))
                promotion = False

        return gametiles
