from tkinter import *
from tkinter import messagebox
import random
class Board:
    bg_color = {
        '2': '#eee4da',
        '4': '#ede0c8',
        '8': '#edc850',
        '16': '#edc53f',
        '32': '#f67c5f',
        '64': '#f65e3b',
        '128': '#00ffff',
        '256': '#89CFF0',
        '512': '#0096FF',
        '1024': '#3F00FF',
        '2048': '#191970',}
    color={'2': '#776e65',
        '4': '#f9f6f2',
        '8': '#f9f6f2',
        '16': '#f9f6f2',
        '32': '#f9f6f2',
        '64': '#f9f6f2',
        '128': '#776e65',
        '256': '#776e65',
        '512': '#f9f6f2',
        '1024': '#f9f6f2',
        '2048': '#f9f6f2',}

    def __init__(self):
        self.n=4
        self.window=Tk()
        self.window.geometry("370x370")
        self.window.title('2048')
        ic= PhotoImage(file='2048_logo.svg.png')
        self.window.iconphoto(False,ic)
        self.gameArea=Frame(self.window, bg='azure3')
        positionRight = int(self.window.winfo_screenwidth() / 2 - 370 / 2)
        positionDown = int(self.window.winfo_screenheight() / 2 - 370 / 2)
        self.window.geometry("+{}+{}".format(positionRight, positionDown))
        self.board=[]
        self.gridCell=[[0]*4 for i in range(4)]
        self.compress=False
        self.merge=False
        self.moved=False
        self.score=0

        for i in range(4):
            rows=[]
            for j in range(4):
                l=Label(self.gameArea,text='',bg='white',font=('Nexa Bold',22,'bold'),width=4,height=2)
                l.grid(row=i,column=j,padx=7,pady=7)

                rows.append(l)
            self.board.append(rows)
        self.gameArea.grid()

    def reverse(self):
        for ind in range(4):
            i=0
            j=3
            while i<j:
                self.gridCell[ind][i],self.gridCell[ind][j]=self.gridCell[ind][j],self.gridCell[ind][i]
                i+=1
                j-=1

    def transpose(self):
        self.gridCell=[list(t) for t in zip(*self.gridCell)]

    def compress_grid(self):
        self.compress=False
        temp=[[0]*4 for i in range(4)]
        for i in range(4):
            c=0
            for j in range(4):
                if self.gridCell[i][j] != 0:
                    temp[i][c] = self.gridCell[i][j]
                    if c!=j:
                        self.compress = True
                    c+=1
        self.gridCell=temp

    def merge_grid(self):
        self.merge = False
        for i in range(4):
            for j in range(3):
                if self.gridCell[i][j]==self.gridCell[i][j+1] and self.gridCell[i][j]!=0:
                    self.gridCell[i][j]*=2
                    self.gridCell[i][j+1]=0
                    self.score+=self.gridCell[i][j]
                    self.merge=True

    def random_cell(self):
        cells=[]
        for i in range(4):
            for j in range(4):
                if self.gridCell[i][j]==0:
                    cells.append((i,j))
        curr = random.choice(cells)
        i=curr[0]
        j=curr[1]
        self.gridCell[i][j]=2

    def can_merge(self):
        for i in range(4):
            for j in range(3):
                if self.gridCell[i][j]==self.gridCell[i][j+1]:
                    return True

        for i in range(3):
            for j in range(4):
                if self.gridCell[i+1][j]==self.gridCell[i][j]:
                    return True
        return False

    def paint_grid(self):
        for i in range(4):
            for j in range(4):
                if self.gridCell[i][j]==0:
                    self.board[i][j].config(text='',bg='grey')
                else:
                    self.board[i][j].config(text=str(self.gridCell[i][j]),bg=self.bg_color.get(str(self.gridCell[i][j])),fg=self.color.get(str(self.gridCell[i][j])))


class Game:
    def __init__(self,k):
        self.k=k
        self.end=False
        self.won=False

    def start(self):
        self.k.random_cell()
        self.k.random_cell()
        self.k.paint_grid()
        self.k.window.bind('<Key>',self.link_keys)
        self.k.window.mainloop()

    def link_keys(self,event):
        if self.end or self.won:
            return
        self.k.compress=False
        self.k.merge=False
        self.k.moved=False
        key=event.keysym
        if key=='Up' or key=="w":
            self.k.transpose()
            self.k.compress_grid()
            self.k.merge_grid()
            self.k.moved=self.k.compress or self.k.merge
            self.k.compress_grid()
            self.k.transpose()
        elif key=='Down' or key=="s":
            self.k.transpose()
            self.k.reverse()
            self.k.compress_grid()
            self.k.merge_grid()
            self.k.moved = self.k.compress or self.k.merge
            self.k.compress_grid()
            self.k.reverse()
            self.k.transpose()
        elif key=='Left' or key=="a":
            self.k.compress_grid()
            self.k.merge_grid()
            self.k.moved = self.k.compress or self.k.merge
            self.k.compress_grid()
        elif key=='Right' or key=="d":
            self.k.reverse()
            self.k.compress_grid()
            self.k.merge_grid()
            self.k.moved = self.k.compress or self.k.merge
            self.k.compress_grid()
            self.k.reverse()
        else:
            pass

        self.k.paint_grid()
        print(self.k.score)
        flag=0
        for i in range(4):
            for j in range(4):
                if (self.k.gridCell[i][j]==2048):
                    flag = 1
                    break
        if (flag==1):
            self.won=True
            messagebox.showinfo('2048',message='You Won,now go and do something productive')
            return
        for i in range(4):
            for j in range(4):
                if self.k.gridCell[i][j]==0:
                    flag=1
                    break
        if not (flag or self.k.can_merge()):
            self.end=True
            messagebox.showinfo('2048', 'You Lost. Well Duh')
        if self.k.moved:
            self.k.random_cell()
        self.k.paint_grid()

print("Score:")
k=Board()
game2048=Game(k)
game2048.start()
