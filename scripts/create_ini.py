from __future__ import absolute_import
from reaper_python import *
import C3toolbox

import sys
import os
import re
import traceback
import tkinter
from tkinter import filedialog
from configparser import ConfigParser
from tkinter import ttk

sys.argv = ["Main"]  # normalize for REAPER launcher

CAT_LABEL = "Create .ini"
CAT_CATEGORY = "Misc"
CAT_ORDER = 1

# --- Globals / Constants ---
EXTSTATE_SECTION      = "SongMetaSaver"
EXTSTATE_KEY_LASTDIR  = "last_dir"  # keep remembering last save folder for convenience

# Defaults file pinned to script directory
SCRIPT_DIR        = os.path.dirname(os.path.abspath(__file__))
DEFAULTS_BASENAME = "song_defaults.ini"
DEFAULTS_PATH     = os.path.join(SCRIPT_DIR, DEFAULTS_BASENAME)

# GUI field lists
META_FIELDS = [
    "Name", "Artist", "Album", "Track", "Year", "Genre",
    "Charter", "Icon", "Loading_Phrase", "Preview_Start_Time"
]
DIFF_FIELDS = [
    "Drums", "Drums_Real", "Bass", "Bass_Real", "Rhythm",
    "Guitar", "Guitar_Real", "Keys", "Keys_Real",
    "Vocals", "Vocals_Harm", "Band"
]

# Exact output order for song.ini
INI_ORDER = [
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

form = None
meta_entries = {}
diff_entries = {}

PAD_X, PAD_Y = 10, 6

# --- Utilities ---
def init_style(root):
    """Set a modern-ish ttk theme with slightly larger paddings."""
    s = ttk.Style()
    try:
        # 'vista' on Win, 'clam' cross-platform
        s.theme_use('vista')
    except Exception:
        s.theme_use('clam')

    # Slightly roomier widgets
    s.configure('TLabel', padding=(2, 2))
    s.configure('TEntry', padding=(2, 2))
    s.configure('TButton', padding=(6, 4))
    s.configure('Section.TLabelframe.Label', font=('Arial', 10, 'bold'))

def add_tooltip(widget, text):
    """Very small tooltip helper."""
    tip = {'win': None}
    def show(_e):
        if tip['win'] or not text: return
        x, y, cx, cy = widget.bbox("insert") if hasattr(widget, "bbox") else (0,0,0,0)
        x += widget.winfo_rootx() + 25
        y += widget.winfo_rooty() + 20
        tip['win'] = tw = tkinter.Toplevel(widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = ttk.Label(tw, text=text, relief='solid', borderwidth=1, padding=(6,3))
        label.pack()
    def hide(_e):
        if tip['win']:
            tip['win'].destroy()
            tip['win'] = None
    widget.bind("<Enter>", show)
    widget.bind("<Leave>", hide)

def labeled_entry(parent, label_text, width=28, padx=PAD_X, pady=PAD_Y, sticky_label='e', sticky_entry='we'):
    """Create a label + entry row inside `parent` and return the Entry."""
    row = parent.grid_size()[1]  # next row
    ttk.Label(parent, text=label_text + ":").grid(row=row, column=0, padx=padx, pady=pady, sticky=sticky_label)
    ent = ttk.Entry(parent, width=width)
    ent.grid(row=row, column=1, padx=padx, pady=pady, sticky=sticky_entry)
    return ent

def log(msg):
    try:
        RPR_ShowConsoleMsg(str(msg) + "\n")
    except Exception:
        pass

def u2b(s):
    if s is str:
        return s.encode("utf-8")
    return s

def digits_only(s):
    return re.sub(r"[^0-9]", "", s or "")

def get_project_dir_fallback():
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

def field_maps():
    meta_map = {
        "Name": "name",
        "Artist": "artist",
        "Album": "album",
        "Track": "track",
        "Year": "year",
        "Genre": "genre",
        "Charter": "charter",
        "Icon": "icon",
        "Loading_Phrase": "loading_phrase",
        "Preview_Start_Time": "preview_start_time",
    }
    diff_map = {
        "Drums": "diff_drums",
        "Drums_Real": "diff_drums_real",
        "Bass": "diff_bass",
        "Bass_Real": "diff_bass_real",
        "Rhythm": "diff_rhythm",
        "Guitar": "diff_guitar",
        "Guitar_Real": "diff_guitar_real",
        "Keys": "diff_keys",
        "Keys_Real": "diff_keys_real",
        "Vocals": "diff_vocals",
        "Vocals_Harm": "diff_vocals_harm",
        "Band": "diff_band",
    }
    return meta_map, diff_map

# --- Defaults load/save ---
def load_defaults_into_form(defaults_path):
    """Load [song] from song_defaults.ini in the script folder into the GUI."""
    if not defaults_path or not os.path.isfile(defaults_path):
        return False
    try:
        cfg = ConfigParser.RawConfigParser()
        cfg.optionxform = str
        cfg.read(defaults_path)

        section = "song" if cfg.has_section("song") else ("Song" if cfg.has_section("Song") else None)
        if not section:
            return False

        meta_map, diff_map = field_maps()

        for gui_label, ini_key in meta_map.items():
            if cfg.has_option(section, ini_key):
                val = cfg.get(section, ini_key)
                meta_entries[gui_label].delete(0, tkinter.END)
                meta_entries[gui_label].insert(0, val)

        for gui_label, ini_key in diff_map.items():
            if cfg.has_option(section, ini_key):
                val = cfg.get(section, ini_key)
                diff_entries[gui_label].delete(0, tkinter.END)
                diff_entries[gui_label].insert(0, val)

        return True
    except Exception:
        log("Failed to load defaults:\n" + traceback.format_exc())
        return False

def save_form_as_defaults(meta_dict, diffs_dict):
    """Write current GUI values to song_defaults.ini next to the script."""
    meta_map, diff_map = field_maps()
    try:
        # Ensure folder exists (it will)
        parent = os.path.dirname(DEFAULTS_PATH)
        if parent and not os.path.isdir(parent):
            try: os.makedirs(parent)
            except Exception: pass

        cfg = ConfigParser.RawConfigParser()
        cfg.optionxform = str
        cfg.add_section("song")

        for gui_label, ini_key in meta_map.items():
            cfg.set("song", ini_key, u2b(meta_dict.get(gui_label, "")))

        for gui_label, ini_key in diff_map.items():
            v = u2b(diffs_dict.get(gui_label, "").strip())
            cfg.set("song", ini_key, v)

        with open(DEFAULTS_PATH, "w") as f:
            cfg.write(f)

        log("Saved defaults to script folder: {}".format(DEFAULTS_PATH))
        return True
    except Exception:
        log("Failed to save defaults:\n" + traceback.format_exc())
        return False

# --- Data collection & final INI save ---
def collect_meta_from_form():
    return {
        "Name":               meta_entries["Name"].get().strip(),
        "Artist":             meta_entries["Artist"].get().strip(),
        "Album":              meta_entries["Album"].get().strip(),
        "Track":              meta_entries["Track"].get().strip(),
        "Year":               digits_only(meta_entries["Year"].get().strip()),
        "Genre":              meta_entries["Genre"].get().strip(),
        "Charter":            meta_entries["Charter"].get().strip(),
        "Icon":               meta_entries["Icon"].get().strip(),
        "Loading_Phrase":     meta_entries["Loading_Phrase"].get().strip(),
        "Preview_Start_Time": digits_only(meta_entries["Preview_Start_Time"].get().strip()),
    }

def collect_diffs_from_form():
    return {k: v.get().strip() for k, v in diff_entries.items()}

def save_ini(meta_dict, diffs_dict):
    data = {}

    for k, v in meta_dict.items():
        data[k.lower()] = u2b(v)

    for k, v in diffs_dict.items():
        v = v.strip()
        v = "-1" if v == "" else v
        data["diff_" + k.lower()] = u2b(v)

    data["delay"]           = "0"
    data["multiplier_note"] = "116"
    data["pro_drums"]       = "True"
    data["kit_type"]        = "1"
    data["song_length"]     = ""

    initial_dir  = get_project_dir_fallback()
    default_name = "song.ini"
    file_path = filedialog.asksaveasfilename(
        title="Save Song Metadata",
        initialdir=initial_dir,
        initialfile=default_name,
        defaultextension=".ini",
        filetypes=[("INI files", "*.ini"), ("All files", "*.*")]
    )
    if not file_path:
        log("Save cancelled.")
        return False

    try:
        with open(file_path, "w") as f:
            f.write("[song]\n")
            for key in INI_ORDER:
                if key in data:
                    f.write("{} = {}\n".format(key, data[key]))
                elif key.startswith("diff_"):
                    f.write("{} = -1\n".format(key))
                else:
                    f.write("{} = \n".format(key))
        RPR_SetExtState(EXTSTATE_SECTION, EXTSTATE_KEY_LASTDIR, os.path.dirname(file_path), True)
        return True
    except Exception:
        log("Failed to save INI:\n" + traceback.format_exc())
        return False

# --- UI Callbacks ---
def on_create(_evt=None):
    try:
        meta  = collect_meta_from_form()
        diffs = collect_diffs_from_form()
        C3toolbox.startup()
        if save_ini(meta, diffs):
            form.destroy()
    except Exception:
        log("Exception in on_create:\n" + traceback.format_exc())

def on_load_defaults():
    try:
        if not load_defaults_into_form(DEFAULTS_PATH):
            log("No defaults found at: {}".format(DEFAULTS_PATH))
    except Exception:
        log("Exception in on_load_defaults:\n" + traceback.format_exc())

def on_save_defaults():
    try:
        meta  = collect_meta_from_form()
        diffs = collect_diffs_from_form()
        save_form_as_defaults(meta, diffs)
    except Exception:
        log("Exception in on_save_defaults:\n" + traceback.format_exc())

# --- Launch UI ---
def launch():
    global form, meta_entries, diff_entries

    C3toolbox.startup()

    form = tkinter.Tk()
    form.wm_title("Song Metadata")
    init_style(form)

    # Make the main window responsive
    form.columnconfigure(0, weight=1)
    form.rowconfigure(0, weight=1)

    # Notebook with two tabs
    notebook = ttk.Notebook(form)
    notebook.grid(row=0, column=0, sticky='nsew', padx=PAD_X, pady=(PAD_Y, 0))

    info_frame = ttk.Frame(notebook)
    diff_frame = ttk.Frame(notebook)
    notebook.add(info_frame, text="Info")
    notebook.add(diff_frame, text="Difficulty")

    # Configure frames
    for f in (info_frame, diff_frame):
        f.columnconfigure(0, weight=0)
        f.columnconfigure(1, weight=1)

    # --- Info Section ---
    info_box = ttk.Labelframe(info_frame, text="Info", style='Section.TLabelframe')
    info_box.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=PAD_X, pady=PAD_Y)
    info_box.columnconfigure(0, weight=0)
    info_box.columnconfigure(1, weight=1)

    meta_entries = {}
    for field in META_FIELDS:
        meta_entries[field] = labeled_entry(info_box, field, width=32)

    add_tooltip(meta_entries.get("Year"), "Numbers only (e.g., 2025)")
    add_tooltip(meta_entries.get("Preview_Start_Time"), "Milliseconds (e.g., 45000 for 45s)")

    # --- Difficulty Section ---
    diff_box = ttk.Labelframe(diff_frame, text="Difficulty", style='Section.TLabelframe')
    diff_box.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=PAD_X, pady=PAD_Y)
    diff_box.columnconfigure(0, weight=0)
    diff_box.columnconfigure(1, weight=1)

    diff_entries = {}
    for field in DIFF_FIELDS:
        diff_entries[field] = labeled_entry(diff_box, field, width=12)

    # --- Button Bar ---
    btn_bar = ttk.Frame(form)
    btn_bar.grid(row=1, column=0, sticky='ew', padx=PAD_X, pady=(PAD_Y, PAD_Y))
    btn_bar.columnconfigure(0, weight=1)  # spacer expands

    ttk.Button(btn_bar, text="Load Defaults", command=on_load_defaults).grid(row=0, column=1, padx=(0, 6))
    ttk.Button(btn_bar, text="Save Defaults", command=on_save_defaults).grid(row=0, column=2, padx=(0, 6))
    ttk.Button(btn_bar, text="Create", command=on_create).grid(row=0, column=3)

    # Hotkeys
    form.bind("<Return>", on_create)
    form.bind("<Control-s>", lambda e: on_save_defaults())
    form.bind("<Control-l>", lambda e: on_load_defaults())

    # Optional banner (under buttons)
    banner_path = os.path.join(sys.path[0], "banner.gif")
    if os.path.exists(banner_path):
        banner = tkinter.PhotoImage(file=banner_path)
        banner_lbl = ttk.Label(form, image=banner)
        banner_lbl.image = banner
        banner_lbl.grid(row=2, column=0, pady=(0, PAD_Y))

    # Auto-load defaults from script folder (if present)
    try:
        load_defaults_into_form(DEFAULTS_PATH)
    except Exception:
        pass

    # Open window center screen
    C3toolbox.center_on_screen(form)
    

if __name__ == "__main__":
    launch()
