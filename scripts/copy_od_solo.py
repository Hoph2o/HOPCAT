from __future__ import absolute_import
from reaper_python import *
import C3toolbox

CAT_LABEL = "Add missing solo/OD to pro"
CAT_CATEGORY = "Pro"
CAT_ORDER = 1

def launch():
    C3toolbox.startup()
    C3toolbox.copy_od_solo()

if __name__ == '__main__':
    launch()
    #C3toolbox.startup()
    #C3toolbox.copy_od_solo()

