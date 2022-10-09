import time
from src.gmui.gmui_handler import GM_UI
from pywinauto import Desktop


def test_kill(ensure_start):
    gm: GM_UI = GM_UI()
    gm.kill()
    time.sleep(2)
    desktop: Desktop = Desktop("uia")
    windows = [win.window_text().strip() for win in desktop.windows(enabled_only=True) if len(win.window_text()) > 0]
    assert not ("Groove Music" in windows)


if __name__ == "__main__":
    test_kill()
