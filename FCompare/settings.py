from fman import show_alert, OK, CANCEL, show_file_open_dialog, PLATFORM, \
 load_json, save_json, PLATFORM
from subprocess import Popen
from core.os_ import get_popen_kwargs_for_opening
from os.path import exists, splitdrive
import os
import sys
import json

_COMPAISON_TOOL_KEY = "comparisonTool"
_SETTINGS_FILE = "Comparison Settings.json"

class Settings:
    settings = {}
    _PLATFORM_APPLICATIONS_FILTER = {
        'Mac': 'Applications (*.app)',
        'Windows': 'Applications (*.exe)',
        'Linux': 'Applications (*)'
    }

    def get_comparison_tool(self):
        self._ensure_comparison_tool_is_chosen()
        return self.settings.get(_COMPAISON_TOOL_KEY, None)

    def _ensure_comparison_tool_is_chosen(self):
        self.settings = load_json(_SETTINGS_FILE, default={})
        comparisonTool = self.settings.get(_COMPAISON_TOOL_KEY, None)
        if not comparisonTool:
            self._ask_for_comaparison_tool()

    def _ask_for_comaparison_tool(self):
        choice = show_alert(
            'Comparison tool is currently not configured. Please pick one.',
            OK | CANCEL, OK
        )
        if choice & OK:
            viewer_path = show_file_open_dialog(
                'Pick a comparison tool', self._get_applications_directory(),
                self._PLATFORM_APPLICATIONS_FILTER[PLATFORM]
            )   
            if viewer_path:
                # viewer = get_popen_kwargs_for_opening('{file}', viewer_path)
                self.settings[_COMPAISON_TOOL_KEY] = viewer_path
                save_json(_SETTINGS_FILE, self.settings)    

    def _get_applications_directory(self):
        if PLATFORM == 'Mac':
            return '/Applications'
        elif PLATFORM == 'Windows':
            result = os.environ["ProgramW6432"]
            if not result:
                result = os.environ["ProgramFiles"]
            if not exists(result):
                result = splitdrive(sys.executable)[0] + '\\'
            return result
        elif PLATFORM == 'Linux':
            return '/usr/bin'
        raise NotImplementedError(PLATFORM)