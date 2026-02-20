from __future__ import absolute_import
from reaper_python import *
import C3toolbox
import sys
import os
sys.argv=["Main"]

import tkinter
global instrument_var
global expression_var
global fldRowTxt
global level_var
global grid_var
global bendChkvar
global sameChkvar
global sparseChkvar
global grid_var

CAT_LABEL = "Delete empty phrases"
CAT_CATEGORY = "Vocals"
CAT_ORDER = 1

def execute():
    global instrument_var
    global grid_var
    global form
    instrument = str(instrument_var.get())
    instrument = C3toolbox.array_instruments[instrument]
    C3toolbox.startup()
    C3toolbox.cleanup_phrases(instrument) #instrument, level, option, selected
    form.destroy()

def launch():
    global instrument_var
    global form
    global grid_var
    
    form = tkinter.Tk()
    getFld = tkinter.IntVar()
    form.wm_title('Cleanup phrases')
    C3toolbox.startup()
    instrument_name = C3toolbox.get_trackname()
    if instrument_name in C3toolbox.array_dropdownvocals:
        instrument_id = C3toolbox.array_dropdownvocals[instrument_name]
    else:
        instrument_id = 0

    # STEP 1
    helpLf = tkinter.Frame(form)
    helpLf.grid(row=0, column=1, sticky='NS', padx=5, pady=5)
    
    inFileLbl = tkinter.Label(helpLf, text="Be careful when cleaning up phrases on complex harmony parts:")
    inFileLbl.grid(row=0, column=1, columnspan=2, sticky='WE', padx=5, pady=2)

    inFile2Lbl = tkinter.Label(helpLf, text="you may have empty phrases on H1 that cover notes on H3")
    inFile2Lbl.grid(row=1, column=1, columnspan=2, sticky='WE', padx=5, pady=2)
    
    OPTIONS = ["Vocals", "Harmony 1", "Harmony 2", "Harmony 3"]

    instrument_var = tkinter.StringVar(helpLf)
    instrument_var.set(OPTIONS[instrument_id]) # default value

    instrumentOpt = tkinter.OptionMenu(helpLf, instrument_var, *OPTIONS)
    instrumentOpt.grid(row=2, column=1, columnspan=1, sticky="WE", pady=3)

    allBtn = tkinter.Button(helpLf, text="Cleanup phrases", command= lambda: execute()) 
    allBtn.grid(row=2, column=2, rowspan=1, sticky="WE", padx=5, pady=2)
    
    logo = tkinter.Frame(form, bg="#000")
    logo.grid(row=8, column=0, columnspan=10, sticky='WE', \
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
    #C3toolbox.cleanup_phrases('PART VOCALS') #Do not set SELECTED to 1, it won't work

