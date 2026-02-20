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
global odvar
global tolerance

CAT_LABEL = "Create phrase markers"
CAT_CATEGORY = "Vocals"
CAT_ORDER = 1

def execute(sel):
    global instrument_var
    global grid_var
    global form
    global odvar
    global tolerance
    instrument = str(instrument_var.get())
    odvar = str(odvar.get())
    
    grid = str(grid_var.get())
    grid_array = { 'Quarter grid' : 480, 'Eighth grid' : 240 }
    grid = grid_array[grid]
    tolerance = tolerance.get()
    if tolerance == '':
        tolerance = 4    
    vocal_tracks = ["Vocals", "Harmony 1", "Harmony 2"]
    harmony_tracks = ["Harmony 1", "Harmony 2"]
    C3toolbox.startup()
    if instrument == "Harmonies":
        overdrive = C3toolbox.array_instruments["Harmony 1"]
        for x in range(0, len(harmony_tracks)):
            instrument = C3toolbox.array_instruments[harmony_tracks[x]]
            C3toolbox.create_phrase_markers(instrument, grid, 0)
    elif instrument == "Vocals and Harmonies":
        overdrive = C3toolbox.array_instruments["Vocals"]
        for x in range(0, len(vocal_tracks)):
            instrument = C3toolbox.array_instruments[vocal_tracks[x]]
            C3toolbox.create_phrase_markers(instrument, grid, 0)
    else:
        overdrive = C3toolbox.array_instruments[instrument]
        C3toolbox.PM(">" + overdrive)
        instrument = C3toolbox.array_instruments[instrument]
        C3toolbox.create_phrase_markers(instrument, grid, 0)
        
    if odvar == 1:
        C3toolbox.add_vocalsoverdrive(overdrive, int(tolerance), 0)
    
    #instrument, level, option, selected
    form.destroy()

def launch():
    global instrument_var
    global grid_var
    global form
    global odvar
    global tolerance
    
    form = tkinter.Tk()
    getFld = tkinter.IntVar()
    
    form.wm_title('Create phrase markers')
    C3toolbox.startup()
    instrument_name = C3toolbox.get_trackname()
    if instrument_name in C3toolbox.array_dropdownvocals:
        instrument_id = C3toolbox.array_dropdownvocals[instrument_name]
    else:
        instrument_id = 0

    # STEP 1
    helpLf = tkinter.Frame(form)
    helpLf.grid(row=0, column=1, sticky='NS', padx=5, pady=5)
    
    OPTIONS = ["Vocals", "Harmony 1", "Harmony 2", "Harmonies", "Vocals and Harmonies" ]

    instrument_var = tkinter.StringVar(helpLf)
    instrument_var.set(OPTIONS[instrument_id]) # default value

    instrumentOpt = tkinter.OptionMenu(helpLf, instrument_var, *OPTIONS)
    instrumentOpt.grid(row=0, column=1, columnspan=1, sticky="WE", pady=3)
    
    OPTIONS = ["Quarter grid", "Eighth grid"]

    grid_var = tkinter.StringVar(helpLf)
    grid_var.set(OPTIONS[0]) # default value

    gridOpt = tkinter.OptionMenu(helpLf, grid_var, *OPTIONS)
    gridOpt.grid(row=0, column=2, columnspan=1, sticky="WE", pady=3)

    odvar = tkinter.IntVar(helpLf)
    odChk = tkinter.Checkbutton(helpLf, \
               text="Create overdrive markers for Vocals or Harmony 1 (for every number of phrases)", onvalue=1, offvalue=0, variable=odvar)
    odChk.grid(row=0, column=3, sticky='W', padx=5, pady=2)

    tolerance = tkinter.Entry(helpLf)
    tolerance.insert(0, "4")
    tolerance.config(width=5)
    tolerance.grid(row=0, column=4, padx=5, pady=2, sticky='W')
    
    allBtn = tkinter.Button(helpLf, text="Create phrase markers", command= lambda: execute(0)) 
    allBtn.grid(row=0, column=5, rowspan=1, sticky="WE", padx=5, pady=2)
    
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
    #C3toolbox.create_phrase_markers('PART VOCALS', 480, 0) #Do not set SELECTED to 1, it won't work

