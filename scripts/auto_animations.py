from __future__ import absolute_import
from reaper_python import *
import C3toolbox
import sys
import os
sys.argv=["Main"]
import tkinter

global form
global level_var
global instrument_var
global crashChkvar
global softChkvar
global flamChkvar
global ghostChkvar
global tolerance
global form
global expression_var
global fldRowTxt
global mutevar
global beattrack_var
global keysvar

CAT_LABEL = "Automatic animations"
CAT_CATEGORY = "System & Supersets"
CAT_ORDER = 1

def execute(selected):
    global beattrack_var
    global level_var
    global instrument_var
    global crashChkvar
    global softChkvar
    global flamChkvar
    global ghostChkvar
    global tolerance
    global form
    global expression_var
    global fldRowTxt
    global mutevar
    global keysvar
    
    C3toolbox.startup()
    
    expression = str(expression_var.get())
    pause = str(fldRowTxt.get())
    if pause == 'default':
        pause = 0
    
    level = str(level_var.get())
    grid_array = { '1/16' : 'e', '1/32' : 's' }
    grid = grid_array[level]
    crash = crashChkvar.get()
    soft = softChkvar.get()
    flam = flamChkvar.get()
    ghost = ghostChkvar.get()
    keysvar = int(keysvar.get())
    tolerance = tolerance.get()
    if tolerance == '':
        tolerance = 4
    
    mutevar = mutevar.get()
    beattrack = beattrack_var.get()
    if beattrack == 'Normal BEAT track':
        beattrack = 0
    else:
        beattrack = 1
        
    
    #C3toolbox.PM(str(beattrack) + " - " + str(expression) + " - " + str(pause) + " - " + str(grid) + " - " + str(crash) + " - " + str(soft) + " - " + str(flam) + " - " + str(tolerance) + " - " + str(mutevar))
    C3toolbox.startup()
    C3toolbox.auto_animations(beattrack, expression, pause, grid, crash, soft, flam, ghost, tolerance, keysvar, mutevar)
    form.destroy()

def launch():
    global beattrack_var
    global level_var
    global instrument_var
    global crashChkvar
    global softChkvar
    global flamChkvar
    global ghostChkvar
    global tolerance
    global form
    global expression_var
    global fldRowTxt
    global mutevar
    global keysvar
    
    form = tkinter.Tk()
    form.wm_title('Auto animations')

    C3toolbox.startup()
      
    # GENERAL
    
    general = tkinter.LabelFrame(form, text=" General animations: ")
    general.grid(row=0, columnspan=4, sticky='WE', \
                 padx=5, pady=5, ipadx=5, ipady=5)

    OPTIONS = ["Normal BEAT track", "Halved BEAT track"]

    beattrack_var = tkinter.StringVar(general)
    beattrack_var.set(OPTIONS[0]) # default value

    beattrackOpt = tkinter.OptionMenu(general, beattrack_var, *OPTIONS)
    beattrackOpt.grid(row=0, column=1, sticky="W", pady=3)

    OPTIONS = ["play", "mellow", "intense"]

    expression_var = tkinter.StringVar(general)
    expression_var.set(OPTIONS[0]) # default value

    expressionOpt = tkinter.OptionMenu(general, expression_var, *OPTIONS)
    expressionOpt.grid(row=0, column=2, columnspan=1, sticky="WE", pady=3)

    fldLbl = tkinter.Label(general, \
                           text="Ticks to trigger idle:")
    fldLbl.grid(row=0, column=3, padx=5, pady=2, sticky='W')
    var = tkinter.StringVar()
    fldRowTxt = tkinter.Entry(general, textvariable=var)
    var.set('default')
    fldRowTxt.grid(row=0, column=4, columnspan=1, padx=5, pady=2, sticky='W')

    # KEYS

    keysanim = tkinter.LabelFrame(form, text=" Pro keys animations: ")
    keysanim.grid(row=3, columnspan=5, sticky='WE', \
                 padx=5, pady=5, ipadx=5, ipady=5)

    keysvar = tkinter.IntVar(keysanim)
    keysvarChk = tkinter.Checkbutton(keysanim, \
               text="Create pro keys animations from Real Keys X", onvalue=1, offvalue=0, variable=keysvar)
    keysvarChk.grid(row=0, column=1, sticky='W', padx=5, pady=2)
    if C3toolbox.tracks_array['PART REAL_KEYS_X'] != 999:
        keysvarChk.select()
    
    # DRUMS
    
    drumsanim = tkinter.LabelFrame(form, text=" Drums animations: ")
    drumsanim.grid(row=4, columnspan=5, sticky='WE', \
                 padx=5, pady=5, ipadx=5, ipady=5)

    levelLbl = tkinter.Label(drumsanim, text="Select grid")
    levelLbl.grid(row=0, column=1, sticky='WE', padx=5, pady=2)

    OPTIONS = ["1/16", "1/32"]

    level_var = tkinter.StringVar(drumsanim)
    level_var.set(OPTIONS[0]) # default value

    levelOpt = tkinter.OptionMenu(drumsanim, level_var, *OPTIONS)
    levelOpt.grid(row=1, column=1, sticky="WE", pady=3)

    crashChkvar = tkinter.IntVar(drumsanim)
    crashChk = tkinter.Checkbutton(drumsanim, \
               text="CRASH1 as default crash", onvalue=1, offvalue=0, variable=crashChkvar)
    crashChk.grid(row=0, column=2, sticky='W', padx=5, pady=2)
    
    softChkvar = tkinter.IntVar(drumsanim)
    softChk = tkinter.Checkbutton(drumsanim, \
               text="Soft as default for snare/crash", onvalue=1, offvalue=0, variable=softChkvar)
    softChk.grid(row=1, column=2, sticky='W', padx=5, pady=2)    

    toleranceLbl = tkinter.Label(drumsanim, \
                           text="Min. cymbals hits:")
    toleranceLbl.grid(row=0, column=3, padx=5, pady=2, sticky='W')

    tolerance = tkinter.Entry(drumsanim)
    tolerance.insert(0, "4")
    tolerance.config(width=5)
    tolerance.grid(row=1, column=3, padx=5, pady=2, sticky='W')

    mutevar = tkinter.IntVar(drumsanim)
    muteChk = tkinter.Checkbutton(drumsanim, \
               text="Overwrite notes", onvalue=1, offvalue=0, variable=mutevar)
    muteChk.grid(row=2, column=1, sticky='W', padx=5, pady=2)

    flamChkvar = tkinter.IntVar(drumsanim)
    flamChk = tkinter.Checkbutton(drumsanim, \
               text="Make snare+Y toms flams", onvalue=1, offvalue=0, variable=flamChkvar)
    flamChk.grid(row=2, column=2, sticky='W', padx=5, pady=2)
    flamChk.select()

    ghostChkvar = tkinter.IntVar(drumsanim)
    ghostChk = tkinter.Checkbutton(drumsanim, \
               text="Make vel. 1 snare soft hits", onvalue=1, offvalue=0, variable=ghostChkvar)
    ghostChk.grid(row=2, column=3, sticky='W', padx=5, pady=2)
    ghostChk.select()

    allBtn = tkinter.Button(drumsanim, text="Create animations", command= lambda: execute(0)) 
    allBtn.grid(row=3, column=3, sticky="WE", padx=5, pady=2)
    
    logo = tkinter.Frame(form, bg="#000")
    logo.grid(row=5, column=0, columnspan=10, sticky='WE', \
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
    #C3toolbox.reduce_5lane('PART BASS', [1, 1, 1], ['e', 0, 1, 1], ['q', 1, 1, 0], ['h', 1, 1, 0], 0, 10)
