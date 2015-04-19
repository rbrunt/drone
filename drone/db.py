import os
import _winreg

def get_data_path():
	#TODO: makde this platform specific..
	reg_key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r"Software\OpenLP\OpenLP\advanced")
	return _winreg.QueryValueEx(reg_key, "data path")[0]

def get_songs_db_path():
	return os.path.join(data_path, "songs", "songs.sqlite")

#On import, set the data_path variable.
data_path = get_data_path()

