from __future__ import absolute_import
from reaper_python import *
import C3toolbox

CAT_LABEL = "Remove invalid markers"
CAT_CATEGORY = "System & Supersets"
CAT_ORDER = 1

def launch():
    C3toolbox.startup()
    C3toolbox.filter_notes('')

if __name__ == '__main__':
    launch()
