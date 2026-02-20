from __future__ import absolute_import
from reaper_python import *
import C3toolbox
import sys
import os
sys.argv=["Main"]

import tkinter
global instrument_var
global fldRowTxt
global level_var
global grid_var
global bendChkvar
global opensChkvar
global sameChkvar
global sparseChkvar

CAT_LABEL = "Remove notes"
CAT_CATEGORY = "5-Lane / Drums"
CAT_ORDER = 1

def execute(sel):
    global form
    array_grid = { "1" : "w", "1/2" : "h", "1/4" : "q", "1/8" : "e", "1/16" : "s" }
    #RPR_ShowConsoleMsg(sel)
    instrument = str(instrument_var.get())
    instrument = C3toolbox.array_instruments[instrument]
    tolerance = str(fldRowTxt.get())
    if tolerance == '':
        tolerance = 20
    level = str(level_var.get())
    grid = str(grid_var.get())
    bend = str(bendChkvar.get())
    opens_to_green = str(opensChkvar.get())
    same = str(sameChkvar.get())
    sparse = str(sparseChkvar.get())
    if instrument == "PART REAL_KEYS":
        instrument = instrument + C3toolbox.array_levels[level][1]
        
    #RPR_ShowConsoleMsg(array_grid[grid]+" - "+array_levels[level][0]+" - "+instrument+" - "+tolerance+" - "+same+" - "+sparse+" - "+bend+" - "+str(sel))
    #RPR_ShowConsoleMsg(instrument+" - "+level+" - "+grid+" - "+tolerance+" - "+bend+" - "+same+" - "+sparse)
    C3toolbox.startup()
    
    C3toolbox.remove_notes(array_grid[grid], C3toolbox.array_levels[level][0], instrument, int(tolerance), int(same), int(sparse), int(bend), int(opens_to_green), int(sel))
    #(what,level,instrument,how,same,sparse,bend,selected)
    #C3toolbox.remove_notes('q', 'x', '', 10, 0, 0, 0, 0)
    form.destroy()

def launch():
    global instrument_var
    global fldRowTxt
    global level_var
    global grid_var
    global bendChkvar
    global opensChkvar
    global sameChkvar
    global sparseChkvar
    global form
    
    form = tkinter.Tk()
    getFld = tkinter.IntVar()
    form.wm_title('Remove notes')
    C3toolbox.startup()
    instrument_name = C3toolbox.get_trackname()
    if instrument_name in C3toolbox.array_dropdownid:
        instrument_id = C3toolbox.array_dropdownid[instrument_name]
    else:
        instrument_id = 0
    instrument_track = C3toolbox.get_trackid()
    array_instrument_data = C3toolbox.process_instrument(instrument_track)
    array_instrument_notes = array_instrument_data[1]
    array_notesevents = C3toolbox.create_notes_array(array_instrument_notes)
    curlevel = C3toolbox.level(array_notesevents[0], instrument_track)
    if curlevel is None:
        form.destroy()
        return

    # STEP 1
    stepOne = tkinter.LabelFrame(form, text=" 1. Select instrument and difficulty level: ")
    stepOne.grid(row=0, columnspan=8, sticky='WE', \
                 padx=5, pady=5, ipadx=5, ipady=5)

    inFileLbl = tkinter.Label(stepOne, text="Select instrument")
    inFileLbl.grid(row=0, column=0, sticky='E', padx=5, pady=2)

    OPTIONS = ["Guitar", "Rhythm", "Bass", "Drums", "Keys", "Pro Keys", "Pro Guitar", "Pro Guitar (22)", "Pro Bass", "Pro Bass (22)"]

    # Pro guitar/bass IDs
    if instrument_id in range(8,13):
        instrument_id -= 1

    if instrument_id > len(OPTIONS) - 1: instrument_id = 0
    instrument_var = tkinter.StringVar(stepOne)
    instrument_var.set(OPTIONS[instrument_id]) # default value

    instrumentOpt = tkinter.OptionMenu(stepOne, instrument_var, *OPTIONS)
    instrumentOpt.grid(row=0, column=1, columnspan=1, sticky="WE", pady=3)

    levelLbl = tkinter.Label(stepOne, text=" |   Select difficulty")
    levelLbl.grid(row=0, column=4, sticky='E', padx=5, pady=2)

    OPTIONS = ["Expert", "Hard", "Medium", "Easy"]

    level_var = tkinter.StringVar(stepOne)
    level_var.set(OPTIONS[C3toolbox.array_levels_id[curlevel]]) # default value

    levelOpt = tkinter.OptionMenu(stepOne, level_var, *OPTIONS)
    levelOpt.grid(row=0, column=5, columnspan=4, sticky="WE", pady=3) 

    # STEP 2
    stepTwo = tkinter.LabelFrame(form, text=" 2. Choose grid for reduction: ")
    stepTwo.grid(row=1, columnspan=8, sticky='WE', \
                 padx=5, pady=5, ipadx=5, ipady=5)

    outTblLbl = tkinter.Label(stepTwo, \
          text="Select grid:")
    outTblLbl.grid(row=1, column=0, sticky='W', padx=5, pady=2)

    OPTIONS = ["1", "1/2", "1/4", "1/8"]

    grid_var = tkinter.StringVar(stepTwo)
    grid_var.set(OPTIONS[0]) # default value

    gridOpt = tkinter.OptionMenu(stepTwo, grid_var, *OPTIONS)
    gridOpt.grid(row=1, column=1, columnspan=1, sticky="W", pady=3)
    

    fldLbl = tkinter.Label(stepTwo, \
                           text="Tolerance in tick (0-30, 30=1/64th):")
    fldLbl.grid(row=1, column=3, padx=5, pady=2, sticky='W')

    fldRowTxt = tkinter.Entry(stepTwo)
    fldRowTxt.insert(0, "20")
    fldRowTxt.grid(row=1, column=4, columnspan=1, padx=5, pady=2, sticky='W')

    # STEP 3
    stepThree = tkinter.LabelFrame(form, text=" 3. Configure: ")
    stepThree.grid(row=2, columnspan=5, sticky='WE', \
                   padx=5, pady=5, ipadx=5, ipady=5)
    sameChkvar = tkinter.IntVar(stepThree)
    sameChk = tkinter.Checkbutton(stepThree, \
               text="Keep consecutive notes", onvalue=1, offvalue=0, variable=sameChkvar)
    sameChk.grid(row=3, column=1, sticky='W', padx=5, pady=2)

    sparseChkvar = tkinter.IntVar(stepThree)
    sparseChk = tkinter.Checkbutton(stepThree, \
               text="Keep sparse notes", onvalue=1, offvalue=0, variable=sparseChkvar)
    sparseChk.grid(row=3, column=2, sticky='W', padx=5, pady=2)    

    bendChkvar = tkinter.IntVar(stepThree)
    bendChk = tkinter.Checkbutton(stepThree, \
               text="Enable pitch bend detection", onvalue=1, offvalue=0, variable=bendChkvar)
    bendChk.grid(row=4, column=1, sticky='W', padx=5, pady=2)

    opensChkvar = tkinter.IntVar(stepThree)
    opensChk = tkinter.Checkbutton(stepThree, \
               text="Move open notes to green", onvalue=1, offvalue=0, variable=opensChkvar)
    opensChk.grid(row=4, column=2, sticky='W', padx=5, pady=2)

    # HELP
    helpLf = tkinter.LabelFrame(form, text=" Quick Help ")
    helpLf.grid(row=0, column=9, columnspan=1, rowspan=3, \
                sticky='NS', padx=5, pady=5)
    helpLbl = tkinter.Label(helpLf, text="Check documentation\nfor configuration switches\n\n\n\n\n")
    helpLbl.grid(row=0, columnspan=1, column=9, sticky='W')
    
    selFileBtn = tkinter.Button(helpLf, text="Reduce selected", command= lambda: execute(1)) 
    selFileBtn.grid(row=6, column=9, sticky="WE", padx=5, pady=2)

    okFileBtn = tkinter.Button(helpLf, text="Reduce", command= lambda: execute(0))
    okFileBtn.grid(row=7, column=9, sticky="WE", padx=5, pady=2)

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
    #C3toolbox.remove_notes('q','x','PART GUITAR',20,0,0,0,0)
    #(what,level,instrument,how,same,sparse,bend,selected)
    #example: C3toolbox.remove_notes('q', 'x', '', 10, 0, 0, 0, 0)
