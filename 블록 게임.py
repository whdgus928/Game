'''
게임 설명
lefr: 왼쪽으로 한 칸 이동
right: 오른쪽으로 한 칸 이동
down: 아래로 빨리 이동
space bar: 아래로 한번에 이동

점수 기능
'''

import random as r
import turtle as t
import time
dy=[-1,0,1,0]
dx=[0,1,0,-1]

class Brick():
    def __init__(self):
        self.y=0
        self.x=6
        self.color=r.randint(1,6)

    def move_left(self,grid):
        if grid[self.y][self.x-1]==0 and grid[self.y+1][self.x-1]==0:
            grid[self.y][self.x]=0
            self.x-=1

    def move_right(self,grid):
        if grid[self.y][self.x+1]==0 and grid[self.y+1][self.x+1]==0:
            grid[self.y][self.x]=0
            self.x+=1

    def move_down(self,grid):
        if grid[self.y+1][self.x]==0 and grid[self.y+2][self.x]==0 and grid[self.y+3][self.x]==0:
            grid[self.y][self.x]=0
            self.y+=2
    def move_floor(self,grid):      
        grid[self.y][self.x]=0
        self.y=max_one_height(grid,self.x)-2

def draw_grid(block,grid):
    block.clear()
    top=250
    left=-150
    colors=['black','red','blue','orange','yellow','green','purple','white']
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            sc_x=left+(x*22)
            sc_y=top+(y*-22)
            block.goto(sc_x,sc_y)
            if y==15 and grid[y][x]==7:
                block.color('red')
            else:
                block.color(colors[grid[y][x]])
            block.stamp()
    block.goto(left,top)

def DFS(y,x,grid,color):
    global ch, blank
    ch[y][x]=1
    blank.append((y,x))
    for i in range(4):
        yy=y+dy[i]
        xx=x+dx[i]
        if 0<=yy<24 and 0<=xx<13:
            if grid[yy][xx]==color and ch[yy][xx]==0:
                DFS(yy,xx,grid,color)

def max_height(grid):
    for y in range(1,24):
        for x in range(1,13):
            if grid[y][x]!=0:
                return y
def max_one_height(grid,x):
    for y in range(1,24):
        if grid[y][x]!=0:
            return y
    else:
        return 24

def grid_update(grid,blank):
    for y,x in blank:
        grid[y][x]=0
    height=max_height(grid)
    for y in range(23,height,-1):
        for x in range(1,13):
            if grid[y][x]==0:
                tmp_y=y
                while grid[tmp_y-1][x]==0 and tmp_y-1>0:
                    tmp_y-=1
                grid[y][x]=grid[tmp_y-1][x]
                grid[tmp_y-1][x]=0

def continual_remove():
    global blank,ch
    while True:
        flag=1
        for y in range(23,15,-1):
            for x in range(1,13):
                if grid[y][x]!=0:
                    ch=[[0]*14 for _ in range(25)]
                    blank=[]
                    DFS(y,x,grid,grid[y][x])
                    if len(blank)>=4:
                        score(s)
                        grid_update(grid,blank)
                        flag=0
        draw_grid(block,grid)    
        if flag==1:
            break
def game_over():
    pen.up()
    pen.goto(-120,100)
    pen.write('Game Over',font=('couruer',30))

def you_win():
    pen.up()
    pen.goto(-100,100)
    pen.write('You Win',font=('couruer',30))
def score(score):
    if score>0:
        pen.up()
        pen.color('black')
        pen.goto(-200,290)
        pen.write(score-1,font=('couruer',15))
    pen.up()
    pen.color('white')
    pen.goto(-200,290)
    pen.write(score,font=('couruer',15))

if __name__=="__main__":
    sc=t.Screen()
    sc.tracer(False) # 빠르게 그릴때
    sc.bgcolor('black')
    sc.setup(width=600,height=700)
    grid=[[0]*12 for _ in range(24)]
    for i in range(24):
        grid[i].insert(0,7)
        grid[i].append(7)
    grid.append([7]*14)

    for y in range(23,20,-1):
        for x in range(1,13):
            grid[y][x]=r.randint(1,6)

    block=t.Turtle()
    block.penup()
    block.speed(0)
    block.color('white')
    block.shape('square')
    block.setundobuffer(None) #앞에걸 취소한다

    brick=Brick() #업데이트 해줘야 그려짐
    grid[brick.y][brick.x]=brick.color
    draw_grid(block,grid)

    pen=t.Turtle()
    pen.ht()
    pen.goto(-80,290)
    pen.color("white")
    pen.write('Block Game',font=('courier',20,'normal'))
    pen.up()
    pen.goto(-270,290)
    pen.write('score : ',font=('couruer',15))

    sc.onkeypress(lambda: brick.move_left(grid),"Left")
    sc.onkeypress(lambda: brick.move_right(grid),"Right")
    sc.onkeypress(lambda: brick.move_down(grid),"Down")
    sc.onkeypress(lambda: brick.move_floor(grid),"space")
    sc.listen()

    s=0
    while True:
        sc.update()
        score(s)
        if grid[brick.y+1][brick.x]==0:
            grid[brick.y][brick.x]=0
            brick.y+=1
            grid[brick.y][brick.x]=brick.color
        else:
            ch=[[0]*14 for _ in range(25)]
            blank=[]
            DFS(brick.y,brick.x,grid,brick.color)
            if len(blank)>=4:
                s+=1
                score(s)
                grid_update(grid,blank)
                continual_remove()

            height=max_height(grid)
            if height<=15:
                game_over()
                break
            elif height>=22:
                draw_grid(block,grid)
                you_win()
                break
            brick=Brick()

        draw_grid(block,grid)
        time.sleep(0.05)

    sc.mainloop() #없으면 창이 꺼져버림