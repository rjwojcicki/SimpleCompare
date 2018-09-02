from fman import show_alert, OK, CANCEL, show_file_open_dialog, PLATFORM, \
 load_json, save_json, PLATFORM
from subprocess import Popen
from core.os_ import get_popen_kwargs_for_opening
from os.path import exists, splitdrive
import os
import sys
import json

_COMPAISON_TOOL_KEY = "comparisonTool"
_SETTINGS_FILE = "Simple Compare Settings.json"
_PLATFORM_APPLICATIONS_FILTER = {
    'Mac': 'Applications (*.app)',
    'Windows': 'Applications (*.exe)',
    'Linux': 'Applications (*)'
}

class Settings:
    def get_comparison_tool(self):
        tool = self._load_comparison_tool()
        if tool:
            return tool
        tool = self._ask_for_comaparison_tool()
        if not tool:
            return None
        self._save_comparison_tool(tool)
        return tool

    def _load_comparison_tool(self) -> str:
        settings = load_json(_SETTINGS_FILE, default={})
        return settings.get(_COMPAISON_TOOL_KEY, None)

    def _save_comparison_tool(self, tool_path: str):
        save_json(_SETTINGS_FILE, {_COMPAISON_TOOL_KEY: tool_path})

    def _ask_for_comaparison_tool(self):
        can_configure = self._can_configure_now()
        if not (can_configure):
            return None
        return self._pick_comparison_tool()

    def _can_configure_now(self) -> bool:
        choice = show_alert(
            """Comparison tool is currently not configured. Please pick one.
Use tools like KDiff3, DiffMerge, Beyond Compare, etc""",
            OK | CANCEL, OK
        )
        return choice & OK

    def _pick_comparison_tool(self) -> str:
        tool_path = show_file_open_dialog(
            'Pick a comparison tool', self._get_applications_directory(),
            _PLATFORM_APPLICATIONS_FILTER[PLATFORM]
        )
        return tool_path

    def _get_applications_directory(self) -> str:
        if PLATFORM == 'Mac':
            return '/Applications'
        elif PLATFORM == 'Windows':
            result = os.environ["ProgramW6432"]
            if not result or not exists(result):
                result = os.environ["ProgramFiles"]
            if not exists(result):
                result = splitdrive(sys.executable)[0] + '\\'
            return result
        elif PLATFORM == 'Linux':
            return '/usr/bin'
        raise RuntimeError("Not supported platform: '" + PLATFORM + \
            "'. Supported platforms are 'Mac', 'Windows' and 'Linux'")
