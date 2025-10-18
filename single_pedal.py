from reaper_python import *
import C3toolbox
import sys
import os
sys.argv=["Main"]
import Tkinter

global level_var
global form
global moveChkvar

def execute(selected):
    global level_var
    global form
    global moveChkvar
    level = str(level_var.get())
    move = moveChkvar.get()

    C3toolbox.startup()
    C3toolbox.single_pedal(C3toolbox.array_levels[level][0], 20, int(move), selected)
    #instrument, level, fix, move, selected
    window.close()
    form.destroy()

def launch():
    global level_var
    global form
    global moveChkvar
    
    C3toolbox.startup()
    form = Tkinter.Tk()
    form.wm_title('Reduce double pedal kicks to single pedal kicks')
    
    helpLf = Tkinter.Frame(form)
    helpLf.grid(row=0, column=1, sticky='NS', padx=5, pady=5)

    OPTIONS = ["Expert", "Hard", "Medium", "Easy"]

    level_var = Tkinter.StringVar(helpLf)
    level_var.set(OPTIONS[0]) # default value

    levelOpt = apply(Tkinter.OptionMenu, (helpLf, level_var) + tuple(OPTIONS))
    levelOpt.grid(row=0, column=1, columnspan=1, sticky="WE", pady=3)

    allBtn = Tkinter.Button(helpLf, text="Reduce all", command= lambda: execute(0)) 
    allBtn.grid(row=0, column=2, rowspan=1, sticky="WE", padx=5, pady=2)

    selBtn = Tkinter.Button(helpLf, text="Reduce selected", command= lambda: execute(1)) 
    selBtn.grid(row=0, column=3, rowspan=1, sticky="WE", padx=5, pady=2)

    moveChkvar = Tkinter.IntVar(helpLf)
    moveChk = Tkinter.Checkbutton(helpLf, \
               text="Move to X+ kick instead of removing", onvalue=1, offvalue=0, variable=moveChkvar)
    moveChk.grid(row=1, column=1, sticky='W', padx=5, pady=2)
    moveChk.select()

    logo = Tkinter.Frame(form, bg="#000")
    logo.grid(row=1, column=0, columnspan=10, sticky='WE', \
                 padx=0, pady=0, ipadx=0, ipady=0)

    path = os.path.join( sys.path[0], "banner.gif" )
    img = Tkinter.PhotoImage(file=path)
    imageLbl = Tkinter.Label(logo, image = img, borderwidth=0)
    imageLbl.grid(row=0, column=0, rowspan=2, sticky='E', padx=0, pady=0)

    form.mainloop()

if __name__ == '__main__':
    launch()
    #C3toolbox.startup()
    #C3toolbox.single_pedal('x', 20, 0)
