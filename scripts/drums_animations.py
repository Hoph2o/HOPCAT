from __future__ import absolute_import
from reaper_python import *
import C3toolbox
import os
import sys
sys.argv=["Main"]
import tkinter

global level_var
global instrument_var
global crashChkvar
global softChkvar
global flamChkvar
global ghostChkvar
global tolerance
global form

CAT_LABEL = "Create drums animations"
CAT_CATEGORY = "System & Supersets"
CAT_ORDER = 1

def execute(a):

    global level_var
    global instrument_var
    global crashChkvar
    global softChkvar
    global flamChkvar
    global ghostChkvar
    global tolerance
    global form
    
    C3toolbox.startup()
    #C3toolbox.drums_animations('PART DRUMS', 0, 0, 0, 'e', 4, 10)
    level = str(level_var.get())
    grid_array = { '1/16' : 'e', '1/32' : 's' }
    grid = grid_array[level]
    instrument = str(instrument_var.get())
    instrument = C3toolbox.array_instruments[instrument]
    crash = crashChkvar.get()
    soft = softChkvar.get()
    flam = flamChkvar.get()
    ghost = ghostChkvar.get()
    tolerance = tolerance.get()
    C3toolbox.drums_animations(instrument, int(crash), int(soft), int(flam), int(ghost), grid, int(tolerance), 20, 0)
    form.destroy()

def launch():
    
    global level_var
    global instrument_var
    global crashChkvar
    global softChkvar
    global flamChkvar
    global ghostChkvar
    global tolerance
    global form
    form = tkinter.Tk()
    form.wm_title('Automatic drums animations')
    
    helpLf = tkinter.Frame(form)
    helpLf.grid(row=0, column=1, sticky='NS', padx=5, pady=5)

    inFileLbl = tkinter.Label(helpLf, text="Select instrument")
    inFileLbl.grid(row=0, column=1, sticky='E', padx=5, pady=2)

    OPTIONS = ["Drums", "2x Drums"]

    instrument_var = tkinter.StringVar(helpLf)
    instrument_var.set(OPTIONS[0]) # default value

    instrumentOpt = tkinter.OptionMenu(helpLf, instrument_var, *OPTIONS)
    instrumentOpt.grid(row=1, column=1, columnspan=1, sticky="WE", pady=3)

    levelLbl = tkinter.Label(helpLf, text="Select grid")
    levelLbl.grid(row=2, column=1, sticky='WE', padx=5, pady=2)

    OPTIONS = ["1/16", "1/32"]

    level_var = tkinter.StringVar(helpLf)
    level_var.set(OPTIONS[0]) # default value

    levelOpt = tkinter.OptionMenu(helpLf, level_var, *OPTIONS)
    levelOpt.grid(row=3, column=1, columnspan=1, sticky="WE", pady=3) 

    crashChkvar = tkinter.IntVar(helpLf)
    crashChk = tkinter.Checkbutton(helpLf, \
               text="CRASH1 as default crash", onvalue=1, offvalue=0, variable=crashChkvar)
    crashChk.grid(row=0, column=2, sticky='W', padx=5, pady=2)

    softChkvar = tkinter.IntVar(helpLf)
    softChk = tkinter.Checkbutton(helpLf, \
               text="Soft as default for snare/crash", onvalue=1, offvalue=0, variable=softChkvar)
    softChk.grid(row=1, column=2, sticky='W', padx=5, pady=2)

    toleranceLbl = tkinter.Label(helpLf, \
                           text="Min. cymbals hits:")
    toleranceLbl.grid(row=2, column=2, padx=5, pady=2, sticky='W')

    tolerance = tkinter.Entry(helpLf)
    tolerance.insert(0, "4")
    tolerance.config(width=5)
    tolerance.grid(row=3, column=2, padx=5, pady=2, sticky='W')

    flamChkvar = tkinter.IntVar(helpLf)
    flamChk = tkinter.Checkbutton(helpLf, \
               text="Make snare+Y toms flams", onvalue=1, offvalue=0, variable=flamChkvar)
    flamChk.grid(row=0, column=3, sticky='W', padx=5, pady=2)
    flamChk.select()

    ghostChkvar = tkinter.IntVar(helpLf)
    ghostChk = tkinter.Checkbutton(helpLf, \
               text="Make vel. 1 snare soft hits", onvalue=1, offvalue=0, variable=ghostChkvar)
    ghostChk.grid(row=1, column=3, sticky='W', padx=5, pady=2)
    ghostChk.select()
    
    allBtn = tkinter.Button(helpLf, text="Create animations", command= lambda: execute(0)) 
    allBtn.grid(row=2, column=3, rowspan=1, sticky="WE", padx=5, pady=2)

    logo = tkinter.Frame(form, bg="#000")
    logo.grid(row=4, column=0, columnspan=3, sticky='WE', \
                 padx=0, pady=0, ipadx=0, ipady=0)

    path = os.path.join( sys.path[0], "banner.gif" )
    img = tkinter.PhotoImage(file=path)
    imageLbl = tkinter.Label(logo, image = img, borderwidth=0)
    imageLbl.grid(row=0, column=0, rowspan=2, sticky='E', padx=0, pady=0)

    # Open window center screen
    imageLbl.image = img
    C3toolbox.center_on_screen(form)
    

if __name__ == '__main__':
    launch()
    #C3toolbox.startup()
    #C3toolbox.drums_animations('PART DRUMS', 0, 0, 0, 'e', 4, 10, 0)
    
