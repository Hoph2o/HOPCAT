from __future__ import print_function
from reaper_python import *
import sys
import tkinter as tk

APP_TITLE = "MIDI Note Selector"

CAT_LABEL = "MIDI Note Selector"
CAT_CATEGORY = "Misc"
CAT_ORDER = 1

# -------- REAPER helpers --------

def get_active_take():
    editor = RPR_MIDIEditor_GetActive()
    if not editor:
        return None
    return RPR_MIDIEditor_GetTake(editor)

def enum_selected_note_indices(take):
    idx = -1
    out = []
    while True:
        idx = RPR_MIDI_EnumSelNotes(take, idx)
        if idx == -1:
            break
        out.append(idx)
    return out

def get_note_fields(take, idx):
    t = RPR_MIDI_GetNote(take, idx, False, False, 0.0, 0.0, 0, 0, 0)
    if not isinstance(t, (list, tuple)) or len(t) < 8:
        raise RuntimeError("Unexpected return from RPR_MIDI_GetNote: {}".format(t))
    selected, muted, s, e, ch, p, v = t[-7:]
    return selected, muted, s, e, ch, p, v

def set_note_selected(take, idx, make_selected):
    selected, muted, s, e, ch, p, v = get_note_fields(take, idx)
    RPR_MIDI_SetNote(take, idx, bool(make_selected), bool(muted),
                     float(s), float(e), int(ch), int(p), int(v), False)

def apply_selection(step, offset):
    take = get_active_take()
    if not take:
        RPR_ShowMessageBox("Open a MIDI editor and try again.", APP_TITLE, 0)
        return

    sel = enum_selected_note_indices(take)
    if not sel:
        RPR_ShowMessageBox("No selected notes found in the active take.", APP_TITLE, 0)
        return

    if step < 1:
        step = 1
    if offset < 1:
        offset = 1
    start_idx = offset - 1

    RPR_Undo_BeginBlock()
    RPR_MIDI_SelectAll(take, False)

    for i in range(start_idx, len(sel), step):
        set_note_selected(take, sel[i], True)

    RPR_MIDI_Sort(take)
    RPR_Undo_EndBlock("MIDI: Select every n-th note (Python)", -1)

# -------- Tk UI --------
form = None
class NoteSelectorUI(object):
    def __init__(self):
        global form
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.resizable(False, False)
        form = self.root
        # Always on top
        try:
            self.root.attributes("-topmost", True)
        except Exception:
            pass
        self.root.lift()
        #self._arm_topmost_watchdog()

        pad = {"padx": 6, "pady": 1}

        # Headline labels
        self.lbl_line1 = tk.Label(self.root, text="Select every 2nd note, starting with the 2nd note")
        self.lbl_line1.grid(row=0, column=0, columnspan=2, **pad)

        # Wider layout
        self.root.columnconfigure(1, weight=1, minsize=100)

        # Step slider: 1..16
        tk.Label(self.root, text="n (step)").grid(row=2, column=0, sticky="w", **pad)
        self.var_step = tk.IntVar(value=2)
        self.sld_step = tk.Scale(self.root, from_=1, to=16, orient=tk.HORIZONTAL,
                                 showvalue=True, resolution=1, length=100,
                                 variable=self.var_step, command=self._on_slider)
        self.sld_step.grid(row=2, column=1, sticky="ew", **pad)

        # Offset slider: 1..16
        tk.Label(self.root, text="offset").grid(row=3, column=0, sticky="w", **pad)
        self.var_offset = tk.IntVar(value=2)
        self.sld_offset = tk.Scale(self.root, from_=1, to=16, orient=tk.HORIZONTAL,
                                   showvalue=True, resolution=1, length=100,
                                   variable=self.var_offset, command=self._on_slider)
        self.sld_offset.grid(row=3, column=1, sticky="ew", **pad)

        # Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=(12, 12))

        self.btn_go = tk.Button(btn_frame, text="Go!", width=12, command=self.on_go)
        self.btn_go.pack(side=tk.LEFT, padx=8)

        self.btn_close = tk.Button(btn_frame, text="Close", width=12, command=self.root.destroy)
        self.btn_close.pack(side=tk.LEFT, padx=8)

        self._refresh_labels()

        # Center the window at a double-wide size
        self._center_window(width=300, height=160)

        # Keep topmost when clicking elsewhere
        #self.root.bind("<FocusOut>", self._reassert_topmost)

    def _center_window(self, width=300, height=160):
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = int((sw - width) / 2)
        y = int((sh - height) / 2)
        self.root.geometry("{}x{}+{}+{}".format(width, height, x, y))

    #def _arm_topmost_watchdog(self):
        #def _tick():
            #try:
                #self.root.attributes("-topmost", True)
                #self.root.lift()
            #finally:
                #self.root.after(500, _tick)
        #self.root.after(500, _tick)

    #def _reassert_topmost(self, _evt=None):
        #try:
            #self.root.attributes("-topmost", True)
            #self.root.lift()
        #except Exception:
            #pass

    @staticmethod
    def _ordinal(n):
        try:
            n = int(n)
        except Exception:
            return str(n)
        if 10 <= (n % 100) <= 20:
            suffix = "th"
        else:
            last = n % 10
            if last == 1:
                suffix = "st"
            elif last == 2:
                suffix = "nd"
            elif last == 3:
                suffix = "rd"
            else:
                suffix = "th"
        return "{}{}".format(n, suffix)

    def _refresh_labels(self):
        step = self.var_step.get()
        offset = self.var_offset.get()

        text = "Select every {} note, starting with the {} note".format(
            self._ordinal(step), self._ordinal(offset)
        )

        self.lbl_line1.config(text=text)

    def _on_slider(self, _evt=None):
        self._refresh_labels()

    def on_go(self):
        try:
            step = int(self.var_step.get())
            offset = int(self.var_offset.get())
            apply_selection(step, offset)
            #self._reassert_topmost()
            try:
                self.root.focus_force()
            except Exception:
                pass
        except Exception as e:
            RPR_ShowConsoleMsg("[{}] Error: {}\n".format(APP_TITLE, e))

    def run(self):
        try:
            self.root.mainloop()
        except Exception as e:
            RPR_ShowConsoleMsg("[{}] UI error: {}\n".format(APP_TITLE, e))

def launch():
    NoteSelectorUI()

if __name__ == '__main__':
    launch()
