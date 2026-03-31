Scope on a Rope

Files:
- main.py
- requirements.txt

Setup on Windows
* Put these files in a folder, for example:
  C:\Users\Scope\scopeOnARope

* Put your looping background video in the same folder and name it:
  background.mp4

* python -m venv venv
  
* venv\Scripts\activate

* python -m pip install --upgrade pip

* pip install -r requirements.txt

* Run:
  python main.py

* to start Scope on a Rope at startup, create a link to startScope.bat in the startup folder
  on Windows 
  open a run window with Windows + R
  execute shell:startup
  in the startup directory, create a shortcut to the startScope.bat script

Notes
- If the microscope is not found, change CAMERA_INDEX in main.py from 0 to 1 or 2.
- If you want a window for debugging instead of fullscreen, set FULLSCREEN = False.
- Change MICROSCOPE_RECT to move/resize the microscope overlay.
- Current default display is portrait 1080 x 1920.
