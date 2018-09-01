from fman import DirectoryPaneCommand, show_alert, load_json, OK, CANCEL
from fman.url import as_human_readable
import subprocess
from .settings import Settings

savedToCompare = ""
settings = Settings()

class SaveToCompare(DirectoryPaneCommand):	
	def __call__(self):
		global savedToCompare
		files = self.get_chosen_files()
		selectedFile = files[0]
		savedToCompare = as_human_readable(selectedFile)

	def is_visible(self):
		files = self.get_chosen_files()
		return len(files) == 1

class CompareWithSaved(DirectoryPaneCommand):
	def __call__(self):

		global savedToCompare
		selectedFile = as_human_readable(self.get_chosen_files()[0])
		subprocess.call([settings.get_comparison_tool(), savedToCompare, selectedFile])
		pass

	def is_visible(self):
		global savedToCompare
		return savedToCompare != "" and len(self.get_chosen_files()) == 1


class CompareFiles(DirectoryPaneCommand):
	def __call__(self):
		global savedToCompare
		selectedFile1 = as_human_readable(self.get_chosen_files()[0])
		selectedFile2 = as_human_readable(self.get_chosen_files()[1])
		subprocess.call([settings.get_comparison_tool(), selectedFile1, selectedFile2])
		pass

	def is_visible(self):
		return len(self.get_chosen_files()) == 2