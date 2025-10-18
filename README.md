# CAT-YARG
The main idea of this repo is to modify CAT so it accepts CH/YARG exclusive features (Expert+ kick notes, open notes, tap regions etc.) rather than erroring out due to invalid notes. If you chart primarily for RB3, please use [the original](https://github.com/abefacciazzi/CAT) instead.

More info about CAT available [here](https://rhythmgamingworld.com/forums/topic/c3-automation-tools-2/).

## Installation
1. Make sure ReaScript is working:
   - This can be done by installing [Python 2.7](https://www.python.org/downloads/release/python-2718/);
   - Make sure you get the same version as your REAPER install (i.e. if you use the 32-bit version of REAPER, get the 32-bit version of Python 2.7);
   - **In REAPER, go to Options -> Preferences... -> ReaScript, check the "Enable" box, and click OK.** This screen should detect Python, i.e. "Python: python27.dll is installed." If it's not, try restarting REAPER. If it's still not, make sure you got the right version of Python.
   - If you're still encountering issues and you're using 64-bit versions of REAPER/Python 2.7, try using the 32-bit versions instead. It is possible to have both the 32-bit **and** 64-bit versions of REAPER installed at the same time.
2. Download the latest version [here](https://github.com/raphaelgoulart/CAT-YARG/archive/refs/heads/master.zip);
3. Extract it anywhere (recommended folder: `C:\Users\rgces\AppData\Roaming\REAPER\Scripts`);
4. **In REAPER, go to Actions -> Show action list... and click New/load... under ReaScript.** Browse to the main script file from step 2 (CAT.py) and click Open;
5. **Double-click "Custom: CAT.py" in the actions list to run the script.**

## Changes from original version
- Create drums animations
  - [x] Silently ignore Expert+ kicks (note 95) instead of erroring out;
  - [x] For velocity 1 snare notes, auto-generate Snare Rim animation notes instead of Snare Hard (togglable);
- Automatic reductions (drums)
  - [x] Silently ignore Expert+ kicks (note 95) instead of erroring out;
- Automatic reductions (5-lane)
  - [x] Silently ignore tap markers;
  - [x] "Move opens to green" toggle for each difficult (default: off/on/on for H/M/E respectively);
  - [x] Add support for PART GUITAR COOP track;
- Reduce 2x bass pedal
  - [x] Move to note 95 instead of deleting;
- General
  - [x] Add "Guitar Coop" to all 5-lane related functions
  - [ ] Ensure all functions still work even if the charts have non-RB3 features in them;
- Pro Guitar/Bass
  - [ ] (maybe) Add support to PART REAL_GUITAR_COOP and REAL_RHYTHM, **if** those get added to YARG;
- CARV
  - This just hangs in my PC, so I won't be touching that. Sorry!
