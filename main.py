import time
from typing import Any
from pywinauto.application import Application, WindowSpecification
import pywinauto

app: Application = Application("uia").start(
    r"explorer.exe shell:AppsFolder\Microsoft.ZuneMusic_8wekyb3d8bbwe!Microsoft.ZuneMusic"
)
time.sleep(2)
w_handle_list: list = pywinauto.findwindows.find_windows(title="Groove Music", class_name="ApplicationFrameWindow")
while not w_handle_list:
    w_handle_list = pywinauto.findwindows.find_windows(title="Groove Music", class_name="ApplicationFrameWindow")
w_handle: Any = w_handle_list[0]

app.connect(handle=w_handle)

gm: WindowSpecification = app.window(handle=w_handle)

gm.print_control_identifiers()

gm.Recentplays.click_input()
time.sleep(2)
gm.Mymusic.click_input()
# my_music: Any = gm.child_window(title="My music", auto_id="mymusic", control_type="TabItem").wrapper_object()
# my_music.click_input()
gm.Play.click_input()
# gm.print_control_identifiers()
time.sleep(2)
gm.Pause.click_input()
time.sleep(2)
gm.CloseGrooveMusic.click()
print("Done")
