from __future__ import absolute_import
from reaper_python import *
import C3toolbox
import sys
import os
sys.argv=["Main"]
import tkinter

global level_var
global instrument_var
global what_var
global form

CAT_LABEL = "Leave single snare hits"
CAT_CATEGORY = "5-Lane / Drums"
CAT_ORDER = 1

def execute(selected):
    global level_var
    global instrument_var
    global what_var
    global form
    what_array = { 'Any note' : 'a', 'Kick' : 's', 'Any tom' : 't', 'Any cymbal' : 'c' }
    level = str(level_var.get())
    instrument = str(instrument_var.get())
    instrument = C3toolbox.array_instruments[instrument]
    what = str(what_var.get())
    what = what_array[what]

    if instrument == "PART REAL_KEYS":
        instrument = instrument + C3toolbox.array_levels[level][1]
    C3toolbox.startup()
    C3toolbox.single_snare(instrument, C3toolbox.array_levels[level][0], what, selected)
    #instrument, level, fix, selected
    form.destroy()

def launch():
    global level_var
    global instrument_var
    global what_var
    global form
    
    C3toolbox.startup()
    form = tkinter.Tk()
    form.wm_title('Leave only snare')
    
    helpLf = tkinter.Frame(form)
    helpLf.grid(row=0, column=1, sticky='NS', padx=5, pady=5)

    inFileLbl = tkinter.Label(helpLf, text="Select instrument")
    inFileLbl.grid(row=1, column=1, sticky='E', padx=5, pady=2)

    OPTIONS = ["Drums", "2x Drums"]

    instrument_var = tkinter.StringVar(helpLf)
    instrument_var.set(OPTIONS[0]) # default value

    instrumentOpt = tkinter.OptionMenu(helpLf, instrument_var, *OPTIONS)
    instrumentOpt.grid(row=0, column=1, columnspan=1, sticky="WE", pady=3)

    levelLbl = tkinter.Label(helpLf, text="Select level")
    levelLbl.grid(row=1, column=2, sticky='E', padx=5, pady=2)

    OPTIONS = ["Expert", "Hard", "Medium", "Easy"]

    level_var = tkinter.StringVar(helpLf)
    level_var.set(OPTIONS[0]) # default value

    levelOpt = tkinter.OptionMenu(helpLf, level_var, *OPTIONS)
    levelOpt.grid(row=0, column=2, columnspan=1, sticky="WE", pady=3)

    whatLbl = tkinter.Label(helpLf, text="Leave only a snare when paired with...")
    whatLbl.grid(row=1, column=3, sticky='E', padx=5, pady=2)

    OPTIONS = ["Any note", "Kick", "Any tom", "Any cymbal"]

    what_var = tkinter.StringVar(helpLf)
    what_var.set(OPTIONS[0]) # default value

    whatOpt = tkinter.OptionMenu(helpLf, what_var, *OPTIONS)
    whatOpt.grid(row=0, column=3, columnspan=1, sticky="WE", pady=3) 

    allBtn = tkinter.Button(helpLf, text="Simplify snare hits", command= lambda: execute(0)) 
    allBtn.grid(row=0, column=4, rowspan=1, sticky="WE", padx=5, pady=2)

    selBtn = tkinter.Button(helpLf, text="Simplify selected snares hits", command= lambda: execute(1)) 
    selBtn.grid(row=1, column=4, rowspan=1, sticky="WE", padx=5, pady=2)

    logo = tkinter.Frame(form, bg="#000")
    logo.grid(row=2, column=0, columnspan=10, sticky='WE', \
                 padx=0, pady=0, ipadx=0, ipady=0)

    path = os.path.join( sys.path[0], "banner.gif" )
    img = tkinter.PhotoImage(file=path)
    imageLbl = tkinter.Label(logo, image = img, borderwidth=0)
    imageLbl.grid(row=0, column=0, rowspan=2, sticky='E', padx=0, pady=0)

    # Open window center screen
    form.grab_release()
    imageLbl.image = img
    C3toolbox.center_on_screen(form)
    
    form.quit()
    
if __name__ == '__main__':
    launch()
    #C3toolbox.startup()
    #C3toolbox.single_snare('PART DRUMS', 'e', 'c', 0)
