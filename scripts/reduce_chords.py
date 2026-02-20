from __future__ import absolute_import
from reaper_python import *
import C3toolbox
import os
import sys
sys.argv=["Main"]
import tkinter

global level_var
global instrument_var
global fixChkvar
global Chkvar
global form

CAT_LABEL = "Reduce chords"
CAT_CATEGORY = "5-Lane / Drums"
CAT_ORDER = 1

def execute(selected):
    global level_var
    global instrument_var
    global fixChkvar
    global Chkvar
    global form
    level = str(level_var.get())
    instrument = str(instrument_var.get())
    instrument = C3toolbox.array_instruments[instrument]
    if instrument == "PART REAL_KEYS":
        instrument = instrument + C3toolbox.array_levels[level][1]
    option = fixChkvar.get()
    C3toolbox.startup()
    C3toolbox.reduce_chords(instrument, C3toolbox.array_levels[level][0], int(option), selected) #instrument, level, option, selected
    form.destroy()

def launch():
    global form
    global level_var
    global instrument_var
    global fixChkvar
    global Chkvar
    C3toolbox.startup()
    form = tkinter.Tk()
    form.wm_title('Reduce chords')

    instrument_name = C3toolbox.get_trackname()

    if instrument_name in C3toolbox.array_dropdownid_chords:
        instrument_id = C3toolbox.array_dropdownid_chords[instrument_name]
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
    
    helpLf = tkinter.Frame(form)
    helpLf.grid(row=0, column=1, sticky='NS', padx=5, pady=5)

    OPTIONS = ["Guitar", "Rhythm", "Bass", "Keys"]

    instrument_var = tkinter.StringVar(helpLf)
    instrument_var.set(OPTIONS[instrument_id]) # default value

    instrumentOpt = tkinter.OptionMenu(helpLf, instrument_var, *OPTIONS)
    instrumentOpt.grid(row=0, column=1, columnspan=1, sticky="WE", pady=3)


    OPTIONS = ["Hard", "Medium", "Easy"]

    level_var = tkinter.StringVar(helpLf)
    level_var.set(OPTIONS[C3toolbox.array_levels_id[curlevel]]) # default value

    levelOpt = tkinter.OptionMenu(helpLf, level_var, *OPTIONS)
    levelOpt.grid(row=0, column=2, columnspan=1, sticky="WE", pady=3) 

    fixChkvar = tkinter.IntVar(helpLf)
    fixChk = tkinter.Checkbutton(helpLf, \
               text="Enable option", onvalue=1, offvalue=0, variable=fixChkvar)
    fixChk.grid(row=0, column=3, sticky='W', padx=5, pady=2)
    
    allBtn = tkinter.Button(helpLf, text="Reduce all chords", command= lambda: execute(0)) 
    allBtn.grid(row=0, column=4, rowspan=1, sticky="WE", padx=5, pady=2)

    selBtn = tkinter.Button(helpLf, text="Reduce only selected", command= lambda: execute(1)) 
    selBtn.grid(row=0, column=5, rowspan=1, sticky="WE", padx=5, pady=2)

    inFileLbl = tkinter.Label(helpLf, text="Option is: Hard - Enable use of BG and RO chords; Medium - Allow use of BO chords; Easy - Allow for B and O notes")
    inFileLbl.grid(row=1, column=1, columnspan=5, sticky='E', padx=5, pady=2)    

    logo = tkinter.Frame(form, bg="#000")
    logo.grid(row=2, column=0, columnspan=10, sticky='WE', \
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
    #C3toolbox.reduce_chords('PART GUITAR', 'h', 1, 0)
    
