import os, time, sys, subprocess
import random as rnd

def main():
    try:
        import keyboard
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'keyboard'])
        import keyboard

    class player:
        pos = []
        pno = None
        score = 0

        def __init__(self, pos, pno=None, score=None):
            self.pos = [i for i in range(pos - 2, pos + 3)]
            self.pno = pno
            score = 0

        def move(self, direction=None, ballpos=None):
            if self.pno == 1:
                if keyboard.is_pressed("w") and self.pos[0] != 1: self.pos = list(map(lambda x: x-1, self.pos))
                elif keyboard.is_pressed("s") and self.pos[4] != size - 1: self.pos = list(map(lambda x: x+1, self.pos))
            elif self.pno == 2:
                if direction == "++" and self.pos[0] != 1: self.pos = list(map(lambda x: x-1, self.pos)) if ballpos[0] < self.pos[0] and rnd.uniform(0, 1) < 0.8 else self.pos
                elif direction == "--" and self.pos[4] != size - 1: self.pos = list(map(lambda x: x+1, self.pos)) if ballpos[0] > self.pos[0] and rnd.uniform(0, 1) < 0.8 else self.pos
                elif direction == "+-" and self.pos[4] != size - 1: self.pos = list(map(lambda x: x+1, self.pos)) if ballpos[0] > self.pos[0] and rnd.uniform(0, 1) < 0.8 else self.pos
                elif direction == "-+" and self.pos[0] != 1: self.pos = list(map(lambda x: x-1, self.pos)) if ballpos[0] < self.pos[0] and rnd.uniform(0, 1) < 0.8 else self.pos

    class ball:
        x = None
        y = None
        mv = None

        def __init__(self, x, y, mv):
            self.x = x
            self.y = y
            self.mv = mv

        def reset(self):
            self.x = int(size / 2)
            self.y = int(ln / 2)
            self.mv = rnd.choice(["++", "+-", "--", "-+"])

        def bounce(self, p1 = None, p2 = None):
            if self.y == ln - 1: p1.score += 1; self.reset(); return
            elif self.y == 0: p2.score += 1; self.reset(); return
            if self.mv == "++":
                if self.x == 1: self.mv = "+-"
                elif self.y == ln - 2 and self.x in rpl.pos: self.mv = "-+"
            elif self.mv == "--":
                if self.x == size - 1: self.mv = "-+"
                elif self.y == 1 and self.x in lpl.pos: self.mv = "+-"
            elif self.mv == "-+":
                if self.x == 1: self.mv = "--"
                elif self.y == 1 and self.x in lpl.pos: self.mv = "++"
            elif self.mv == "+-":
                if self.y == ln - 2 and self.x in rpl.pos: self.mv = "--"
                elif self.x == size - 1: self.mv = "++"
                
        def move(self):
            if self.mv == "++":
                self.x -= 1
                self.y += 1
            elif self.mv == "--":
                self.x += 1
                self.y -= 1
            elif self.mv == "+-":
                self.x += 1
                self.y += 1
            elif self.mv == "-+":
                self.x -= 1
                self.y -= 1

        def pos(self):
            return (self.x, self.y)

    def gridReset(grid):
        grid = [[" " for i in range(ln)] for j in range(size)]
        return grid

    size = 40; ln = size + int(size / 4); mv = rnd.choice(["++", "+-", "--", "-+"])
    grid = [[" " for i in range(ln)] for j in range(size)]
    ball = ball(int(size / 2), int(ln / 2), mv)
    lpl = player(int(size / 2), 1); rpl = player(int(size / 2), 2)
    spd = 0.05
    while True:
        grid = gridReset(grid)
        grid[ball.pos()[0]][ball.pos()[1]] = repr(chr(11203))[1]
        for i in lpl.pos:
            grid[i][1] = repr(chr(9611))[1]
        for i in rpl.pos:
            grid[i][ln - 2] = repr(chr(9611))[1]
        for i in range(size):
            grid[i][int(ln / 2)] = repr(chr(9474))[1]
            print(repr(chr(9616))[1] + " ".join(grid[i]) + repr(chr(9611))[1])
        ball.bounce(lpl, rpl)
        ball.move(); rpl.move(ball.mv, (ball.x, ball.y)); lpl.move()
        time.sleep(spd)
        os.system("cls")