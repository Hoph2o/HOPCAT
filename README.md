# HOPCAT
This fork was created to further add to CAT and the work done with CAT-YARG

https://github.com/abefacciazzi/CAT

https://github.com/raphaelgoulart/CAT-YARG

# New Features
create_ini - A Moonscraper-esque metadate input window to generate a song.ini file directly from REAPER.
Additional track name compatibility (see below)

# Installation
- Install python 2.7.12 (https://www.python.org/downloads/release/python-2712/)
- Enable ReaScript in REAPER (Options>Preferences>ReaScript)
- In this window you should see "Python: python27.dll is installed"
- Go to Actions>Show action list>New action>Load ReaScript
- Navigate to you HOPCAT folder and select "CAT.py"
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
- PART RHYTHM
- PART GUITAR COOP
- EVENTS
- BEAT
- VENUE
