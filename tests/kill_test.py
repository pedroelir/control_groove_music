import time
from src.gmui.gmui_handler import GM_UI
from pywinauto import Desktop, Application
import subprocess
import pytest


@pytest.fixture()
def ensure_start():
    desktop: Desktop = Desktop("uia")
    windows = [win.window_text().strip() for win in desktop.windows(enabled_only=True) if len(win.window_text()) > 0]
    if not ("Groove Music" in windows):
        Application("uia").start(r"explorer.exe shell:AppsFolder\Microsoft.ZuneMusic_8wekyb3d8bbwe!Microsoft.ZuneMusic")
        time.sleep(2)
        windows = [
            win.window_text().strip() for win in desktop.windows(enabled_only=True) if len(win.window_text()) > 0
        ]
        assert "Groove Music" in windows

    yield

    desktop: Desktop = Desktop("uia")
    windows = [win.window_text().strip() for win in desktop.windows(enabled_only=True) if len(win.window_text()) > 0]
    if "Groove Music" in windows:
        subprocess.call("taskkill /im Music.UI.exe /f")
        time.sleep(2)
        windows = [
            win.window_text().strip() for win in desktop.windows(enabled_only=True) if len(win.window_text()) > 0
        ]
        assert not ("Groove Music" in windows)


def test_kill(ensure_start):
    gm: GM_UI = GM_UI()
    gm.kill()
    time.sleep(2)
    desktop: Desktop = Desktop("uia")
    windows = [win.window_text().strip() for win in desktop.windows(enabled_only=True) if len(win.window_text()) > 0]
    assert not ("Groove Music" in windows)


if __name__ == "__main__":
    test_kill()
