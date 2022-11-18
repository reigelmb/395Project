from tkinter import *
import json

# Import tkinter and json... Obviously

'''class Player:
    def __init__(self):
        self.health = 5.0
        self.movement = 10.0
        self.burn = False
        self.poison = False
        self.cut = False

    def update(self, status):
        //Updates movement
        if self.movement > 0:
            self.movement -=1
        //Updates poison/checks poison
        if self.poison == True:
            self.health -=.5
        elif status == "poison":
            self.poison = True
        //Updates burn/checks burn
        if self.burn == True:
            print("burned but no effect yet")
        elif status == "burn":
            self.burn = True
        //Updates cut/checks cut
        if self.cut == True:
            self.health -=.5
        elif status == "cut":
            self.cut == True
    def isAlive(self):
        return self.health > 0
    
    def checkItem(itemRequired, inventory):
        if itemRequired in inventory:
            return True
        else:
            return False
    

'''
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

        '''Set the number of chapters completed so far to 0 so that when the player
        '''
        self.chapterNum = 0
        self.title = Label(self.frame, text="Typical Monday", justify=CENTER, font=("Roman", 20), fg="orange",
                           bg="black", width=85, wraplength=500)
        self.title.grid(row=0, column=0, columnspan=2, pady=100)
        self.START = Button(self.frame, text="Start", command=self.clickStartButton, justify=CENTER)
        self.START.grid(row=2, column=0, rowspan=2, pady=100, ipadx=50)
        self.DIE = Button(self.frame, text="Quit", command=self.clickDieButton, justify=CENTER)
        self.DIE.grid(row=2, column=1, rowspan=2, pady=100, ipadx=50)
        self.image = PhotoImage(file="StartPhoto.png")

    def clickStartButton(self):
        self.frame.destroy()
        self.numButtons = 3
        self.inventory_items = {"27": "Burnt Lasagna"}
        self.menu = Menu(self.window, tearoff=0, bg="white", fg="orange")
        self.inventory = Menu(self.menu)
        for i in self.inventory_items:
            self.inventory.add_command(label=self.inventory_items[str(i)])
        self.menu.add_cascade(label="Inventory", menu=self.inventory)
        self.menu.add_command(label="Help")
        self.menu.add_command(label="Quit", command=self.clickDieButton)

        self.window.config(menu=self.menu)
        self.start()

    def start(self):

        self.window["bg"] = "black"
        self.frame = Frame(self.window, bg="black")
        self.frame.grid(row=0, column=0, padx=10, pady=10)
        self.numButtons = 1
        if self.file[str(self.chapterNum)]["Scenario1"]["Dec1"] != "":
            self.numButtons += 1

            if self.file[str(self.chapterNum)]["Scenario1"]["Dec2"] != "":
                self.numButtons += 1

                if self.file[str(self.chapterNum)]["Scenario1"]["Dec3"] != "":
                    self.numButtons += 1

        self.dialog = Label(self.frame, text=self.file[str(self.chapterNum)]["Scenario1"]["Dialogue"], justify=CENTER,
                            font=("Roman", 20), fg="orange", bg="black", width=85, wraplength=500)
        self.dialog.grid(row=0, column=0, columnspan=self.numButtons, rowspan=2, pady=40, sticky="n")
        self.dialog.grid_rowconfigure(0, weight=1)

        self.inspect_scenario = Button(self.frame, text="Inspect", justify=CENTER,
                                       command=lambda: self.inspect("Scenario1"))

        if self.file[str(self.chapterNum)]["Scenario1"]["Dec1"] != "":
            self.option1 = Button(self.frame, text=self.file[str(self.chapterNum)]["Scenario1"]["Dec1"],
                                  command=lambda: self.options(
                                      self.file[str(self.chapterNum)]['Scenario1']['pointer1']), width=10,
                                  justify=CENTER)
            self.option1.grid(row=2, column=0, sticky="s", rowspan=2, pady=100)
            self.inspect_scenario.grid(row=2, column=1, sticky="s", rowspan=2, pady=100, ipadx=50)

        if self.file[str(self.chapterNum)]["Scenario1"]["Dec2"] != "":
            self.option2 = Button(self.frame, text=self.file[str(self.chapterNum)]["Scenario1"]["Dec2"],
                                  command=lambda: self.options(
                                      self.file[str(self.chapterNum)]['Scenario1']['pointer2']), width=10,
                                  justify=CENTER)
            self.option2.grid(row=2, column=1, rowspan=2, pady=100, ipadx=50)
            self.inspect_scenario.grid(row=2, column=2, sticky="s", rowspan=2, pady=100, ipadx=50)

        if self.file[str(self.chapterNum)]["Scenario1"]["Dec3"] != "":
            self.option3 = Button(self.frame, text=self.file[str(self.chapterNum)]["Scenario1"]["Dec3"],
                                  command=lambda: self.options(
                                      self.file[str(self.chapterNum)]['Scenario1']['pointer3']), width=10,
                                  justify=CENTER)
            self.option3.grid(row=2, column=2, sticky="s", rowspan=2, pady=100)
            self.inspect_scenario.grid(row=2, column=3, sticky="s", rowspan=2, pady=100, ipadx=50)

    def options(self, currentScenario):
        self.dialog.destroy()

        if self.numButtons == 1:
            self.go_back.destroy()

        if self.numButtons >= 2:
            self.inspect_scenario.destroy()
            self.option1.destroy()

            if self.numButtons >= 3:
                self.option2.destroy()

                if self.numButtons == 4:
                    self.option3.destroy()

        if self.file[str(self.chapterNum)][currentScenario]["Dec1"] == "Quit":

            self.dialog = Label(self.frame, text=self.file[str(self.chapterNum)][currentScenario]["Dialogue"],
                                justify=CENTER,
                                font=("Roman", 20), fg="orange", bg="black", width=85, wraplength=500)
            self.dialog.grid(row=0, column=0, columnspan=2, pady=75)

            self.option1 = Button(self.frame, text="Quit", width=10, command=self.clickDieButton)
            self.option1.grid(row=2, column=0, sticky="s", rowspan=2, pady=100, ipadx=50)

            self.chapterNum += 1

            self.option2 = Button(self.frame, text="Continue?", width=10, command=self.clickStartButton)
            self.option2.grid(row=2, column=1, rowspan=2, pady=100, ipadx=50)

        elif self.file[str(self.chapterNum)][currentScenario]["Dec2"] == "":
            self.numButtons = 2
            self.dialog = Label(self.frame, text=self.file[str(self.chapterNum)][currentScenario]["Dialogue"],
                                justify=CENTER, font=("Roman", 20), fg="orange", bg="black", width=85, wraplength=500)
            self.dialog.grid(row=0, column=0, columnspan=self.numButtons, pady=75)

            self.option1 = Button(self.frame, text=self.file[str(self.chapterNum)][currentScenario]["Dec1"],
                                  command=lambda: self.options(
                                      self.file[str(self.chapterNum)][currentScenario]['pointer1']), justify=CENTER)
            self.option1.grid(row=2, column=0, sticky="s", rowspan=2, pady=100, ipadx=50)

            self.inspect_scenario = Button(self.frame, text="Inspect", justify=CENTER,
                                           command=lambda: self.inspect(
                                               self.file[str(self.chapterNum)][currentScenario]))
            self.inspect_scenario.grid(row=2, column=1, sticky="s", rowspan=2, pady=100, ipadx=50)

        elif self.file[str(self.chapterNum)][currentScenario]["Dec3"] == "":
            self.numButtons = 3
            self.dialog = Label(self.frame, text=self.file[str(self.chapterNum)][currentScenario]["Dialogue"],
                                justify=CENTER, font=("Roman", 20), fg="orange", bg="black", width=85, wraplength=500)
            self.dialog.grid(row=0, column=0, columnspan=self.numButtons, pady=75)

            self.option1 = Button(self.frame, text=self.file[str(self.chapterNum)][currentScenario]["Dec1"],
                                  command=lambda: self.options(
                                      self.file[str(self.chapterNum)][currentScenario]['pointer1']), justify=CENTER)
            self.option1.grid(row=2, column=0, sticky="s", rowspan=2, pady=100, ipadx=50)

            self.option2 = Button(self.frame, text=self.file[str(self.chapterNum)][currentScenario]["Dec2"],
                                  command=lambda: self.options(
                                      self.file[str(self.chapterNum)][currentScenario]['pointer2']), justify=CENTER)
            self.option2.grid(row=2, column=1, rowspan=2, pady=100, ipadx=50)

            self.inspect_scenario = Button(self.frame, text="Inspect", justify=CENTER,
                                           command=lambda: self.inspect(
                                               self.file[str(self.chapterNum)][currentScenario]))
            self.inspect_scenario.grid(row=2, column=2, sticky="s", rowspan=2, pady=100, ipadx=50)

        else:
            self.numButtons = 4
            self.dialog = Label(self.frame, text=self.file[str(self.chapterNum)][currentScenario]["Dialogue"],
                                justify=CENTER, font=("Roman", 20), fg="orange", bg="black", width=85, wraplength=500)
            self.dialog.grid(row=0, column=0, columnspan=self.numButtons, pady=75)

            self.option1 = Button(self.frame, text=self.file[str(self.chapterNum)][currentScenario]["Dec1"],
                                  command=lambda: self.options(
                                      self.file[str(self.chapterNum)][currentScenario]['pointer1']), justify=CENTER)
            self.option1.grid(row=2, column=0, sticky="s", rowspan=2, ipadx=50, pady=100)

            self.option2 = Button(self.frame, text=self.file[str(self.chapterNum)][currentScenario]["Dec2"],
                                  command=lambda: self.options(
                                      self.file[str(self.chapterNum)][currentScenario]['pointer2']), justify=CENTER)
            self.option2.grid(row=2, column=1, rowspan=2, ipadx=50, pady=100)

            self.option3 = Button(self.frame, text=self.file[str(self.chapterNum)][currentScenario]["Dec3"],
                                  command=lambda: self.options(
                                      self.file[str(self.chapterNum)][currentScenario]['pointer3']), justify=CENTER)
            self.option3.grid(row=2, column=2, rowspan=2, ipadx=50, pady=100)

            self.inspect_scenario = Button(self.frame, text="Inspect", justify=CENTER,
                                           command=lambda: self.inspect(
                                               self.file[str(self.chapterNum)][currentScenario]))
            self.inspect_scenario.grid(row=2, column=3, sticky="s", rowspan=2, pady=100, ipadx=50)

    def clickDieButton(self):
        exit()

    def inspect(self, currentScenario):
        self.inspect_scenario.destroy()
        if self.numButtons >= 2:
            self.inspect_scenario.destroy()
            self.option1.destroy()

            if self.numButtons >= 3:
                self.option2.destroy()

                if self.numButtons == 4:
                    self.option3.destroy()

        self.dialog.destroy()

        if self.file[str(self.chapterNum)][currentScenario]["inspect"]["Dec1"] == "":
            self.numButtons = 1
            self.dialog = Label(self.frame,
                                text=self.file[str(self.chapterNum)][currentScenario]["inspect"]["Description"],
                                justify=CENTER, font=("Roman", 20), fg="orange", bg="black", width=85, wraplength=500)
            self.dialog.grid(row=0, column=0, columnspan=self.numButtons, pady=75)

            self.go_back = Button(self.frame, text="Go Back", justify=CENTER,
                                  command=lambda: self.options(self.file[str(self.chapterNum)][currentScenario]))
            self.go_back.grid(row=2, column=0, sticky="s", rowspan=2, pady=100, ipadx=50)

        if self.file[str(self.chapterNum)][currentScenario]["inspect"]["Dec2"] == "":
            self.numButtons = 2
            self.dialog = Label(self.frame,
                                text=self.file[str(self.chapterNum)][currentScenario]["inspect"]["Description"],
                                justify=CENTER, font=("Roman", 20), fg="orange", bg="black", width=85, wraplength=500)
            self.dialog.grid(row=0, column=0, columnspan=self.numButtons, pady=75)

            self.option1 = Button(self.frame, text=self.file[str(self.chapterNum)][currentScenario]["inspect"]["Dec1"],
                                  command=lambda: self.options(
                                      self.file[str(self.chapterNum)][currentScenario]["inspect"]["Description"]),
                                  justify=CENTER)
            self.option1.grid(row=2, column=0, sticky="s", rowspan=2, pady=100, ipadx=50)

            self.go_back = Button(self.frame, text="Go Back", justify=CENTER,
                                  command=lambda: self.options(self.file[str(self.chapterNum)][currentScenario]))
            self.go_back.grid(row=2, column=1, sticky="s", rowspan=2, pady=100, ipadx=50)

        elif self.file[str(self.chapterNum)][currentScenario]["Dec3"] == "":
            self.numButtons = 3

            self.dialog = Label(self.frame,
                                text=self.file[str(self.chapterNum)][currentScenario]["inspect"]["Description"],
                                justify=CENTER, font=("Roman", 20), fg="orange", bg="black", width=85, wraplength=500)
            self.dialog.grid(row=0, column=0, columnspan=self.numButtons, pady=75)

            self.option1 = Button(self.frame, text=self.file[str(self.chapterNum)][currentScenario]["inspect"]["Dec1"],
                                  command=lambda: self.options(
                                      self.file[str(self.chapterNum)][currentScenario]['pointer1']), justify=CENTER)
            self.option1.grid(row=2, column=0, sticky="s", rowspan=2, pady=100, ipadx=50)

            self.option2 = Button(self.frame, text=self.file[str(self.chapterNum)][currentScenario]["inspect"]["Dec2"],
                                  command=lambda: self.options(
                                      self.file[str(self.chapterNum)][currentScenario]['pointer2']), justify=CENTER)
            self.option2.grid(row=2, column=1, rowspan=2, pady=100, ipadx=50)

            self.go_back = Button(self.frame, text="Go Back", justify=CENTER,
                                  command=lambda: self.inspect(self.file[str(self.chapterNum)][currentScenario]))
            self.go_back.grid(row=2, column=2, sticky="s", rowspan=2, pady=100, ipadx=50)

        else:
            self.numButtons = 4
            self.dialog = Label(self.frame,
                                text=self.file[str(self.chapterNum)][currentScenario]["inspect"]["Description"],
                                justify=CENTER, font=("Roman", 20), fg="orange", bg="black", width=85, wraplength=500)
            self.dialog.grid(row=0, column=0, columnspan=self.numButtons, pady=75)
            self.option1 = Button(self.frame, text=self.file[str(self.chapterNum)][currentScenario]["inspect"]["Dec1"],
                                  command=lambda: self.options(
                                      self.file[str(self.chapterNum)][currentScenario]['pointer1']), justify=CENTER)
            self.option1.grid(row=2, column=0, sticky="s", rowspan=2, ipadx=50, pady=100)

            self.option2 = Button(self.frame, text=self.file[str(self.chapterNum)][currentScenario]["inspect"]["Dec2"],
                                  command=lambda: self.options(
                                      self.file[str(self.chapterNum)][currentScenario]['pointer2']), justify=CENTER)
            self.option2.grid(row=2, column=1, rowspan=2, ipadx=50, pady=100)

            self.option3 = Button(self.frame, text=self.file[str(self.chapterNum)][currentScenario]["inspect"]["Dec3"],
                                  command=lambda: self.options(
                                      self.file[str(self.chapterNum)][currentScenario]['pointer3']), justify=CENTER)
            self.option3.grid(row=2, column=2, rowspan=2, ipadx=50, pady=100)
            self.go_back = Button(self.frame, text="Go Back", justify=CENTER,
                                  command=lambda: self.inspect(self.file[str(self.chapterNum)][currentScenario]))
            self.go_back.grid(row=2, column=3, sticky="s", rowspan=2, pady=100, ipadx=50)

    def itemDescription(self, currentScenario, pointer):
        if self.numButtons >= 2:
            self.inspect_scenario.destroy()
            self.option1.destroy()
            if self.numButtons >= 3:
                self.option2.destroy()
                if self.numButtons == 4:
                    self.option3.destroy()
        self.dialog.destroy()

    '''def inventory(self):
        self.inventory_window = Toplevel(self.window)
        self.inventory_items = {}
        self.inventory_window.geometry("200x400")
        self.menu.add(OptionMenu, )
        self.inventory_window['bg'] = "gray"
        self.title = Label(self.inventory_window, text="Inventory", justify=CENTER, font=("Roman", 20), fg="orange",
                           bg="gray", width=15, wraplength=200)
        self.title.grid(row=0, column=0)'''


window = Window(json_chapter, json_items, window=root)
root.mainloop()
