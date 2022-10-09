import time
from pywinauto import Desktop, Application
import subprocess
import pytest


@pytest.fixture()
def ensure_kill():
    desktop: Desktop = Desktop("uia")
    windows = [win.window_text().strip() for win in desktop.windows(enabled_only=True) if len(win.window_text()) > 0]
    if "Groove Music" in windows:
        subprocess.call("taskkill /im Music.UI.exe /f")
        time.sleep(2)
        windows = [
            win.window_text().strip() for win in desktop.windows(enabled_only=True) if len(win.window_text()) > 0
        ]
        assert not ("Groove Music" in windows)


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


@pytest.fixture(scope="session", autouse=True)
def general_setup_teardown():
    yield
    # kill the process at the oend of all the tests
    desktop: Desktop = Desktop("uia")
    windows = [win.window_text().strip() for win in desktop.windows(enabled_only=True) if len(win.window_text()) > 0]
    if "Groove Music" in windows:
        subprocess.call("taskkill /im Music.UI.exe /f")
        time.sleep(2)
        windows = [
            win.window_text().strip() for win in desktop.windows(enabled_only=True) if len(win.window_text()) > 0
        ]
        assert not ("Groove Music" in windows)
