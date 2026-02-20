from __future__ import absolute_import
from reaper_python import *
import C3toolbox
import sys
import os
sys.argv=["Main"]

import tkinter

CAT_LABEL = "Export lyrics"
CAT_CATEGORY = "Vocals"
CAT_ORDER = 1

def execute(sel):
    global instrument_var
    global form
    instrument = str(instrument_var.get())
    if instrument == "Every part":
        C3toolbox.startup()
        C3toolbox.export_lyrics_all(sel)
    else:
        instrument = C3toolbox.array_instruments[instrument]
        C3toolbox.startup()
        C3toolbox.export_lyrics(instrument, sel)
        
    #instrument, level, option, selected
    form.destroy()

def launch():
    global instrument_var
    global form
    
    form = tkinter.Tk()
    getFld = tkinter.IntVar()
    form.wm_title('Export lyrics')
    C3toolbox.startup()
    instrument_name = C3toolbox.get_trackname()
    if instrument_name in C3toolbox.array_dropdownvocals:
        instrument_id = C3toolbox.array_dropdownvocals[instrument_name]
    else:
        instrument_id = 0

    # STEP 1
    helpLf = tkinter.Frame(form)
    helpLf.grid(row=0, column=1, sticky='NS', padx=5, pady=5)
    
    OPTIONS = ["Vocals", "Harmony 1", "Harmony 2", "Harmony 3", "Every part"]

    instrument_var = tkinter.StringVar(helpLf)
    instrument_var.set(OPTIONS[instrument_id]) # default value
    instrumentOpt = tkinter.OptionMenu(helpLf, instrument_var, *OPTIONS)
    instrumentOpt.grid(row=0, column=1, columnspan=1, sticky="WE", pady=3)
    
    allBtn = tkinter.Button(helpLf, text="Export lyrics", command= lambda: execute(0)) 
    allBtn.grid(row=0, column=2, rowspan=1, sticky="WE", padx=5, pady=2)

    selBtn = tkinter.Button(helpLf, text="Export lyrics with phrase markers", command= lambda: execute(1)) 
    selBtn.grid(row=0, column=3, rowspan=1, sticky="WE", padx=5, pady=2)    
    
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
    #C3toolbox.export_lyrics('PART VOCALS', 1) #Do not set SELECTED to 1, it won't work

