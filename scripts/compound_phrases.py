from __future__ import absolute_import
from reaper_python import *
import C3toolbox

CAT_LABEL = "Compact phrases"
CAT_CATEGORY = "Vocals"
CAT_ORDER = 1

def launch():
    C3toolbox.startup()
    C3toolbox.compact_phrases()

if __name__ == '__main__':
    launch()
