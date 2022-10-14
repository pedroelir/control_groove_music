from gmui.gmui_handler import GM_UI


def test_is_running(ensure_start):
    gm: GM_UI = GM_UI()
    assert gm.is_running()
