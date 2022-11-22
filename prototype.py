from tkinter import *
import json

# Import tkinter and json... Obviously

class Player:
    def __init__(self):
        self.health = 5.0
        self.movement = 10.0
        self.burn = False
        self.poison = False
        self.cut = False

    def update(self, status):
        #Updates movement
        if self.movement > 0:
            self.movement-=1
        #Updates poison/checks poison
        if self.poison == True:
            self.health -=.5
        elif status == "poison":
            self.poison = True
        #Updates burn/checks burn
        if self.burn == True:
            self.health -= .5
            print(self.health)
            print("burned but no effect yet")
        elif status == "burn":
            self.burn = True
        #Updates cut/checks cut
        if self.cut == True:
            self.health -=.5
        elif status == "cut":
            self.cut = True
    def isAlive(self):
        return self.health > 0

    def checkItem(itemRequired, inventory):
        if itemRequired in inventory:
            return True
        else:
            return False



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

        '''
        Set self.title to a label. Make that labels parent self.frame, Set the text to "Typical monday and make
        sure it is properly aligned in the center.
        '''
        self.title = Label(self.frame, text="Typical Monday", justify=CENTER, font=("Roman", 20), fg="orange",
                           bg="black", width=85, wraplength=500)
        '''In the grid, set self.title to row 0 and column 0. Have it span 2 columns'''
        self.title.grid(row=0, column=0, columnspan=2, pady=100)

        '''Create self.START variable which will be a button whose parent is self.frame. Make the text for it 
        "Start" and make it call the clickStartButton function when pressed make sure it is aligned
        to the center'''
        self.START = Button(self.frame, text="Start", command=self.clickStartButton, justify=CENTER)

        '''Align the self.START button to be in row 2  and column 0 of the grid and have it span
        2 rows'''
        self.START.grid(row=2, column=0, rowspan=2, pady=100, ipadx=50)

        '''Create self.DIE button g'''
        self.DIE = Button(self.frame, text="Quit", command=self.clickDieButton, justify=CENTER)
        self.DIE.grid(row=2, column=1, rowspan=2, pady=100, ipadx=50)
        # self.image = PhotoImage(file="StartPhoto.png")
        self.player = Player()

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

    def start(self):
        self.did_inspect = 0
        self.window["bg"] = "black"
        self.frame = Frame(self.window, bg="black")
        self.frame.grid(row=0, column=0, padx=10, pady=10)

        self.player.update(self.status)

        if self.file[str(self.chapterNum)]["Scenario1"]["Dec1"] != "":
            self.numButtons = 2
            self.option1 = Button(self.frame, text=self.file[str(self.chapterNum)]["Scenario1"]["Dec1"],
                                  command=lambda: self.options(self.file[str(self.chapterNum)]['Scenario1']['pointer1']),
                                  justify=CENTER)
            self.option1.grid(row=2, column=0, sticky="s", rowspan=2, pady=100)

        if self.file[str(self.chapterNum)]["Scenario1"]["Dec2"] != "":
            self.numButtons = 3
            self.option2 = Button(self.frame, text=self.file[str(self.chapterNum)]["Scenario1"]["Dec2"],
                                  command=lambda: self.options(self.file[str(self.chapterNum)]['Scenario1']['pointer2']),
                                  justify=CENTER)
            self.option2.grid(row=2, column=1, rowspan=2, pady=100, ipadx=50)

        if self.file[str(self.chapterNum)]["Scenario1"]["Dec3"] != "":
            self.numButtons = 4
            self.option3 = Button(self.frame, text=self.file[str(self.chapterNum)]["Scenario1"]["Dec3"],
                                  command=lambda: self.options(self.file[str(self.chapterNum)]['Scenario1']['pointer3']),
                                  justify=CENTER)
            self.option3.grid(row=2, column=2, sticky="s", rowspan=2, pady=100)

        self.inspect_scenario = Button(self.frame, text="Inspect", justify=CENTER, command=lambda: self.inspect("Scenario1"))
        self.inspect_scenario.grid(row=2, column=(self.numButtons-1), sticky="s", rowspan=2, pady=100, ipadx=50)

        self.dialog = Label(self.frame, text=self.file[str(self.chapterNum)]["Scenario1"]["Dialogue"], justify=CENTER,
                            font=("Roman", 20), fg="orange", bg="black", width=85, wraplength=500)
        self.dialog.grid(row=0, column=0, columnspan=self.numButtons, rowspan=2, pady=40, sticky="n")
        self.dialog.grid_rowconfigure(0, weight=1)

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
        if self.did_inspect:
            self.go_back.destroy()
            self.did_inspect = False

        self.dialog.destroy()

        if self.file[str(self.chapterNum)][currentScenario]["takeDamage"] != "0":
            self.status = self.file[str(self.chapterNum)][currentScenario]["takeDamage"]
            self.player.update(self.status)
            print("You got burned :(")

        if self.numButtons >= 1:
            self.inspect_scenario.destroy()
            self.option1.destroy()

            if self.numButtons >= 3:
                self.option2.destroy()

                if self.numButtons == 4:
                    self.option3.destroy()


        if self.file[str(self.chapterNum)][currentScenario]["Dec1"] == "Quit":
            self.dialog = Label(self.frame, text=self.file[str(self.chapterNum)][currentScenario]["Dialogue"],
                                justify=CENTER, font=("Roman", 20), fg="orange", bg="black", width=85, wraplength=500)
            self.dialog.grid(row=0, column=0, columnspan=2, pady=75)

            self.option1 = Button(self.frame, text="Quit", command=self.clickDieButton)
            self.option1.grid(row=2, column=0, sticky="s", rowspan=2, pady=100, ipadx=50)

            if self.file[str(self.chapterNum)][currentScenario]["Dec2"] == "Go back to previous Scenario?":
                self.option2 = Button(self.frame, text=self.file[str(self.chapterNum)][currentScenario]["Dec2"],
                                      command=lambda: self.options(self.file[str(self.chapterNum)][currentScenario]['pointer2']), justify=CENTER)
                self.option2.grid(row=2, column=1, rowspan=2, pady=100, ipadx=50)
            else:
                self.chapterNum += 1

                self.option2 = Button(self.frame, text="Continue?", command=self.clickStartButton)
                self.option2.grid(row=2, column=1, rowspan=2, pady=100, ipadx=50)
        else:
            if self.file[str(self.chapterNum)][currentScenario]["Dec1"] != "":
                self.numButtons = 2

                self.option1 = Button(self.frame, text=self.file[str(self.chapterNum)][currentScenario]["Dec1"],
                                      command=lambda: self.options(self.file[str(self.chapterNum)][currentScenario]['pointer1']), justify=CENTER)
                self.option1.grid(row=2, column=0, sticky="s", rowspan=2, pady=100, ipadx=50)

            if self.file[str(self.chapterNum)][currentScenario]["Dec2"] != "":
                self.numButtons = 3

                self.option2 = Button(self.frame, text=self.file[str(self.chapterNum)][currentScenario]["Dec2"],
                                  command=lambda: self.options(
                                      self.file[str(self.chapterNum)][currentScenario]['pointer2']), justify=CENTER)
                self.option2.grid(row=2, column=1, rowspan=2, pady=100, ipadx=50)

            if self.file[str(self.chapterNum)][currentScenario]["Dec3"] != "":
                self.numButtons = 4

                self.option3 = Button(self.frame, text=self.file[str(self.chapterNum)][currentScenario]["Dec3"],
                                      command=lambda: self.options(self.file[str(self.chapterNum)][currentScenario]['pointer3']), justify=CENTER)
                self.option3.grid(row=2, column=2, rowspan=2, ipadx=50, pady=100)

            self.inspect_scenario = Button(self.frame, text="Inspect", justify=CENTER,
                                           command=lambda: self.inspect(currentScenario))
            self.inspect_scenario.grid(row=2, column=(self.numButtons-1), sticky="s", rowspan=2, pady=100, ipadx=50)

            self.dialog = Label(self.frame, text=self.file[str(self.chapterNum)][currentScenario]["Dialogue"],
                                justify=CENTER, font=("Roman", 20), fg="orange", bg="black", width=85, wraplength=500)
            self.dialog.grid(row=0, column=0, columnspan=self.numButtons, pady=75)




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
                                  command=lambda: self.itemDescription(currentScenario, self.file[str(self.chapterNum)][currentScenario]["inspect"]["pointer1"]),
                                    justify=CENTER)
            self.option1.grid(row=2, column=0, sticky="s", rowspan=2, pady=100, ipadx=50)

        if self.file[str(self.chapterNum)][currentScenario]["inspect"]["Dec2"] != "":
            self.numButtons = 3

            self.option2 = Button(self.frame, text=self.file[str(self.chapterNum)][currentScenario]["inspect"]["Dec2"],
                              command=lambda: self.itemDescription(currentScenario, self.file[str(self.chapterNum)][currentScenario]["inspect"]["pointer2"]), justify=CENTER)
            self.option2.grid(row=2, column=1, rowspan=2, pady=100, ipadx=50)

        if self.file[str(self.chapterNum)][currentScenario]["inspect"]["Dec3"] != "":
            self.numButtons = 4
            self.option3 = Button(self.frame, text=self.file[str(self.chapterNum)][currentScenario]["inspect"]["Dec3"],
                                  command=lambda: self.itemDescription(currentScenario, self.file[str(self.chapterNum)][currentScenario]["inspect"]["pointer3"]), justify=CENTER)
            self.option3.grid(row=2, column=2, rowspan=2, ipadx=50, pady=100)


        self.go_back = Button(self.frame, text="Go Back", justify=CENTER, command=lambda: self.options(currentScenario))
        self.go_back.grid(row=2, column=(self.numButtons-1), sticky="s", rowspan=2, pady=100, ipadx=50)

        self.dialog = Label(self.frame, text=self.file[str(self.chapterNum)][currentScenario]["inspect"]["Description"],
                    justify=CENTER, font=("Roman", 20), fg="orange", bg="black", width=85, wraplength=500)
        self.dialog.grid(row=0, column=0, columnspan=self.numButtons, pady=75)

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
        self.item.grid(row=0, column=0, columnspan=self.numButtons, pady=75)

        self.option1 = Button(self.frame, text="Pick up", command=lambda: self.addItem(currentScenario, pointer))
        self.option1.grid(row=2, column=0, pady=75)

        self.option2 = Button(self.frame, text="Leave it", command=lambda: [self.option2.destroy(), self.inspect(currentScenario)])
        self.option2.grid(row=2, column=1, pady=75)

    def addItem(self, currentScenario, pointer):
        self.option1.destroy()
        self.option2.destroy()
        self.numButtons = 0
        self.item.destroy()
        self.inventory_items[self.items["Items"][pointer]["Name"]] = self.items["Items"][pointer]["Type"]
        self.file[str(self.chapterNum)][currentScenario]["inspect"][pointer] = ""
        self.displayInventory(currentScenario, pointer)

    def displayInventory(self, currentScenario, pointer):
        self.inventory.add_command(label=self.items["Items"][pointer]["Name"])
        self.inspect(currentScenario)


window = Window(json_chapter, json_items, window=root)
root.mainloop()
