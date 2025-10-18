from reaper_python import *
import C3toolbox
import sys
import os
import traceback
sys.argv = ["Main"]

import Tkinter
import tkFileDialog
import ConfigParser
import re

# Globals
global form, meta_entries, diff_entries

EXTSTATE_SECTION = "SongMetaSaver"
EXTSTATE_KEY_LASTDIR = "last_dir"

def get_project_dir_fallback():
    """Prefer last saved dir, else current project dir"""
    last_dir = RPR_GetExtState(EXTSTATE_SECTION, EXTSTATE_KEY_LASTDIR)
    if last_dir and os.path.isdir(last_dir):
        return last_dir

    try:
        _, _, proj_path, _ = RPR_GetProjectPathEx(0, "", 8192)
        if proj_path and os.path.isdir(proj_path):
            return proj_path
    except Exception:
        pass

    try:
        _, proj_path, _ = RPR_GetProjectPath("", 4096)
        if proj_path and os.path.isdir(proj_path):
            return proj_path
    except Exception:
        pass

    return os.getcwd()

def save_ini(meta, diffs):
    """Writes INI in exact order"""
    order = [
        "delay", "multiplier_note",
        "artist", "name", "album", "track", "year", "genre",
        "pro_drums", "kit_type",
        "diff_drums", "diff_drums_real",
        "diff_bass", "diff_bass_real",
        "diff_rhythm", "diff_guitar", "diff_guitar_real",
        "diff_keys", "diff_keys_real",
        "diff_vocals", "diff_vocals_harm", "diff_band",
        "charter", "icon", "loading_phrase", "preview_start_time",
        "song_length"
    ]

    data = {}

    # Fill from entries
    for key, val in meta.items():
        val = val if not isinstance(val, unicode) else val.encode("utf-8")
        data[key.lower()] = val

    # Add difficulty values
    for key, val in diffs.items():
        v = val.strip() if val.strip() != "" else "-1"
        v = v if not isinstance(v, unicode) else v.encode("utf-8")
        data["diff_" + key.lower()] = v

    # Fixed values
    data["delay"] = "0"
    data["multiplier_note"] = "116"
    data["pro_drums"] = "True"
    data["kit_type"] = "1"
    data["song_length"] = ""

    initial_dir = get_project_dir_fallback()
    default_name = "song.ini"
    file_path = tkFileDialog.asksaveasfilename(
        title="Save Song Metadata",
        initialdir=initial_dir,
        initialfile=default_name,
        defaultextension=".ini",
        filetypes=[("INI files", "*.ini"), ("All files", "*.*")]
    )

    if not file_path:
        RPR_ShowConsoleMsg("Save cancelled.\n")
        return False

    try:
        with open(file_path, "w") as f:
            f.write("[song]\n")
            for key in order:
                if key in data:
                    f.write("{} = {}\n".format(key, data[key]))
                elif key.startswith("diff_"):
                    f.write("{} = -1\n".format(key))
                else:
                    f.write("{} = \n".format(key))

        RPR_SetExtState(EXTSTATE_SECTION, EXTSTATE_KEY_LASTDIR, os.path.dirname(file_path), True)
        return True
    except Exception:
        RPR_ShowConsoleMsg("Failed to save INI:\n" + traceback.format_exc())
        return False

def execute(_evt=None):
    """Collect and save metadata."""
    global meta_entries, diff_entries, form
    try:
        meta = {
            "Name":  meta_entries["Name"].get().strip(),
            "Artist": meta_entries["Artist"].get().strip(),
            "Album": meta_entries["Album"].get().strip(),
            "Track": meta_entries["Track"].get().strip(),
            "Year":  re.sub(r"[^0-9]", "", meta_entries["Year"].get().strip()),
            "Genre": meta_entries["Genre"].get().strip(),
            "Charter": meta_entries["Charter"].get().strip(),
            "Icon": meta_entries["Icon"].get().strip(),
            "Loading_Phrase": meta_entries["Loading_Phrase"].get().strip(),
            "Preview_Start_Time": re.sub(r"[^0-9]", "", meta_entries["Preview_Start_Time"].get().strip())
        }

        diffs = {k: v.get().strip() for k, v in diff_entries.items()}

        C3toolbox.startup()

        if save_ini(meta, diffs):
            form.destroy()

    except Exception:
        RPR_ShowConsoleMsg("Exception occurred:\n" + traceback.format_exc())

def launch():
    global form, meta_entries, diff_entries
    form = Tkinter.Tk()
    form.wm_title("Song Metadata")
    C3toolbox.startup()

    meta_entries = {}
    diff_entries = {}

    meta_fields = [
        "Name", "Artist", "Album", "Track", "Year", "Genre",
        "Charter", "Icon", "Loading_Phrase", "Preview_Start_Time"
    ]

    Tkinter.Label(form, text="Info", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2, pady=(5, 10))

    for i, field in enumerate(meta_fields, start=1):
        Tkinter.Label(form, text=field + ":").grid(row=i, column=0, padx=10, pady=4, sticky="e")
        entry = Tkinter.Entry(form, width=32)
        entry.grid(row=i, column=1, padx=10, pady=4, sticky="w")
        meta_entries[field] = entry

    diff_fields = [
        "Drums", "Drums_Real", "Bass", "Bass_Real", "Rhythm",
        "Guitar", "Guitar_Real", "Keys", "Keys_Real",
        "Vocals", "Vocals_Harm", "Band"
    ]

    Tkinter.Label(form, text="Difficulty", font=("Arial", 10, "bold")).grid(row=0, column=3, columnspan=2, pady=(5, 10))

    for j, field in enumerate(diff_fields, start=1):
        Tkinter.Label(form, text=field + ":").grid(row=j, column=3, padx=10, pady=3, sticky="e")
        entry = Tkinter.Entry(form, width=12)
        entry.grid(row=j, column=4, padx=10, pady=3, sticky="w")
        diff_entries[field] = entry

    last_row = max(len(meta_fields), len(diff_fields)) + 1
    Tkinter.Button(form, text="Create", command=execute).grid(row=last_row, column=0, columnspan=5, pady=10)
    form.bind("<Return>", execute)

    path = os.path.join(sys.path[0], "banner.gif")
    if os.path.exists(path):
        img = Tkinter.PhotoImage(file=path)
        lbl = Tkinter.Label(form, image=img, borderwidth=0)
        lbl.image = img
        lbl.grid(row=last_row + 1, column=0, columnspan=5, pady=5)

    form.mainloop()

if __name__ == "__main__":
    launch()
