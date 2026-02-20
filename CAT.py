from __future__ import absolute_import
from reaper_python import *
import os
import sys
import json
import tkinter as Tk
import traceback
sys.argv = ["Main"]

APP_TITLE = "HOPCAT-ROG v0.4"

# ======================================================================
#                     Auto-import tools from ./scripts
# ======================================================================

SCRIPT_DIR = sys.path[0]
SCRIPTS_DIR = os.path.join(SCRIPT_DIR, "scripts")

if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
if os.path.isdir(SCRIPTS_DIR) and SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

def _log_console(msg):
    try:
        RPR_ShowConsoleMsg(str(msg) + "\n")
    except Exception:
        pass

try:
    THIS_BASENAME = os.path.splitext(os.path.basename(__file__))[0]
except Exception:
    THIS_BASENAME = None  # REAPER can omit __file__

def _should_import(module_name, this_basename):
    if not module_name:
        return False
    if this_basename and module_name == this_basename:
        return False
    if module_name.startswith("_"):
        return False
    if module_name in ("reaper_python",):
        return False
    return True

# Import every .py in ./scripts and expose as globals()[basename]
if os.path.isdir(SCRIPTS_DIR):
    for fname in os.listdir(SCRIPTS_DIR):
        if not fname.endswith(".py"):
            continue
        modname = os.path.splitext(fname)[0]
        if not _should_import(modname, THIS_BASENAME):
            continue
        try:
            globals()[modname] = __import__(modname)
        except Exception as e:
            _log_console("Failed to import %s: %s" % (modname, e))
else:
    _log_console("Warning: scripts folder not found at: %s" % SCRIPTS_DIR)

# ======================================================================
#             Dynamic registry: discover tools & categories
# ======================================================================

PINNED_CATEGORY_ORDER = ["System & Supersets", "5-Lane / Drums", "Vocals", "Pro"]

def _collect_tools_from_globals():
    registry = []
    for key, mod in globals().items():
        if not isinstance(key, str) or key.startswith("_"):
            continue
        try:
            has_launch = hasattr(mod, "launch") and callable(getattr(mod, "launch"))
        except Exception:
            has_launch = False
        if not has_launch:
            continue

        # Expect scripts to declare these; provide safe fallbacks to avoid crashes.
        label    = getattr(mod, "CAT_LABEL", key)
        category = getattr(mod, "CAT_CATEGORY", "Misc")
        order    = getattr(mod, "CAT_ORDER", 9999)

        registry.append({
            "key": key,
            "label": label,
            "category": category,
            "order": order,
            "module": mod,
        })
    return registry

def _build_categories(registry):
    category = {}
    func_index = {}

    for item in registry:
        category.setdefault(item["category"], []).append((item["label"], item["key"]))
        func_index[item["key"]] = item["label"]

    # sort items in each category: CAT_ORDER then label
    for cat, items in category.items():
        order_map = dict((i["key"], i["order"]) for i in registry if i["category"] == cat)
        category[cat] = sorted(items, key=lambda t: (order_map.get(t[1], 9999), t[0].lower()))

    # category ordering
    present = set(category.keys())
    ordered = ["Favorites"]
    for pin in PINNED_CATEGORY_ORDER:
        if pin in present:
            ordered.append(pin)
            present.remove(pin)
    for cat in sorted(present, key=lambda s: s.lower()):
        ordered.append(cat)

    return category, func_index, ordered

# Build the dynamic registry now
_TOOL_REGISTRY = _collect_tools_from_globals()
BASE_CATEGORIES, FUNC_INDEX, CATEGORY_ORDER = _build_categories(_TOOL_REGISTRY)

# ======================================================================
#                      Favorites persistence (JSON)
# ======================================================================

FAV_FILE = os.path.join(sys.path[0], "CAT_favorites.json")

def load_favorites():
    try:
        if os.path.exists(FAV_FILE):
            with open(FAV_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return set([k for k in data if k in FUNC_INDEX])
    except Exception:
        pass
    return set()

def save_favorites(favs_set):
    try:
        with open(FAV_FILE, "w", encoding="utf-8") as f:
            json.dump(sorted(list(favs_set)), f, indent=2)
    except Exception:
        pass

# ======================================================================
#                          Generic tool runner
# ======================================================================

def run_5lane():
    mod = globals().get("reduce_5lane")
    if hasattr(mod, "launch") and callable(getattr(mod, "launch")):
        globals()["reduce_5lane"].launch("5LANE")
    return mod

# Tools that require custom args or a special call path
SPECIAL_RUNNERS = {
    "reduce_5lane": run_5lane,
}

running_mod = None

def run_tool(func_key):
    global running_mod
    # 1) Special-case tools that need parameters or wrappers
    special = SPECIAL_RUNNERS.get(func_key)
    if special:
        try:
            running_mod = special()
        except Exception as e:
            _log_console("Error running special tool %s: %s" % (func_key, e))
        return

    # 2) Default: module with launch()
    mod = globals().get(func_key)
    if hasattr(mod, "launch") and callable(getattr(mod, "launch")):
        try:
            running_mod = mod
            mod.launch()
        except Exception as e:
            _log_console("Error running %s: %s" % (func_key, traceback.format_exc()))
        return

    # 3) Allow calling local helper functions by name (if any)
    func = globals().get(func_key)
    if callable(func):
        try:
            func()
        except Exception as e:
            _log_console("Error running %s(): %s" % (func_key, e))
        return

    _log_console("Tool not found: %s" % func_key)

def make_run_handler(app, func_key):
    """Close the menu first, then run the tool (prevents Tk image/state issues)."""
    def _cb():
        try:
            app.root.destroy()
        except Exception:
            pass
        run_tool(func_key)
    return _cb

# ======================================================================
#                                 UI
# ======================================================================

STAR_FILLED = u"\u2605"
STAR_EMPTY  = u"\u2606"
try:
    STAR_FILLED.encode("utf-8"); STAR_EMPTY.encode("utf-8")
except Exception:
    STAR_FILLED = "*"; STAR_EMPTY = " "

class CATUI(object):
    def __init__(self):
        # ---- Root setup ----
        self.root = Tk.Tk()
        self.root.wm_title(APP_TITLE)
        try:
            self.root.iconbitmap(default="")
        except Exception:
            pass

        self.favorites = load_favorites()
        self.root.grid_rowconfigure(2, weight=1)

        # ---- Main area: left sidebar + right button grid ----
        main = Tk.Frame(self.root, padx=8, pady=8)
        main.grid(row=2, column=0, sticky="nsew")
        main.grid_columnconfigure(0, weight=0)  # sidebar
        main.grid_columnconfigure(1, weight=1)  # button grid
        main.grid_rowconfigure(0, weight=1)

        # Sidebar (categories)
        left = Tk.Frame(main, padx=6)
        left.grid(row=0, column=0, sticky="ns")
        Tk.Label(left, text="Categories", font=("Arial", 10, "bold")).pack(anchor="w")

        self.cat_list = Tk.Listbox(left, height=12, exportselection=False)
        self.cat_scroll = Tk.Scrollbar(left, orient="vertical", command=self.cat_list.yview)
        self.cat_list.configure(yscrollcommand=self.cat_scroll.set)
        self.cat_list.pack(side="left", fill="y")
        self.cat_scroll.pack(side="left", fill="y")

        # Populate sidebar: Favorites first, then the discovered categories in order
        for name in (["Favorites"] + [c for c in CATEGORY_ORDER if c != "Favorites"]):
            self.cat_list.insert("end", name)

        self.cat_list.bind("<<ListboxSelect>>", self.on_category_changed)

        # Button grid (3 columns, stretch to fill)
        self.button_frame = Tk.Frame(main)
        self.button_frame.grid(row=0, column=1, sticky="nsew")
        for c in range(3):
            self.button_frame.grid_columnconfigure(c, weight=1)

        self.current_category = None
        self.all_btns = []  # (btn_widget, label, func_key)

        # Default selection = Favorites
        if self.cat_list.size() > 0:
            self.cat_list.selection_set(0)
            self.on_category_changed()

        # Size + center on screen
        self._center_on_screen(900, 300)

        # Esc to close quickly
        self.root.bind("<Escape>", lambda e: self.root.destroy())

    # ---------- Window helpers ----------
    def _center_on_screen(self, w, h):
        try:
            self.root.geometry("%dx%d+0+0" % (w, h))
            self.root.update_idletasks()
            sw = self.root.winfo_screenwidth()
            sh = self.root.winfo_screenheight()
            x = int((sw - w) / 2)
            y = int((sh - h) / 2)
            self.root.geometry("%dx%d+%d+%d" % (w, h, x, y))
        except Exception:
            pass

    # ---------- Favorites helpers ----------
    def is_fav(self, func_key):
        return func_key in self.favorites

    def toggle_favorite(self, func_key):
        if func_key in self.favorites:
            self.favorites.remove(func_key)
        else:
            self.favorites.add(func_key)
        save_favorites(self.favorites)
        self._refresh_stars()
        if self.current_category == "Favorites":
            self._show_buttons_for("Favorites")

    def _decorate(self, label, key):
        return (STAR_FILLED + " " if self.is_fav(key) else STAR_EMPTY + " ") + label

    def _refresh_stars(self):
        for btn, label, key in self.all_btns:
            btn.configure(text=self._decorate(label, key))

    # ---------- Category handling ----------
    def on_category_changed(self, event=None):
        sel = self._get_selected()
        if sel != self.current_category:
            self.current_category = sel
            self._show_buttons_for(sel)

    def _get_selected(self):
        try:
            idx = self.cat_list.curselection()
            return self.cat_list.get(int(idx[0])) if idx else None
        except Exception:
            return None

    def _clear_buttons(self):
        for w in self.button_frame.winfo_children():
            w.destroy()
        self.all_btns = []

    def _favorites_list(self):
        out = []
        for fk in self.favorites:
            if fk in FUNC_INDEX:
                out.append((FUNC_INDEX[fk], fk))
        out.sort(key=lambda x: x[0].lower())
        return out

    def _add_action_button(self, row, col, label, key):
        txt = self._decorate(label, key)
        btn = Tk.Button(self.button_frame, text=txt, width=30, padx=6, pady=6,
                        command=make_run_handler(self, key))
        btn.bind("<Button-3>", lambda e, fk=key: self.toggle_favorite(fk))
        btn.grid(row=row, column=col, padx=4, pady=4, sticky="ew")
        self.all_btns.append((btn, label, key))

    def _show_buttons_for(self, category):
        self._clear_buttons()

        if category == "Favorites":
            actions = self._favorites_list()
            if not actions:
                Tk.Label(self.button_frame,
                         text="No favorites yet. Right-click a button to add one.",
                         fg="#666").grid(row=0, column=0, sticky="w", padx=4, pady=6, columnspan=3)
                return
        else:
            actions = BASE_CATEGORIES.get(category, [])

        COLS = 3
        r = c = 0
        for label, key in actions:
            self._add_action_button(r, c, label, key)
            c += 1
            if c >= COLS:
                c = 0
                r += 1

        for cidx in range(COLS):
            self.button_frame.grid_columnconfigure(cidx, weight=1)

    def run(self):
        global running_mod
        w = self.root
        if running_mod:
            w = running_mod.form
        w.update()
    
    def alive(self):
        global running_mod
        w = self.root
        if running_mod:
            w = running_mod.form
        try:
            return w.winfo_exists()
        except Exception:
            # will happen if the application exits
            return False

    def exit(self):
        global running_mod
        w = self.root
        if running_mod:
            w = running_mod.form
        w.destroy()

# Entry point
if __name__ == "__main__":
    ui = CATUI()
    def run():
        ui.run()
        if ui.alive():
            RPR_defer("run()")
    RPR_defer("run()")
    RPR_atexit("ui.exit()")