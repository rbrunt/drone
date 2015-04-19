import os
import shutil
import _winreg

def get_data_path():
	#TODO: makde this platform specific..
	reg_key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r"Software\OpenLP\OpenLP\advanced")
	return _winreg.QueryValueEx(reg_key, "data path")[0]

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

