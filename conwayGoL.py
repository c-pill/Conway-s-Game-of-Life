from tkinter import *
from random import randint
from copy import deepcopy

root = Tk()
root.title("Conway's Game of Life")
root.state('zoomed')
root.geometry('800x500')

class ValidationFunctions:
    def validateInteger(*value):
        return value[0].isdigit() or len(value[0]) == 0

    def validateFloat(*value):
        if value[0] == '':
            return True
        try:
            float(value[0])
            return True
        except ValueError:
            return False 

verifInt = (root.register(ValidationFunctions.validateInteger), '%P')
verifFloat = (root.register(ValidationFunctions.validateFloat), '%P')

size = IntVar(master=root, value=40)
size.trace_add('write', ValidationFunctions.validateInteger)

percentLive = DoubleVar(master=root, value=20.0)
percentLive.trace_add('write', ValidationFunctions.validateFloat)

playGoL = BooleanVar(master=root, value=False)

canvas = Canvas(master=root, width=500, height=500)
canvas.pack(expand=True)

class ConwayData:
    def __init__(self):
        self.generate()

    def generate(self):
        percent = percentLive.get()
        self.grid = [[1 if randint(0, 100) <= percent else 0 for _ in range(size.get())] for _ in range(size.get())]
        self.tick()
        self.intialGen = deepcopy(self.grid)

    def getNeighborCells(self, row, col):
        return [self.grid[r][c] for r in range(row-1, row+2) for c in range(col-1, col+2) if ((r != row or c != col) and 0 <= r < len(self.grid) and 0 <= c < len(self.grid))]
    
    def liveNeighborGrid(self):
        return [[self.getNeighborCells(row, col).count(1) for col in range(len(self.grid))] for row in range(len(self.grid))]

    def newStatus(self, row, col, liveNeighbors):
        status = self.grid[row][col]
        return ConwayRules.checkLiveCell(liveNeighbors) if status == 1 else ConwayRules.checkDeadCell(liveNeighbors)

    def tick(self):
        liveNeighborGrid = self.liveNeighborGrid()
        self.grid = [[self.newStatus(row, col, liveNeighborGrid[row][col]) for col in range(len(self.grid))] for row in range(len(self.grid))]
        
class ConwayRules:
    # underpopulation with < 2 live neighbors
    # overpopulation with > 3 live neighbors
    # live on with 2 or 3 live neighbors
    def checkLiveCell(liveNeighbors):
        return 1 if 2 <= liveNeighbors <= 3 else 0

    # dead cell => live cell with 3 live neighbors
    def checkDeadCell(liveNeighbors):
        return 1 if liveNeighbors == 3 else 0
    
class DisplayConway:
    def printGrid(self):
        for row in self.grid:
            print(row)

    def createCell(conwayData, row, col):
        cellSize = max(450 / len(conwayData.grid), len(conwayData.grid) / 450)
        return canvas.create_rectangle(
            col * cellSize,
            row * cellSize,
            col * cellSize + cellSize,
            row * cellSize + cellSize,
            fill=('black' if conwayData.grid[row][col] == 0 else 'white')
        )

    def displayBoard(conwayData):
        canvas.delete('all')
        conwayData.board = [[DisplayConway.createCell(conwayData, row, col) for row in range(len(conwayData.grid))] for col in range(len(conwayData.grid))]

conwayData = ConwayData()
DisplayConway.displayBoard(conwayData)

class ButtonMethods:
    def restart():
        conwayData.grid = deepcopy(conwayData.intialGen)
        DisplayConway.displayBoard(conwayData)

    def nextGeneration():
        conwayData.tick()
        DisplayConway.displayBoard(conwayData)

    def generate():
        if size.get != '':
            conwayData.generate()
            DisplayConway.displayBoard(conwayData)

    def play():
        if playGoL.get():
            ButtonMethods.nextGeneration()
            root.after(1, ButtonMethods.play)

class StartStopButton:
    def __init__(self):
        self.button = Button(master=root, text='Start')
        self.button.pack(side='left', pady=25, padx=15)
        self.button.bind('<ButtonPress>', self.toggle)

    def toggle(self, event):
        playGoL.set(not playGoL.get())
        if playGoL.get():
            self.button.config(text='Stop')
            ButtonMethods.play()
        else:
            self.button.config(text='Start')

screenHeight = root.winfo_screenheight()
screenWidth = root.winfo_screenwidth()

startStop = StartStopButton()
restart = Button(master=root, text='Restart', command=ButtonMethods.restart).pack(side='left', pady=25, padx=15)
nextGen = Button(master=root, text='Next', command=ButtonMethods.nextGeneration).pack(side='left', pady=25, padx=15)
generate = Button(master=root, text='Generate', command=ButtonMethods.generate).pack(side='left', pady=25, padx=15)

sizeLabel = Label(master=root, text='Size:').pack(side='left', pady=25, padx=15)
sizeEntry = Entry(master=root, validate='key', validatecommand=verifInt, textvariable=size).pack(side='left', pady=25, padx=15)

percentLabel = Label(master=root, text="% Live at Start:").pack(side='left', pady=25, padx=15)
percentEntry = Entry(master=root, validate='key', validatecommand=verifFloat, textvariable=percentLive).pack(side='left', pady=25, padx=15)

root.mainloop()
