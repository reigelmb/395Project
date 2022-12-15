from tkinter import *
import json
# Import tkinter and json... Obviously
import time
import sys
from PIL import ImageTk, Image


def typingPrint(text):
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)


class Player:                   #player class, handles everything relating to the player from health and status to using items
    def __init__(self):
        self.health = 10.0
        self.maxHealth = 10.0
        self.movement = 10.0
        self.burn = False
        self.poison = False
        self.cut = False
        self.stealth = False
        self.inventoryWeight = 20
        self.currInventoryWeight = 0
        self.currStatus = []

    def updateStatus(self):
        if self.burn == True and "Burn" not in self.currStatus:
            self.currStatus.append("Burn")
        if self.poison == True and "Poison" not in self.currStatus:
            self.currStatus.append("Poison")
        if self.cut == True and "cut" not in self.currStatus:
            self.currStatus.append("But")

    def removeStatus(self):
        if self.burn == False and "Burn" in self.currStatus:
            self.currStatus.append("Burn")
        if self.poison == False and "Poison" in self.currStatus:
            self.currStatus.append("Poison")
        if self.cut == False and "Cut" in self.currStatus:
            self.currStatus.append("Cut")



    def update(self, status):       #this updates everything, to be called at beginning of scenario/turn, updates health, movement, status
        # Updates movement
        if self.movement > 0:
            self.movement -= 1
        # Updates poison/checks poison
        if self.poison == True:
            self.health -= .5
            print("You took posion damage!")
        elif status == "poison":
            self.poison = True
            print("You got inflicted with poison")
            self.updateStatus()
        # Updates burn/checks burn
        if self.burn == True:
            self.health -= .5
            print(self.health)
            print("You took burn damage!")
        elif status == "burn":
            self.burn = True
            print("You got inflicted with burn")
            self.updateStatus()
        # Updates cut/checks cut
        if self.cut == True:
            self.health -= .5
            print("You took damage from your cut")
        elif status == "cut":
            self.cut = True
            print("You got inflicted with a cut")
            self.updateStatus()

    #def isAlive(self):                 #redundant function, checks if alive
     #   return self.health > 0

   # def checkItem(self, itemRequired, inventory):              #function to check if item is in inventory
    #    if itemRequired in inventory:
     #     if (inventory[itemRequired[Effect]])
      #  else:
       #     return inventory

    def removeItem(self, inventory, item, itemList):              #removes item from inventory, returns updated inventory
        if itemList["Items"][item]["isReusable"] == False:
            del inventory[item]
        return inventory


    def useItem(self, inventory, item, itemList):                #uses item, checks what they do and how much, returns updated inventory
        if item != '':
            if itemList["Items"][item]["Effect"] == "addHealth":
                self.health += float(itemList["Items"][item]["Amount"])
                if(self.health > self.maxHealth):
                    self.health = self.maxHealth
                inventory = self.removeItem(inventory, item, itemList)
            elif itemList["Items"][item]["Effect"] == "removeHealth":
                self.health -= float(itemList["Items"][item]["Amount"])
                inventory = self.removeItem(inventory, item, itemList)
            elif itemList["Items"][item]["Effect"] == "healStatus":
                self.poison = False
                self.burn = False
                self.cut = False
                self.removeStatus()
                inventory = self.removeItem(inventory, item, itemList)
            elif itemList["Items"][item]["Effect"] == "healCut":
                self.cut = False
                self.removeStatus()
                inventory = self.removeItem(inventory, item, itemList)
            elif itemList["Items"][item]["Effect"] == "healBurn":
                self.burn = False
                self.removeStatus()
                inventory = self.removeItem(inventory, item, itemList)
            elif itemList["Items"][item]["Effect"] == "healPoison":
                self.poison = False
                self.removeStatus()
                inventory = self.removeItem(inventory, item, itemList)
            elif itemList["Items"][item]["Effect"] == "givePoison":
                self.poison = True
                self.updateStatus()
                inventory = self.removeItem(inventory, item, itemList)
            elif itemList["Items"][item]["Effect"] == "giveBurn":
                self.burn = True
                self.updateStatus()
                inventory = self.removeItem(inventory, item, itemList)
            elif itemList["Items"][item]["Effect"] == "giveCut":
                self.cut = True
                self.updateStatus()
                inventory = self.removeItem(inventory, item, itemList)
            else:
                print("This item isn't implemented fully yet.")
        return inventory



    def updateInventoryWeight(self, inventory, itemList):    #updates the inventory weight
        self.currInventoryWeight = 0
        for item in inventory:
           self.currInventoryWeight += int(itemList[item]["weight"])
        if self.currInventoryWeight > self.inventoryWeight:
                print("Too much weight")
        #elif
root = Tk()
# Set variable root to tk()
root.geometry('900x900')
# Set the geometry of the root variable to 900x900
with open('chapter1.json', 'r', encoding='utf-8') as f:
    # Open json file and put store that into variable "json_object"
    json_chapter = json.load(f)

with open('ItemList.json', 'r', encoding='utf-8') as f:
    # Open json file and put store that into variable "json_object"
    json_items = json.load(f)


class Window(Frame):
    # Initialize Window class be where most of the game is created

    def __init__(self, file, items, window=None):
        Frame.__init__(self, window)
        '''Declare __init__ method which is taking in the json files for the chapters, the list of items, and
        the window which is set to None'''
        # Set self.window equal to window
        self.window = window

        # Set the background of self.window to black
        self.window['bg'] = "black"

        # Give self.window the attribute of being fullscreen
        self.window.attributes('-fullscreen', True)

        # Set variable self.file equal to the json file for the chapters
        self.file = file

        # Set variable self.items equal to the json file for the items
        self.items = items

        '''set variable self.frame to create a frame whose parent is self.window and set the background color to black
        Then create a grid for it'''
        self.frame = Frame(self.window, bg="black")
        self.frame.grid(row=0, column=0, padx=10, pady=10)

        '''
        Set the number of chapters completed so far to 0 so that when the player
        '''
        self.chapterNum = 0


        self.img = (Image.open("StartPhoto.png"))
        self.chOnePhoto = (Image.open("Chapter1Photo.jpg"))
        self.img = self.img.resize((400,400))
        self.chOnePhoto = self.chOnePhoto.resize((400,400))
        self.img = ImageTk.PhotoImage(self.img)
        self.chOnePhoto = ImageTk.PhotoImage(self.chOnePhoto)
        self.label = Label(self.frame, image=self.img, text="Typical Monday", compound=CENTER, fg="orange",
                           width=1200, wraplength=1000, justify=CENTER, bg="black")
        self.label.config(font=("Times 40 bold"))
        self.label.grid(row=0, column=0, columnspan=3, pady=50)

        '''
        Set self.title to a label. Make that labels parent self.frame, Set the text to "Typical monday and make
        sure it is properly aligned in the center.
        '''
        #self.title = Label(self.frame, text="Typical Monday", justify=CENTER, font=("Roman", 40), fg="orange",
         #                  width=50, wraplength=1000)
        '''In the grid, set self.title to row 0 and column 0. Have it span 2 columns'''
        #self.title.grid(row=0, column=0, columnspan=2, pady=100, sticky="nsew")

        '''Create self.START variable which will be a button whose parent is self.frame. Make the text for it 
        "Start" and make it call the clickStartButton function when pressed make sure it is aligned
        to the center'''
        self.START = Button(self.frame, text="Start", height=2, width=3, font=30, command=self.clickStartButton,
                            justify=CENTER, fg="black", bg="orange")

        '''Align the self.START button to be in row 2  and column 0 of the grid and have it span
        2 rows'''
        self.START.grid(row=2, column=0, rowspan=2, pady=100, ipadx=50)

        '''Create self.DIE button g'''
        self.DIE = Button(self.frame, text="Quit", height=2, width=3, font=30, command=self.clickDieButton,
                          justify=CENTER, fg="black", bg="orange")
        self.DIE.grid(row=2, column=1, rowspan=2, pady=100, ipadx=50)

        self.chapterSelect = Button(self.frame, text="Select Chapter", height=2, width=3, font=30, command=self.selectChapter,
                          justify=CENTER, fg="black", bg="orange")
        self.chapterSelect.grid(row=2, column=2, rowspan=2, pady=100, ipadx=50)
        self.player = Player()

    def selectChapter(self):
        self.frame.destroy()
        self.frame = Frame(self.window, bg="black")
        self.frame.grid(row=0, column=0, padx=10, pady=10)
        self.label = Label(self.frame, text="Chapter Select:", justify=CENTER,
                            font=("Roman", 20), fg="orange", bg="black", width=95, wraplength=900)
        self.label.grid(row=0, column=0, columnspan=2, pady=50)
        self.chapterZero = Button(self.frame, image=self.img, text="Chapter 0", height=12, width=15, compound=CENTER, font=30,
                                 command=self.clickStartButton, justify=CENTER, fg="black", bg="orange")
        self.chapterZero.config(font="Roman 20 bold")
        self.chapterZero.grid(row=2, column=0, rowspan=2, pady=100, ipadx=100, ipady=100)
        self.chapterOne = Button(self.frame, image=self.chOnePhoto, text="Chapter 1", height=2, width=3, font=30, command=self.chapterOneSelect,
                          justify=CENTER, compound=CENTER, fg="black", bg="orange")
        self.chapterOne.config(font=("Roman 20 bold"))
        self.chapterOne.grid(row=2, column=1, rowspan=2, pady=100, ipadx=100, ipady=100)

    def chapterOneSelect(self):
        self.chapterNum = 1
        self.clickStartButton()


    def clickStartButton(self):
        self.frame.destroy()
        self.inventory_items = {"27": "Burnt Lasagna"}
        self.menu = Menu(self.window, tearoff=0, bg="white", fg="orange")

        self.status = ""
        self.inventory = Menu(self.menu)
        for i in self.inventory_items:
            self.inventory.add_command(label=self.inventory_items[str(i)])

        self.inventory.add_command(command=self.displayInventory)
        self.menu.add_cascade(label="Inventory", menu=self.inventory)
        self.menu.add_command(label="Help")
        self.menu.add_command(label="Quit", command=self.clickDieButton)

        self.window.config(menu=self.menu)
        self.start()

    def dead(self):
        self.frame.destroy()
        self.deadText = Label(self.window, text="DEAD", font=("Roman", 50, "bold"), fg="red", bg="black")
        self.deadText.pack()
        self.deadButton = Button(self.window, text="Quit?", command=exit)
        self.deadButton.pack()


    def start(self):
        self.did_inspect = 0
        self.window["bg"] = "black"
        self.frame = Frame(self.window, bg="black")
        self.frame.grid(row=0, column=0, padx=10, pady=10)

        self.player.update(self.file[str(self.chapterNum)]["Scenario1"]["hasStatus"])
        print(self.player.health)
        if self.player.health <= 0:
            self.dead()

        if self.file[str(self.chapterNum)]["Scenario1"]["Dec1"] != "":
            self.numButtons = 2
            self.option1 = Button(self.frame, text=self.file[str(self.chapterNum)]["Scenario1"]["Dec1"], height=3, width=5,
                                  wraplength=150, font=5, justify=CENTER, fg="black", bg="orange",
                                  command=lambda: self.options(self.file[str(self.chapterNum)]['Scenario1']['pointer1']))
            self.option1.grid(row=3, column=0, rowspan=2, pady=100, ipadx=50)

        if self.file[str(self.chapterNum)]["Scenario1"]["Dec2"] != "":
            self.numButtons = 3
            self.option2 = Button(self.frame, text=self.file[str(self.chapterNum)]["Scenario1"]["Dec2"], height=3, width=5,
                                  command=lambda: self.options(self.file[str(self.chapterNum)]['Scenario1']['pointer2']),
                                  justify=CENTER, wraplength=150, font=20, fg="black", bg="orange")
            self.option2.grid(row=3, column=1, rowspan=2, pady=100, ipadx=50)

        if self.file[str(self.chapterNum)]["Scenario1"]["Dec3"] != "":
            self.numButtons = 4
            self.option3 = Button(self.frame, text=self.file[str(self.chapterNum)]["Scenario1"]["Dec3"], height=3, width=5,
                                  command=lambda: self.options(self.file[str(self.chapterNum)]['Scenario1']['pointer3']),
                                  justify=CENTER, wraplength=150, font=20, fg="black", bg="orange")
            self.option3.grid(row=3, column=2, rowspan=2, pady=100, ipadx=50)

        self.inspect_scenario = Button(self.frame, text="Inspect", justify=CENTER, height=3, width=5, wraplength=150,
                                       command=lambda: self.inspect("Scenario1"), fg="black", bg="orange")
        self.inspect_scenario.config(font="Helvetica 15 underline bold")
        self.inspect_scenario.grid(row=3, column=(self.numButtons - 1), sticky="s", rowspan=2, pady=100, ipadx=50)
        self.displayHealth()
        self.dialog = Label(self.frame, text=self.file[str(self.chapterNum)]["Scenario1"]["Dialogue"], justify=CENTER,
                            font=("Roman", 20), fg="orange", bg="black", width=95, wraplength=900)
        self.dialog.grid(row=1, column=0, columnspan=self.numButtons, rowspan=2, pady=40, sticky="n")
        #self.dialog.grid_rowconfigure(1, weight=1)
        #if self.chapterNum >= 1:
        #    self.statusBar.destroy()
        #    self.healthBar.destroy()
        #self.displayHealth()


    def displayHealth(self):
        self.health = "Current Health: " + str(self.player.health)
        self.healthBar = Label(self.frame, text=self.health, justify=LEFT, font=("Roman", 15, "bold"), fg="red", bg="black")
        self.healthBar.grid(row=0, column=0,ipadx=40, padx=40)
        self.status = "Status Effects: "
        if self.player.currStatus == []:
            self.status += "None"
        else:
            for i in self.player.currStatus:
                self.status = self.status + str(i)
        self.statusBar = Label(self.frame, text=self.status, justify=LEFT, font=("Roman", 15, "bold"), fg="red", bg="black")
        #self.statusBar.config(text=self.status)
        self.statusBar.grid(row=0, column=self.numButtons-1)

    def updateHealth(self):
        self.health = "Current Health: " + str(self.player.health)
        self.healthBar.config(text=self.health)
        self.status = "Status Effects: "
        if self.player.currStatus == []:
            self.status += "None"
        else:
            for i in self.player.currStatus:
                self.status = self.status + str(i)
        self.statusBar.config(text=self.status)
        self.statusBar.grid(row=0, column=self.numButtons-1)



    '''def displayScenario(self, currentScenario, columnSpan):
        if self.numButtons >= 2:
            self.inspect_scenario.destroy()
            self.option1.destroy()

            if self.numButtons >= 3:
                self.option2.destroy()

                if self.numButtons == 4:
                    self.option3.destroy()

        #if self.file[str(self.chapterNum)][currentScenario]["Dec2"] != "":'''

    def options(self, currentScenario):
        self.player.update(self.file[str(self.chapterNum)][currentScenario]["hasStatus"])
        if self.file[str(self.chapterNum)][currentScenario]["takeDamage"] != "0":
            self.player.health -= int(self.file[str(self.chapterNum)][currentScenario]["takeDamage"])


        if self.player.health <= 0:
            self.dead()

        self.dialog.destroy()

        if self.did_inspect:
            self.go_back.destroy()
            self.did_inspect = False

        if self.numButtons >= 1:
            self.inspect_scenario.destroy()
            self.option1.destroy()

            if self.numButtons >= 3:
                self.option2.destroy()

                if self.numButtons == 4:
                    self.option3.destroy()

        if self.file[str(self.chapterNum)][currentScenario]["Dec1"] == "Quit":
            self.dialog = Label(self.frame, text=self.file[str(self.chapterNum)][currentScenario]["Dialogue"],
                                justify=CENTER, font=("Roman", 20), fg="orange", bg="black", width=95, wraplength=900)
            self.dialog.grid(row=1, column=0, columnspan=2, pady=75)

            self.option1 = Button(self.frame, text="Quit", command=self.clickDieButton, height=3, width=5, wraplength=150, font=15,
                                  fg="black", bg="orange")
            self.option1.grid(row=3, column=0, sticky="s", rowspan=2, pady=100, ipadx=50)

            if self.file[str(self.chapterNum)][currentScenario]["Dec2"] == "Go back to previous Scenario?":
                self.numButtons = 3
                self.option2 = Button(self.frame, text=self.file[str(self.chapterNum)][currentScenario]["Dec2"],
                                      height=3, width=5, wraplength=150, font=15, command=lambda: self.options(
                                          self.file[str(self.chapterNum)][currentScenario]['pointer2']), justify=CENTER,
                                      fg="black", bg="orange")
                self.option2.grid(row=3, column=1, rowspan=2, pady=100, ipadx=50)
            else:
                self.numButtons = 2
                self.chapterNum += 1

                self.option2 = Button(self.frame, text="Continue?", height=3, width=5, wraplength=150, font=15,
                                      command=self.clickStartButton, fg="black", bg="orange")
                self.option2.grid(row=3, column=1, rowspan=2, pady=100, ipadx=50)
        else:
            if self.file[str(self.chapterNum)][currentScenario]["Dec1"] != "":
                self.numButtons = 2

                self.option1 = Button(self.frame, text=self.file[str(self.chapterNum)][currentScenario]["Dec1"],
                                      height=3, width=5, wraplength=150, font=15,
                                      command=lambda: self.options(self.file[str(self.chapterNum)][currentScenario]['pointer1']),
                                      justify=CENTER, fg="black", bg="orange")
                self.option1.grid(row=3, column=0, sticky="s", rowspan=2, pady=100, ipadx=50)

            if self.file[str(self.chapterNum)][currentScenario]["Dec2"] != "":
                self.numButtons = 3

                self.option2 = Button(self.frame, text=self.file[str(self.chapterNum)][currentScenario]["Dec2"],
                                      height=3, width=5, wraplength=150, font=15, command=lambda: self.options(
                                          self.file[str(self.chapterNum)][currentScenario]['pointer2']), justify=CENTER,
                                      fg="black", bg="orange")
                self.option2.grid(row=3, column=1, rowspan=2, pady=100, ipadx=50)

            if self.file[str(self.chapterNum)][currentScenario]["Dec3"] != "":
                self.numButtons = 4

                self.option3 = Button(self.frame, text=self.file[str(self.chapterNum)][currentScenario]["Dec3"],
                                      height=3, width=5, wraplength=150, font=15, command=lambda: self.options(
                                          self.file[str(self.chapterNum)][currentScenario]['pointer3']), justify=CENTER,
                                      fg="black", bg="orange")
                self.option3.grid(row=3, column=2, rowspan=2, ipadx=50, pady=100)

            self.inspect_scenario = Button(self.frame, text="Inspect", justify=CENTER, fg="black", bg="orange",
                                           height=3, width=5, wraplength=150, font=15,command=lambda: self.inspect(currentScenario))
            self.inspect_scenario.config(font="Helvetica 15 underline bold")
            self.inspect_scenario.grid(row=3, column=(self.numButtons - 1), sticky="s", rowspan=2, pady=100, ipadx=50)
            self.dialog = Label(self.frame, text=self.file[str(self.chapterNum)][currentScenario]["Dialogue"],
                                justify=CENTER, font=("Roman", 20), fg="orange", bg="black", width=95, wraplength=900)
            self.dialog.grid(row=1, column=0, columnspan=self.numButtons, pady=75)
            self.updateHealth()

    def clickDieButton(self):
        exit()


    def inspect(self, currentScenario):
        self.did_inspect = True
        self.inspect_scenario.destroy()
        if self.numButtons >= 1:
            self.option1.destroy()

            if self.numButtons >= 3:
                self.option2.destroy()

                if self.numButtons == 4:
                    self.option3.destroy()

        self.dialog.destroy()
        self.numButtons = 1

        if self.file[str(self.chapterNum)][currentScenario]["inspect"]["Dec1"] != "":
            self.numButtons = 2
            self.option1 = Button(self.frame, text=self.file[str(self.chapterNum)][currentScenario]["inspect"]["Dec1"],
                                  fg="black", bg="orange",command=lambda: self.itemDescription(currentScenario,
                                  self.file[str(self.chapterNum)][currentScenario]["inspect"]["pointer1"]), height=3, width=5,
                                  font=15,
                                  justify=CENTER)
            self.option1.grid(row=2, column=0, sticky="s", rowspan=2, pady=100, ipadx=50)

        if self.file[str(self.chapterNum)][currentScenario]["inspect"]["Dec2"] != "":
            self.numButtons = 3

            self.option2 = Button(self.frame, text=self.file[str(self.chapterNum)][currentScenario]["inspect"]["Dec2"],
                                  command=lambda: self.itemDescription(currentScenario,
                                  self.file[str(self.chapterNum)][currentScenario]["inspect"]["pointer2"]), height=3, width=5,
                                  font=15,
                                  justify=CENTER, fg="black", bg="orange")
            self.option2.grid(row=2, column=1, rowspan=2, pady=100, ipadx=50)

        if self.file[str(self.chapterNum)][currentScenario]["inspect"]["Dec3"] != "":
            self.numButtons = 4
            self.option3 = Button(self.frame, text=self.file[str(self.chapterNum)][currentScenario]["inspect"]["Dec3"],
                                  command=lambda: self.itemDescription(currentScenario,
                                                                       self.file[str(self.chapterNum)][currentScenario][
                                                                           "inspect"]["pointer3"]), height=3, width=5,
                                  font=15,
                                  fg="black", bg="orange", justify=CENTER)
            self.option3.grid(row=2, column=2, rowspan=2, ipadx=50, pady=100)

        self.go_back = Button(self.frame, text="Go Back", justify=CENTER, command=lambda: self.options(currentScenario),
                              height=3, width=5, fg="black", bg="orange", font=15)
        self.go_back.grid(row=2, column=(self.numButtons - 1), sticky="s", rowspan=2, pady=100, ipadx=50)

        self.dialog = Label(self.frame, text=self.file[str(self.chapterNum)][currentScenario]["inspect"]["Description"],
                            justify=CENTER, font=("Roman", 20), fg="orange", bg="black", width=85, wraplength=500)
        self.dialog.grid(row=1, column=0, columnspan=self.numButtons, pady=75)
        self.updateHealth()

    def itemDescription(self, currentScenario, pointer):
        self.go_back.destroy()
        if self.numButtons >= 2:
            self.inspect_scenario.destroy()
            self.option1.destroy()
            if self.numButtons >= 3:
                self.option2.destroy()
                if self.numButtons == 4:
                    self.option3.destroy()
        self.dialog.destroy()
        self.numButtons = 2

        self.item = Label(self.frame, text=self.items["Items"][pointer]["Description"], justify=CENTER,
                          font=("Roman", 20), fg="orange", bg="black", width=85, wraplength=500)
        self.item.grid(row=1, column=0, columnspan=self.numButtons, pady=75)

        self.option1 = Button(self.frame, text="Pick up", command=lambda: self.addItem(currentScenario, pointer),
                              height=3, width=5, fg="black", bg="orange", font=15)
        self.option1.grid(row=2, column=0, pady=100, ipadx=50)

        self.option2 = Button(self.frame, text="Leave it", command=lambda: [self.option2.destroy(), self.inspect(currentScenario)],
                              height=3, width=5, fg="black", bg="orange", font=15)
        self.option2.grid(row=2, column=1, pady=100, ipadx=50)
        self.updateHealth()

    def addItem(self, currentScenario, pointer):
        self.option1.destroy()
        self.option2.destroy()
        self.numButtons = 0
        self.item.destroy()
        self.inventory_items[pointer] = self.items["Items"][pointer]["Name"]
        self.file[str(self.chapterNum)][currentScenario]["inspect"][pointer] = ""
        self.displayInventory(currentScenario, pointer)

    def displayInventory(self, currentScenario, pointer):
        self.inventory.add_command(label=self.items["Items"][pointer]["Name"], command=lambda: self.useItem(currentScenario, pointer))
        if self.player.health <= 0:
            self.dead()
        self.inspect(currentScenario)
        #for i in self.inventory_items:

    def useItem(self,currentScenario, pointer):
        self.useButton = Button(self.inventory, text="use item")
        self.player.useItem(self.inventory_items, pointer, self.items)
        self.useItemDialog(currentScenario, pointer)

    def useItemDialog(self, currentScenario, pointer):
        if self.did_inspect:
            self.go_back.destroy()
            self.did_inspect = False
        if self.numButtons >= 2:
            self.inspect_scenario.destroy()
            self.option1.destroy()
            if self.numButtons >= 3:
                self.option2.destroy()
                if self.numButtons == 4:
                    self.option3.destroy()
        self.dialog.destroy()
        self.numButtons = 2
        if pointer in self.file[str(self.chapterNum)][currentScenario]["usableItems"]:
            self.dialog = Label(self.frame, text=self.items["Items"][pointer]["useDialog"],
                                justify=CENTER, font=("Roman", 20), fg="orange", bg="black", width=85, wraplength=500)
            self.dialog.grid(row=1, column=0)
        else:
            self.dialog = Label(self.frame, text="You can't use this item here",
                                justify=CENTER, font=("Roman", 20), fg="orange", bg="black", width=85, wraplength=500)
            self.dialog.grid(row=1, column=0)
        self.continueScenario = Button(self.frame, text="Continue", command=lambda: self.addItem(currentScenario, pointer),
                              height=3, width=5, fg="black", bg="orange", font=15)
        self.continueScenario.grid(row=2, column=0)
        self.updateHealth()


window = Window(json_chapter, json_items, window=root)
root.mainloop()
