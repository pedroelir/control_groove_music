from pathlib import Path
import time
from typing import Any
import pywinauto
from pywinauto.application import Application, WindowSpecification
from pywinauto import Desktop
import pywinauto.mouse


# CURRENT_DIR = os.path.abspath(os.path.curdir)
CURRENT_DIR = Path.cwd()
dirname = CURRENT_DIR.name

desktop = Desktop("uia")
windows = [win.window_text().strip() for win in desktop.windows(enabled_only=True) if len(win.window_text()) > 0]
app: Application = Application("uia").start(
    r"explorer.exe shell:AppsFolder\Microsoft.ZuneMusic_8wekyb3d8bbwe!Microsoft.ZuneMusic"
)
time.sleep(2)
w_handle_list: list = pywinauto.findwindows.find_windows(title="Groove Music", class_name="ApplicationFrameWindow")
w_handle = pywinauto.findwindows.find_window(title="Groove Music", visible_only=False)
while not w_handle:
    w_handle = pywinauto.findwindows.find_window(title="Groove Music", visible_only=False)

app.connect(handle=w_handle)

gm: WindowSpecification = app.window(handle=w_handle)
gm.descendants()
gm.children()
gm.find_element()

# gm.print_control_identifiers()

gm.Recentplays.click_input()
time.sleep(2)
gm.Mymusic.click_input()
# my_music: Any = gm.child_window(title="My music", auto_id="mymusic", control_type="TabItem").wrapper_object()
# my_music.click_input()
add_folder: Any = gm.child_window(
    title="Not finding everything?, Show us where to look for music, ",
    auto_id="NotificationBannerButton",
    control_type="Button",
)
add_folder.click_input()
time.sleep(1)
add_dir = gm.child_window(title="Add folder", control_type="ListItem")
add_dir.click_input()
time.sleep(1)
# gm.print_control_identifiers()
folder_edit = gm.child_window(title="Folder:", auto_id="1152", control_type="Edit")
folder_edit.type_keys(CURRENT_DIR)
add_folder_button = gm.child_window(title="Add this folder to Music", auto_id="1", control_type="Button")
time.sleep(1)
gm.AddthisfoldertoMusic.click_input()
# add_this_folder_button = gm.child_window(title="Add this folder to Music", auto_id="1", control_type="Button")
# add_this_folder_button.click_input()

time.sleep(1)
gm.Done.click_input()
time.sleep(4)
add_folder.click_input()
folder_item = gm.child_window(
    title=f"{dirname}, {CURRENT_DIR}, Activate to remove folder",
    control_type="ListItem",
)
folder_item.set_focus()
time.sleep(3)
folder_item.click_input()
time.sleep(1)
folder_item.click_input()
# gm.control_groove_music.click_input()
time.sleep(1)
gm.RemoveFolder.click_input()
time.sleep(1)
gm.Done.click_input()
time.sleep(1)
gm.Play.click_input()
# gm.print_control_identifiers()
time.sleep(2)
gm.Pause.click_input()
time.sleep(2)
gm.CloseGrooveMusic.click()
print("Done")
