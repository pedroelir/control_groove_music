from pathlib import Path
import time
from typing import Dict, List, Union
from pywinauto.application import Application
from pywinauto.base_wrapper import BaseWrapper
from pywinauto import Desktop, findwindows, WindowSpecification
import subprocess

choose_folder_criteria: Dict[str, str] = {
    "title": "Not finding everything?, Show us where to look for music, ",
    "auto_id": "NotificationBannerButton",
    "control_type": "Button",
}
songs_submenu_criteria: Dict[str, str] = {"title_re": "Songs", "control_type": "ListItem"}
artists_submenu_criteria: Dict[str, str] = {
    "title_re": "Artists",
    "control_type": "ListItem",
}
albums_submenu_criteria: Dict[str, str] = {
    "title_re": "Albums",
    "control_type": "ListItem",
}

addfolder_add_button_criteria: Dict[str, str] = {"title": "Add folder", "control_type": "ListItem"}
addfolder_done_button_criteria: Dict[str, str] = {
    "title": "Done",
    "auto_id": "PrimaryButton",
    "control_type": "Button",
}

addfolderw_folder_textbox_criteria: Dict[str, str] = {
    "title": "Folder:",
    "auto_id": "1152",
    "control_type": "Edit",
}
addfolderw_addthisfolder_button_criteria: Dict[str, str] = {
    "title": "Add this folder to Music",
    "auto_id": "1",
    "control_type": "Button",
}

songlist_crtieria: Dict[str, str] = {"title": "MY MUSIC", "auto_id": "SongsList", "control_type": "List"}

mute_button_criteria: Dict[str, str] = {
    "title_re": "Mute",
    "auto_id": "Command_ToggleMute",
    "control_type": "Button",
}
repeat_button_criteria: Dict[str, str] = {
    "title_re": "Repeat",
    "auto_id": "Command_ToggleRepeat",
    "control_type": "Button",
}
play_button_criteria: Dict[str, str] = {"title": "Play", "auto_id": "Command_Play", "control_type": "Button"}
pause_button_criteria: Dict[str, str] = {"title": "Pause", "auto_id": "Command_Pause", "control_type": "Button"}
nowplaying_button_criteria: Dict[str, str] = {
    # "title_re": "Now playing",
    "auto_id": "NavigateToNowPlayingPageButton",
    "control_type": "Button",
}


class GM_UI:
    def __init__(self) -> None:
        self.__title: str = "Groove Music"
        self.__app: Application = None
        self.__process_name: str = "Music.UI.exe"
        self.__start_cmd: str = r"explorer.exe shell:AppsFolder\Microsoft.ZuneMusic_8wekyb3d8bbwe!Microsoft.ZuneMusic"
        self.__backend: str = "uia"

    def start(self) -> None:
        self.__app = Application(self.__backend).start(self.__start_cmd)

    def kill(self) -> None:
        subprocess.call("taskkill /im Music.UI.exe /f")

    def is_running(self) -> bool:
        desktop: Desktop = Desktop("uia")
        windows: list = [
            win.window_text().strip() for win in desktop.windows(enabled_only=True) if len(win.window_text()) > 0
        ]
        return self.__title in windows

    def connect(self) -> None:
        # w_handle_list: list = findwindows.find_windows(title="Groove Music", class_name="ApplicationFrameWindow")
        try:
            w_handle = findwindows.find_window(title=self.__title, visible_only=False)
            while not w_handle:
                w_handle = findwindows.find_window(title=self.__title, visible_only=False)
        except findwindows.WindowAmbiguousError:
            w_handle = findwindows.find_windows(title=self.__title, visible_only=False)[0]

        self.__app.connect(handle=w_handle)
        self.window: WindowSpecification = self.__app.window(handle=w_handle)

    def play_single_media(self, media_path: Union[str, Path], media_name: str = None) -> None:
        if type(media_path) == str:
            media_path: Path = Path(media_path)

        self.window.child_window(**choose_folder_criteria).click_input()

        self.window.child_window(**addfolder_add_button_criteria).click_input()

        self.window.child_window(**addfolderw_folder_textbox_criteria).type_keys(media_path.parent.absolute())

        self.window.child_window(**addfolderw_addthisfolder_button_criteria).click_input()

        time.sleep(1)
        self.window.child_window(**addfolder_done_button_criteria).click_input()

        # Rotate through Artis/Album/Songs to ensure refresh
        self.window.child_window(**artists_submenu_criteria).click_input()
        self.window.child_window(**albums_submenu_criteria).click_input()
        self.window.child_window(**songs_submenu_criteria).click_input()

        # get song list
        songlist_parent: BaseWrapper = self.window.child_window(**songlist_crtieria).wrapper_object()

        songlist_descendants: List[BaseWrapper] = songlist_parent.descendants()
        songsdescendants: List[str] = [
            element.element_info.name
            for element in songlist_descendants
            if element.element_info.automation_id == "Title"
            and element.element_info.name
            not in [
                "Not finding everything?",
                "Songs",
                "Artists",
                "Albums",
            ]
        ]
        print(f"{songsdescendants=}")

        songs_list: List[BaseWrapper] = songlist_parent.iter_children()
        songs: List[str] = []
        for child in songs_list:
            if child.element_info.control_type == "ListItem":
                songs.append(child.children()[0].element_info.name)
                # for grandchild in child.children():
                #     if grandchild.element_info.automation_id == "Title":
                #         songchildren.append(grandchild.element_info.name)

        print(f"{songs_list=}")
        print(f"{songs=}")

        def get_best_match(candidates: List[str], reference: str, threshold: float = 0.5) -> str:
            from difflib import SequenceMatcher

            if len(candidates) == 0:
                return ""
            if len(candidates) == 1:
                return candidates[0]

            best_ratio: float = threshold
            best_match: str = ""
            print(f"finding best match for {reference}")
            for candidate in candidates:
                cadidate_ratio: float = SequenceMatcher(a=candidate, b=reference).ratio()
                print(f"{candidate} ratio: {cadidate_ratio}")
                if cadidate_ratio > best_ratio:
                    best_match, best_ratio = candidate, cadidate_ratio

            return best_match

        reference: str = media_name if media_name is not None else media_path.stem
        song_title: str = get_best_match(songs, reference)

        song_text_criteria: Dict[str, str] = {"title": song_title, "control_type": "Text"}
        playall_button_criterria: Dict[str, str] = {
            "title": "Play all",
            "auto_id": "Command_PlayCommand",
            "control_type": "Button",
        }
        try:
            if song_title not in ["Select", ""]:
                # if song titile not found or is "select, the song might have focus already"
                print(f"Best match found {song_title}")
                self.window.child_window(**song_text_criteria).click_input()
            else:
                print(f"No Best match found for {reference}, the song might be already selected")
            print("Trying to press play")
            self.window.child_window(**playall_button_criterria).click_input()
        except findwindows.ElementNotFoundError:
            print("cannot play Title")
            return False

        # time.sleep(1)
        # self.window.child_window(**nowplaying_button_criteria).click_input()
        time.sleep(1)
        self.window.child_window(**pause_button_criteria).click_input()
        time.sleep(1)
        self.window.child_window(**play_button_criteria).click_input()
        time.sleep(1)
        self.window.child_window(**repeat_button_criteria).click_input()
        time.sleep(1)
        self.window.child_window(**mute_button_criteria).click_input()
        time.sleep(1)
        self.window.child_window(**repeat_button_criteria).click_input()
        time.sleep(1)
        self.window.child_window(**mute_button_criteria).click_input()
        return self.is_playing

    def is_playing(self) -> bool:
        try:
            self.window.child_window(**play_button_criteria)
            return False
        except findwindows.ElementNotFoundError:
            return True

    def is_paused(self) -> bool:
        try:
            self.window.child_window(**pause_button_criteria)
            return False
        except findwindows.ElementNotFoundError:
            return True
