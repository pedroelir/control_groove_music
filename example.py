import time
from gmui.gmui_handler import GM_UI

gm: GM_UI = GM_UI()
gm.start()
time.sleep(1)
gm.connect()
time.sleep(1)
# gm.window.print_control_identifiers()
gm.play_single_media("sample.mp3", media_name="Time")
time.sleep(5)
gm.play_single_media("05 - All I Want For Christmas Is You.mp3")
time.sleep(1)
gm.kill()
