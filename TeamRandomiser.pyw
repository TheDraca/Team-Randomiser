import random
from tkinter import *
from tkinter import ttk
import platform

###SETUP Window Classes####
class window(Tk):
    WindowSize="250x250"
    def __init__(self,WindowSize=WindowSize):
        Tk.__init__(self)
        self.title("Draca's Shitty Team Randomiser")
        if "Windows" not in platform.platform():
            self.attributes('-type', 'dialog') #Makes the windows free floating for certian unix window managers that like to force full screen
        #self.titlelabel()
        self.geometry(WindowSize)
    def titlelabel(self, text="Draca's Shitty Team Ranndomiser", XPos=(int(WindowSize.split("x")[0])//2), YPos=10, Anchor="center" ):
       #Label(self, text=text).place(anchor=Anchor, x=XPos, y=YPos) #Place the main label in the center by getting half the value of the X Window Size
        Label(self, text=text).grid(row=0,column=0,sticky=N) #Enter a blank row to allow for other text using columns/rows to be positioned around title

    def label(self, text, row, column, sticky):
        Label(self, text=text).grid(row=row,column=column,sticky=sticky,)

    def button(self, text, command, row, column, sticky):
        Button(self, text=text, command=command).grid(row=row, column=column, sticky=sticky)

class dialogwindow(Tk):
    def __init__(self, WindowName="Draca's Shitty Team Randomiser"):
        Tk.__init__(self)
        self.title(WindowName)
        if "Windows" not in platform.platform():
            self.attributes('-type', 'dialog') #Makes the windows free floating for certian unix window managers that like to force full screen
        self.titlelabel(WindowName)

    def titlelabel(self, text="Draca's Shitty Team Randomiser"):
        Label(self, text=text).grid(row=0,column=0,sticky=N) #Enter a blank row to allow for other text using columns/rows to be positioned around title

    def label(self, text, row, column, sticky):
        Label(self, text=text).grid(row=row,column=column,sticky=sticky)

    def button(self, text,  row, column, sticky, command):
        Button(self, text=text, command=command).grid(row=row, column=column, sticky=sticky)

    def CloseButton(self, text, row, column, sticky):
         Button(self, text=text, command=lambda : self.destroy()).grid(row=row, column=column, sticky=sticky)


#Main Functions#
def PlayerListSplit(PlayerList, TeamSize): #Totally stole this function like 100%
    avg =  len(PlayerList) / float(TeamSize)
    output = []
    last = 0.0
    while last < len(PlayerList):
        output.append(PlayerList[int(last):int(last + avg)])
        last += avg
    return output

def CreateTeams(PlayerListEntry,TeamSize):
    RawPlayerList=PlayerListEntry.get("1.0",'end-1c')
    PlayerList=[]
    TeamSize=int(TeamSize.get())

    #Turn RawPlayerList into an acctual list that can be shuffled
    for Player in RawPlayerList.splitlines(True):
        if str(Player) != "\n":
            PlayerList.append(Player.strip())

    #Stop user from entering 0 and breaking everything, or have the same number of players as teams, or too many teams:
    if TeamSize == 0 or TeamSize == 1:
        BadTeamSizeWindow=dialogwindow()
        BadTeamSizeWindow.label("You can't have 0 or 1 teams -_-",1,0,N)
        BadTeamSizeWindow.CloseButton("Close",2,0,N)
    elif int(len(PlayerList)) == TeamSize:
        BadTeamSizeWindow=dialogwindow()
        BadTeamSizeWindow.label("You can't have the same number of players as teams",1,0,N)
        BadTeamSizeWindow.CloseButton("Close",2,0,N)
    elif int(len(PlayerList)) < TeamSize:
        BadTeamSizeWindow=dialogwindow()
        BadTeamSizeWindow.label("You have more teams that players!",1,0,N)
        BadTeamSizeWindow.CloseButton("Close",2,0,N)
    else:
        #Randomise the playerlist
        random.shuffle(PlayerList)

        #Now acctually create the teams, then create make a readable TeamsList to display:
        TeamsList=""
        TeamsArray=list(PlayerListSplit(PlayerList,TeamSize))
        TeamsCount=1
        for Team in TeamsArray:
            TeamsList+="Team {0}:\n".format(TeamsCount)
            for Player in Team:
                TeamsList+="{0}\n".format(Player)
            TeamsList+="\n"    
            TeamsCount += 1
                
        
        #Create a window with the teams list in it
        TeamsWindow=dialogwindow()
        TeamsWindow.label("Teams are:",1,0,N)
        TeamsWindowTextBox=Text(TeamsWindow,  width=31, height=15, wrap='none')

        #Enter the teams 
        TeamsWindowTextBox.insert(END,TeamsList)

        TeamsWindowTextBox.config(state="disabled")
        TeamsWindowTextBox.grid(row=2,column=0,sticky=N)


MainWindow = window()
MainWindow.titlelabel()
#Player entry bit
MainWindow.label("Enter a playname on each line below",1,0,N)
PlayerListEntry=Text(MainWindow, width=31, height=10, wrap='none')
PlayerListEntry.grid(row=2,column=0,sticky=N)

#Create Teams bit
MainWindow.label("Team Size:",3,0,NW)
TeamSize=Spinbox(MainWindow,from_=2, to=100,width=6)
TeamSize.grid(row=4,column=0,sticky=NW)

MainWindow.button("Get Teams", lambda : CreateTeams(PlayerListEntry,TeamSize),4,0,NE)


#Spawn Main Window
MainWindow.mainloop()
