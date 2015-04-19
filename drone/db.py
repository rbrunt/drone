import os
import sys
import shutil

def get_data_path():
	if sys.platform == "win32":
		import _winreg
		reg_key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r"Software\OpenLP\OpenLP\advanced")
		return _winreg.QueryValueEx(reg_key, "data path")[0]
	else:
		#TODO: makde this platform specific...
		exit("Drone currently only works on Windows!")

def get_songs_directory():
	return os.path.join(data_path, "songs")

def get_songs_db_path():
	return os.path.join(get_songs_directory(), "songs.sqlite")

def backup_db():
	shutil.copy(get_songs_db_path(), os.path.join(get_songs_directory(), "songs.sqlite.dronebackup"))

def restore_backup():
	shutil.move(os.path.join(get_songs_directory(), "songs.sqlite.dronebackup"), get_songs_db_path())

#On import, set the data_path variable.
data_path = get_data_path()

