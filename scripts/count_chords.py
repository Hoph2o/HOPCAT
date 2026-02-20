from __future__ import absolute_import
from reaper_python import *
import C3toolbox
import sys
import os
sys.argv=["Main"]
import tkinter

global level_var
global form

CAT_LABEL = "Count Chords"
CAT_CATEGORY = "Uhhh"
CAT_ORDER = 1

def execute(selected):
    global level_var
    global form
    level = str(level_var.get())

    C3toolbox.startup()
    C3toolbox.single_pedal(C3toolbox.array_levels[level][0], 20, selected)
    #instrument, level, fix, selected
    window.close()
    form.destroy()

def launch():
    global level_var
    global form
    
    C3toolbox.startup()
    form = tkinter.Tk()
    form.wm_title('Reduce double pedal kicks to single pedal kicks')
    
    helpLf = tkinter.Frame(form)
    helpLf.grid(row=0, column=1, sticky='NS', padx=5, pady=5)

    OPTIONS = ["Expert", "Hard", "Medium", "Easy"]

    level_var = tkinter.StringVar(helpLf)
    level_var.set(OPTIONS[0]) # default value

    levelOpt = tkinter.OptionMenu(helpLf, level_var, *OPTIONS)
    levelOpt.grid(row=0, column=1, columnspan=1, sticky="WE", pady=3)

    allBtn = tkinter.Button(helpLf, text="Reduce all", command= lambda: execute(0)) 
    allBtn.grid(row=0, column=2, rowspan=1, sticky="WE", padx=5, pady=2)

    selBtn = tkinter.Button(helpLf, text="Reduce selected", command= lambda: execute(1)) 
    selBtn.grid(row=0, column=3, rowspan=1, sticky="WE", padx=5, pady=2)

    logo = tkinter.Frame(form, bg="#000")
    logo.grid(row=1, column=0, columnspan=10, sticky='WE', \
                 padx=0, pady=0, ipadx=0, ipady=0)

    path = os.path.join( sys.path[0], "banner.gif" )
    img = tkinter.PhotoImage(file=path)
    imageLbl = tkinter.Label(logo, image = img, borderwidth=0)
    imageLbl.grid(row=0, column=0, rowspan=2, sticky='E', padx=0, pady=0)

    # Open window center screen
    imageLbl.image = img
    C3toolbox.center_on_screen(form)
    

if __name__ == '__main__':
    #launch()
    C3toolbox.startup()
    C3toolbox.reduce_chords('PART GUITAR', 'x', 0)
