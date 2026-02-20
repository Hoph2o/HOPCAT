from __future__ import absolute_import
from reaper_python import *
import C3toolbox
import os
import sys
sys.argv=["Main"]
import tkinter

global tuningE
global tuningA
global tuningD
global tuningG
global tuningB
global tuninge
global instrument_var
global form

CAT_LABEL = "Generate Root Notes"
CAT_CATEGORY = "Pro"
CAT_ORDER = 1

def execute(a):

    global tuningE
    global tuningA
    global tuningD
    global tuningG
    global tuningB
    global tuninge
    global instrument_var
    global form
    
    C3toolbox.startup()
    instrument = str(instrument_var.get())
    instrument = C3toolbox.array_instruments[instrument]
    stringE = tuningE.get()
    stringA = tuningA.get()
    stringD = tuningD.get()
    stringG = tuningG.get()
    stringB = tuningB.get()
    stringe = tuninge.get()
    C3toolbox.pg_root_notes(instrument, int(stringE), int(stringA), int(stringD), int(stringG), int(stringB), int(stringe))
    form.destroy()

def launch():

    global tuningE
    global tuningA
    global tuningD
    global tuningG
    global tuningB
    global tuninge
    global instrument_var
    global form
    form = tkinter.Tk()
    form.wm_title('Root Notes Generator')
    
    helpLf = tkinter.Frame(form)
    helpLf.grid(row=0, column=1, sticky='NS', padx=5, pady=5)

    inFileLbl = tkinter.Label(helpLf, text="Select instrument")
    inFileLbl.grid(row=0, column=1, sticky='E', padx=5, pady=2)

    OPTIONS = ["Pro Guitar", "Pro Bass", "Pro Guitar 22", "Pro Bass 22"]

    instrument_var = tkinter.StringVar(helpLf)
    instrument_var.set(OPTIONS[0]) # default value

    instrumentOpt = tkinter.OptionMenu(helpLf, instrument_var, *OPTIONS)
    instrumentOpt.grid(row=0, column=2, columnspan=1, sticky="WE", pady=3)

    tuningLbl = tkinter.Label(helpLf, \
                           text="Tuning:")
    tuningLbl.grid(row=0, column=3, padx=0, pady=2, sticky='W')

    tuningE = tkinter.Entry(helpLf)
    tuningE.insert(0, "0")
    tuningE.config(width=2)
    tuningE.grid(row=0, column=4, padx=0, pady=0, sticky='W')

    tuningA = tkinter.Entry(helpLf)
    tuningA.insert(0, "0")
    tuningA.config(width=2)
    tuningA.grid(row=0, column=5, padx=0, pady=0, sticky='W')

    tuningD = tkinter.Entry(helpLf)
    tuningD.insert(0, "0")
    tuningD.config(width=2)
    tuningD.grid(row=0, column=6, padx=0, pady=0, sticky='W')

    tuningG = tkinter.Entry(helpLf)
    tuningG.insert(0, "0")
    tuningG.config(width=2)
    tuningG.grid(row=0, column=7, padx=0, pady=0, sticky='W')

    tuningB = tkinter.Entry(helpLf)
    tuningB.insert(0, "0")
    tuningB.config(width=2)
    tuningB.grid(row=0, column=8, padx=0, pady=0, sticky='W')

    tuninge = tkinter.Entry(helpLf)
    tuninge.insert(0, "0")
    tuninge.config(width=2)
    tuninge.grid(row=0, column=9, padx=0, pady=0, sticky='W')
    
    allBtn = tkinter.Button(helpLf, text="Generate Root Notes", command= lambda: execute(0)) 
    allBtn.grid(row=1, column=4, rowspan=1, columnspan=6, sticky="WE", padx=5, pady=2)

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
    

