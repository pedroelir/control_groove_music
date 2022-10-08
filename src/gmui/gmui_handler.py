from pywinauto.application import Application
from pywinauto import Desktop
import subprocess


class GM_UI:
    def __init__(self) -> None:
        self.__title: str = "Groove Music"
        self.__app: Application = None
        self.__process_name: str = "Music.UI.exe"
        self.__start_cmd: str = r"explorer.exe shell:AppsFolder\Microsoft.ZuneMusic_8wekyb3d8bbwe!Microsoft.ZuneMusic"
        self.__backend: str = "uia"

    def start(self) -> None:
        Application(self.__backend).start(self.__start_cmd)

    def kill(self) -> None:
        subprocess.call("taskkill /im Music.UI.exe /f")

    def is_running(self) -> bool:
        desktop: Desktop = Desktop("uia")
        windows: list = [
            win.window_text().strip() for win in desktop.windows(enabled_only=True) if len(win.window_text()) > 0
        ]
        return self.__title in windows
