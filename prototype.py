from tkinter import *
import json
#Import tkinter and json... Obviously

root = Tk()
#Set variable root to tk()
root.geometry('900x900')
#Set the geometry of the root variable to 900x900
with open('chapter1.json', 'r', encoding='utf-8') as f:
    #Open json file and put store that into variable "json_object"
    json_object = json.load(f)


class Window(Frame):
    #Initialize Window class be where most of the game is created

    def __init__(self, file, window=None):
        Frame.__init__(self, window)
        self.window = window
        self.window['bg'] = "black"
        self.window.attributes('-fullscreen', True)
        self.file = file
        self.frame = Frame(self.window, bg="black")
        self.frame.grid(row=0, column=0, padx=10, pady=10)
        self.title = Label(self.frame, text="Typical Monday", justify=CENTER, font=("Roman", 20), fg="orange", bg="black", width=85, wraplength=500)
        self.title.grid(row=0, column=0, columnspan=2, pady=100)
        self.START = Button(self.frame, text="Start", command=self.clickStartButton, justify=CENTER)
        self.START.grid(row=2, column=0, rowspan=2, pady=100, ipadx=50)
        self.DIE = Button(self.frame, text="Quit", command=self.clickDieButton, justify=CENTER)
        self.DIE.grid(row=2, column=1, rowspan=2, pady=100, ipadx=50)

    def clickStartButton(self):
        '''self.dialog.destroy()
        self.DIE.destroy()
        self.START.destroy()'''
        self.frame.destroy()
        self.start()

    def start(self):
        self.numButtons = 2
        self.window["bg"] = "black"
        self.frame = Frame(self.window, bg="black")
        self.frame.grid(row=1, column=1, padx=10, pady=10)
        self.dialog = Label(self.frame, text=self.file["Scenario"]["Scenario1"]["Dialogue"], justify=CENTER, font="Roman", fg="orange", bg="black", width=100, wraplength=700)
        self.dialog.grid(row=0, column=0, columnspan=3, rowspan=2, pady=40, sticky="n")
        self.dialog.grid_rowconfigure(0, weight=1)
        if self.file["Scenario"]["Scenario1"]["Dec1"] != "":
            self.option1 = Button(self.frame, text=self.file["Scenario"]["Scenario1"]["Dec1"], command=lambda: self.buttons(self.file['Scenario']['Scenario1']['pointer1']), justify=CENTER)
            self.option1.grid(row=3, column=0, sticky="s", rowspan=2, pady=100)
            #self.option1.pack()
        if self.file["Scenario"]["Scenario1"]["Dec2"] != "":
            self.option2 = Button(self.frame, text=self.file["Scenario"]["Scenario1"]["Dec2"], command=lambda: self.buttons(self.file['Scenario']['Scenario1']['pointer2']), justify=CENTER)
            self.option2.grid(row=3, column=1, sticky="s", rowspan=2, pady=100)
            #self.option2.pack()
        if self.file["Scenario"]["Scenario1"]["Dec3"] != "":
            self.option3 = Button(self.window, text=self.file["Scenario"]["Scenario1"]["Dec3"], command=lambda: self.buttons(self.file['Scenario']['Scenario1']['pointer3']), justify=CENTER)
            self.option3.grid(row=3, column=2, sticky="s", rowspan=2, pady=100)
        self.menu = Menu(self.window, tearoff=0, bg="white", fg="orange")
        self.menu.add_command(label="Quit", command=self.clickDieButton)
        self.menu.add_command(label="Inventory")
        self.menu.add_command(label="Help")
        self.window.config(menu=self.menu)


    def buttons(self, currentScenario):
        self.dialog.destroy()
        self.dialog = Label(self.frame, text=self.file["Scenario"][currentScenario]["Dialogue"], justify=CENTER, font="Roman", fg="orange", bg="black", width=100, wraplength=700)
        self.dialog.grid(row=0, column=0, columnspan=3, rowspan=2, pady=5)
        self.dialog.grid_rowconfigure(0, weight=1)
        if self.numButtons >= 1:
            self.option1.destroy()
            if self.numButtons >= 2:
                self.option2.destroy()
                if self.numButtons == 3:
                    self.option3.destroy()

        if self.file["Scenario"][currentScenario]["Dec1"] == "":
            '''self.option1.destroy()
            self.option1 = Button(self.window, text=self.file["Scenario"][currentScenario]["Dec1"],
                              command=lambda: self.buttons(self.file['Scenario'][currentScenario]['pointer1']))
            self.option1.pack()
            self.total += 1'''
            if self.numButtons >= 1:
                self.option1.destroy()
                if self.numButtons >= 2:
                    self.option2.destroy()
                    if self.numButtons == 3:
                        self.option3.destroy()
            self.DIE = Button(self.frame, text="Die", width=10, command=self.clickDieButton)
            self.DIE.grid(row=3, column=1, sticky="S", rowspan=2, pady=100)

        elif self.file["Scenario"][currentScenario]["Dec2"] == "":
            self.option1 = Button(self.frame, text=self.file["Scenario"][currentScenario]["Dec1"],
                              command=lambda: self.buttons(self.file['Scenario'][currentScenario]['pointer1']))
            self.option1.grid(row=3, column=0, sticky="S", rowspan=2, pady=100)
            #self.option1.pack()
            self.numButtons = 1

        elif self.file["Scenario"][currentScenario]["Dec3"] == "":
            self.option1 = Button(self.frame, text=self.file["Scenario"][currentScenario]["Dec1"],
                              command=lambda: self.buttons(self.file['Scenario'][currentScenario]['pointer1']))
            self.option1.grid(row=3, column=0, sticky="S", rowspan=2, pady=100)
            #self.option1.pack()
            self.option2 = Button(self.frame, text=self.file["Scenario"][currentScenario]["Dec2"],
                              command=lambda: self.buttons(self.file['Scenario'][currentScenario]['pointer2']))
            self.option2.grid(row=3, column=1, sticky="S", rowspan=2, pady=100)
            #self.option2.pack()
            self.numButtons = 2

        else:
            self.option1 = Button(self.frame, text=self.file["Scenario"][currentScenario]["Dec1"],
                              command=lambda: self.buttons(self.file['Scenario'][currentScenario]['pointer1']), justify=CENTER)
            self.option1.grid(row=3, column=0, sticky="S", rowspan=2, pady=100)
            #self.option1.pack()
            self.option2 = Button(self.frame, text=self.file["Scenario"][currentScenario]["Dec2"],
                              command=lambda: self.buttons(self.file['Scenario'][currentScenario]['pointer2']), justify=CENTER)
            #self.option2.pack()
            self.option2.grid(row=3, column=1, sticky="S", rowspan=2, pady=100)
            self.option3 = Button(self.frame, text=self.file["Scenario"][currentScenario]["Dec3"],
                              command=lambda: self.buttons(self.file['Scenario'][currentScenario]['pointer3']), justify=CENTER)
            self.option3.grid(row=3, column=2, sticky="S", rowspan=2, pady=100)

            #self.option3.pack()
            self.numButtons = 3




    def clickDieButton(self):
        exit()


window = Window(json_object, window=root)
root.mainloop()
