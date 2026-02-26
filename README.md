# HOPCAT v0.4
This fork was created to further add to CAT and the work done with CAT-YARG

https://github.com/abefacciazzi/CAT

https://github.com/raphaelgoulart/CAT-YARG

Thank you to sanjay for converting CAT to python3 and fixing all my bugs :)

# New Features
- create_ini - A Moonscraper-esque metadate input window to generate a song.ini file directly from REAPER.
- midi_note_selector - Based off a ReaPack script by Lokasenna. Replaces CAT function like "Reduce 2x" and "Reduce to triple hits"
- New UI - Complete overhaul with favorites page and QOL features
- Additional track name compatibility (see below)

# Installation
- Install python 3 (https://www.python.org/downloads/)
- Enable ReaScript in REAPER (Options>Preferences>ReaScript)
- Unlike python 2, you'll probably need to manually point REAPER to your python folder
- Custom path to python dll directory: should be located at **AppData\Local\Programs\Python\Python314** (or whatever version of python you install)
- Force ReaScript to use specific python .dll: **python314** (there's also a file named python3. make sure you're using the file "python + version number")
- You should see "Python: python314.dll is installed" if successful
- Go to Actions>Show action list>New action>Load ReaScript
- Navigate to your HOPCAT folder and select "CAT.py"
- Run "CAT.py" in REAPER

# Important Notes
CAT is REALLY old and expects you to use "proper" track names. I have included a folder of some templates you can use 
that work with CAT. IF THERE IS NO EVENTS TRACK EVERYTHING BREAKS. Below is a complete list of acceptable track names:

- PART BASS *or* BASS
- PART DRUMS *or* DRUMS
- ~~PART DRUMS 2X *or* PART DRUMS 2x *or* PART DRUMS_2x *or* PART DRUMS_2X~~ (don't use this. 2x is supported directly
on the drum track now as note 95)
- PART GUITAR *or* GUITAR
- PART VOCALS *or* VOCALS
- PART KEYS *or* KEYS
- PART REAL_KEYS_X *or* KEYS_X
- PART REAL_KEYS_H *or* KEYS_H
- PART REAL_KEYS_M *or* KEYS_M
- PART REAL_KEYS_E *or* KEYS_E
- PART KEYS_ANIM_RH
- PART KEYS_ANIM_LH
- PART HARM1 *or* HARM1
- PART HARM2 *or* HARM2
- PART HARM3 *or* HARM3
- PART REAL_GUITAR
- PART REAL_GUITAR_22
- PART REAL_BASS
- PART REAL_BASS_22
- PART RHYTHM *or* RHYTHM
- PART GUITAR COOP
- EVENTS
- BEAT
- VENUE
