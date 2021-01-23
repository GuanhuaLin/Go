# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 22:38:37 2021

@author: LIN03
"""


class go:
    
    
    '''
    UNFINISHED FUNCTION: check_board
    PROBLEM FUNCTION: read_sgf
    '''
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    ''' available functions:
        __init__: initialization
        read_sgf(file_name): 
            give the full file name, and then read it
            all moves will be append to the move
        clear_move: clear all moves
        clear board: clear the board
        ordered_move: do a move (color given by self.turn)
        ordered_undo_move: undo the last move
        check_board: make sure the board follows Go rule
    '''
    def __init__(self, size = 19):
        self.size = size
        self.board = [[0]*size for i in range(size)]
        self.move = []
        self.turn = False # False for black and True for white
    
    def sgf_position_transform(self, pos:str):
        x = ord(pos[0])
        y = ord(pos[1])
        if x >= 97 and x <= 122:
            x -= 97
        elif x >= 65 and x <= 90:
            x -= 39
        if y >= 97 and y <= 122:
            y -= 97
        elif y >= 65 and y <= 90:
            y -= 39
        else:
            print('INVALID POSITION')
        return x,y
    
    def exe_read_cmd(self, cmd, cnt):
        if cmd in ['AB','AW','B','W']:
            x,y = self.sgf_position_transform(cnt)
            self.move.append([cmd,x,y])
        elif cmd == 'SZ':
            self.size = int(cnt)
    
    def update_board(self):
        # update the board based on self.move
        self.clear_board(True)
        #print('u',self.move)
        for move in self.move:
            if self.board[move[1]][move[2]] in [1,2]:
                continue
                print('Warning: move going on non-empty position',
                      'system will ignore thie move', sep = ', ')
            elif move[0] in ['AB', 'B']:
                self.turn = False
                self.ordered_move(move[1],move[2],False)
            else:
                self.turn = True
                self.ordered_move(move[1],move[2],False)
        if self.move == []:
            self.turn = False
        elif self.move[-1][0] == 'B':
            self.turn = True
        else:
            self.turn = False
    
    def read_sgf(self, file_name):
        self.clear_move()
        self.clear_board()
        sgf = open(file_name, mode = 'r', encoding = 'utf-8').read()
        #print(sgf,'\n--------------------------------------------------\n')
        l = len(sgf)
        pos = 0
        cmd_start = 0
        cnt_start = 0
        while pos < l:
            if sgf[pos] == '[': # end of command, start of content
                if sgf[cmd_start:pos] != '':
                    while sgf[cmd_start] in ['\n',';']: # if cmd start with it
                        cmd_start += 1
                    cmd = sgf[cmd_start:pos] # generate command
                cnt_start = pos + 1
            elif sgf[pos] == ']': # end of content, start of next command
                cnt = sgf[cnt_start:pos] # conerate command content
                cmd_start = pos + 1
                #print(cmd, cnt)
                self.exe_read_cmd(cmd, cnt) # transfer cmd into readable form
            pos += 1
        self.update_board()
    
    def clear_move(self):
        self.move = []
        self.turn = False
    
    def clear_board(self, resize = False):
        if resize:
            self.board = []
            for row in range(self.size):
                self.board.append([0]*self.size)
        else:
            l = len(self.board[0]) # size not updated, so decide size manually
            for row in self.board:
                for col in range(l):
                    row[col] = 0
    
    def clear_dead_stones_around(self, x:int, y:int):
        c = self.board[x][y]
        if c == 1:
            c = 2
        else:
            c = 1
        # now c is the opposite color of the color of x,y
        if x > 0 and self.board[x-1][y] == c and self.air(x-1,y) == 0:
            dead_stones = self.group(x-1,y)
            for stone in dead_stones:
                self.board[stone[0]][stone[1]] = 0
        if y > 0 and self.board[x][y-1] == c and self.air(x,y-1) == 0:
            dead_stones = self.group(x,y-1)
            for stone in dead_stones:
                self.board[stone[0]][stone[1]] = 0
        if x < self.size-1 and self.board[x+1][y] == c and self.air(x+1,y) == 0:
            dead_stones = self.group(x+1,y)
            for stone in dead_stones:
                self.board[stone[0]][stone[1]] = 0
        if y < self.size-1 and self.board[x][y+1] == c and self.air(x,y+1) == 0:
            dead_stones = self.group(x,y+1)
            for stone in dead_stones:
                self.board[stone[0]][stone[1]] = 0
    
    def ordered_move(self, x:int, y:int, record = True):
        if self.board[x][y] in [0,3]:
            self.board[x][y] = self.turn + 1
            if self.turn:
                if record:
                    self.move.append(['W',x,y])
                self.turn = False
            else:
                if record:
                    self.move.append(['B',x,y])
                self.turn = True
            self.clear_dead_stones_around(x,y)
            if self.air(x,y) == 0: # invalid move
                self.ordered_undo_move()
                print('Invalid move: no air')
        #print('o',self.move)
                    
    def ordered_undo_move(self):
        if self.move != []:
            _,x,y = self.move[-1]
            del(self.move[-1])
            self.update_board()
        else:
            print('No move on board!')
    
    def group(self, x:int, y:int, in_group = []):
        #print('input:',x,y,in_group)
        assert(x in range(self.size) and y in range(self.size))
        c = self.board[x][y]
        assert (c in [1,2]) # must be a position with a stone
        #print(in_group)
        in_group.append([x,y])
        if x > 0 and [x-1,y] not in in_group and self.board[x-1][y] == c:
            #print('left:', in_group)
            in_group = self.group(x-1,y,in_group)
        if y > 0 and [x,y-1] not in in_group and self.board[x][y-1] == c:
            in_group = self.group(x,y-1,in_group)
        if x < self.size-1 and [x+1,y] not in in_group and self.board[x+1][y] == c:
            in_group = self.group(x+1,y,in_group)
        if y < self.size-1 and [x,y+1] not in in_group and self.board[x][y+1] == c:
            in_group = self.group(x,y+1,in_group)
        return in_group
    
    def air(self, x:int, y:int, group = []):
        # The air of some connected stones, according to Go rule,
        # are defined by how many stones the opponent need to 'surround'
        # the up, down, left and right of the stones
        # For more detail please refer to wikipedia of Go Rule
        assert(x in range(self.size) and y in range(self.size))
        c = self.board[x][y]
        assert (c in [1,2]) # must be a position with a stone
        group = self.group(x, y)
        r = 0
        while len(group) != 0:
            x,y = group[-1]
            del(group[-1])
            if x > 0 and [x-1,y] not in group and self.board[x-1][y] in [0,3]:
                r += 1
            if y > 0 and [x,y-1] not in group and self.board[x][y-1] in [0,3]:
                r += 1
            if x < self.size-1 and [x+1,y] not in group and self.board[x+1][y] in [0,3]:
                r += 1
            if y < self.size-1 and [x,y+1] not in group and self.board[x][y+1] in [0,3]:
                r += 1
        return r       
    
    def check_board(self):
        checked = [[False]*self.size for _ in range(self.size)]
        x,y = 0,0
        while x < self.size:
            y = 0
            while y < self.size:
                if not checked[x][y]:
                    pass
                y += 1            
            x += 1
g = go(19)
#g.read_sgf('a.sgf')
'''
for elem in g.board:
    for e in elem:
        if e:
            print(e,end=' ')
        else:
            print(' ',end=' ')
    print('')
print(g.group(4,4))
'''
#for row in g.board:
#    print(row)
