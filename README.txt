Scope on a Rope prototype

Files:
- main.py
- requirements.txt

Setup on Windows
1. Put these files in a folder, for example:
   C:\Users\joe\verify_scope01\scope_on_rope

2. Put your looping background video in the same folder and name it:
   background.mp4

3. Open Command Prompt in that folder.

4. Create and activate a virtual environment:
   py -3.12 -m venv venv
   venv\Scripts\activate

5. Install requirements:
   pip install -r requirements.txt

6. Run:
   python main.py

Notes
- If the microscope is not found, change CAMERA_INDEX in main.py from 0 to 1 or 2.
- If you want a window for debugging instead of fullscreen, set FULLSCREEN = False.
- Change MICROSCOPE_RECT to move/resize the microscope overlay.
- Current default display is portrait 1080 x 1920.
