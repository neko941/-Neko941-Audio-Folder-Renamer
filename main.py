from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.wavpack import WavPack
from mutagen.wave import WAVE
from mutagen.dsf import DSF
from mutagen.dsdiff import DSDIFF
from mutagen.aiff import AIFF
import pythoncom
from win32com.shell import shell, shellcon
import pathlib
import glob
import os
import sys
import shutil
import array

"""Container"""
folderDataList = []
specialCharacters = [":", "?", "/", '"']
audioExtension = {
    "flac": FLAC,
    "wav": WAVE,
    "wv": WavPack,
    "dsf": DSF,
    "dff": DSDIFF,
    "aiff": AIFF
}

"""Create Error Folder"""
if not os.path.exists("[00] Error"):
	os.mkdir("[00] Error")
if not os.path.exists("[00] Error/[00] Diiferent Extensions"):
	os.mkdir("[00] Error/[00] Diiferent Extensions")
error_diff_extensions_path = "[00] Error/[00] Diiferent Extensions"
if not os.path.exists("[00] Error/[01] Special Character"):
	os.mkdir("[00] Error/[01] Special Character")
error_special_character_path = "[00] Error/[01] Special Character"
if not os.path.exists("[00] Error/[02] Cannot Check ABLUM"):
	os.mkdir("[00] Error/[02] Cannot Check ABLUM")
error_album_check = "[00] Error/[02] Cannot Check ABLUM"
if not os.path.exists("[00] Error/[03] Unkown"):
	os.mkdir("[00] Error/[03] Unkown")
error_unknown_path = "[00] Error/[03] Unkown"

def checkNumber(num):
	"""Fix the Sample Rate"""
	if (num - int(num) == 0):
		return int(num)
	return num

def deleteDesktopIni():
	"""Delete All file desktop.ini"""
	for root, directories, files in os.walk(os.getcwd()):
		for file in files:
			if file == "desktop.ini": 
				os.remove(os.path.join(root, file))

def internetShorcut(path):
	shortcut = pythoncom.CoCreateInstance (
	  shell.CLSID_InternetShortcut,
	  None,
	  pythoncom.CLSCTX_INPROC_SERVER,
	  shell.IID_IUniformResourceLocator
	)
	shortcut.SetURL("http://bit.ly/neko941")
	persist_file = shortcut.QueryInterface (pythoncom.IID_IPersistFile)
	persist_file.Save(os.path.join (path,"Neko941's Hi-res Collection.url"), 0)


def getFolderData():
	"""Get Folder Data"""
	for subFolder in glob.glob("*/"):
		if subFolder[:-1] == "[00] Error":
			continue
		else:
			internetShorcut(os.path.abspath(subFolder))
			extensionsInFolder = []
			qualitiesInFolder = []
			for root, directories, files in os.walk(subFolder):
				for file in files:
					extension = os.path.splitext(file)[1][1:]
					if extension in audioExtension.keys():
						if extension not in extensionsInFolder:
							extensionsInFolder.append(extension)

						audio = audioExtension[extension](os.path.join(root, file))
						bitsPerSample = audio.info.bits_per_sample
						sampleRate = checkNumber(audio.info.sample_rate/1000)
						quality = f"{bitsPerSample}-{sampleRate}"
						if quality not in qualitiesInFolder:
							qualitiesInFolder.append(quality)

		qualitiesInFolder.sort()

		if len(extensionsInFolder) != 1:
			shutil.move(subFolder, error_diff_extensions_path)
		else:
			folderData = {
			"folderName" : subFolder[:-1],
			"audioExtension" : extensionsInFolder[0], 
			"audioQuality" : qualitiesInFolder,
			"audioChannels" : audio.info.channels,
			"album" : audio.get("ALBUM"),
			"artist" : audio.get("ARTIST")
			}
			folderData.setdefault("album", None)
			folderData.setdefault("artist", None)
			folderData.setdefault("tag", None)
			folderDataList.append(folderData)

def getFlag():
	for subFolder in folderDataList:
		if "[M]" == subFolder["folderName"][len(subFolder["folderName"])-3:]:
			folderNameWithoutTag = subFolder["folderName"][:len(subFolder["folderName"])-4]
			os.rename(subFolder["folderName"], folderNameWithoutTag)
			subFolder.update({"folderName" : folderNameWithoutTag})
			subFolder.update({"tag" : "MQA"})
		elif "[E]" == subFolder["folderName"][len(subFolder["folderName"])-3:]:
			folderNameWithoutTag = subFolder["folderName"][:len(subFolder["folderName"])-4]
			os.rename(subFolder["folderName"], folderNameWithoutTag)
			subFolder.update({"folderName" : folderNameWithoutTag})
		elif "[ME]" == subFolder["folderName"][len(subFolder["folderName"])-4:]:
			folderNameWithoutTag = subFolder["folderName"][:len(subFolder["folderName"])-5]
			os.rename(subFolder["folderName"], folderNameWithoutTag)
			subFolder.update({"folderName" : folderNameWithoutTag})
			subFolder.update({"tag" : "MQA"})
		elif "[MQA-R]" == subFolder["folderName"][len(subFolder["folderName"])-7:]:
			folderNameWithoutTag = subFolder["folderName"][:len(subFolder["folderName"])-8]
			os.rename(subFolder["folderName"], folderNameWithoutTag)
			subFolder.update({"folderName" : folderNameWithoutTag})
			subFolder.update({"tag" : "MQA-R"})

def renameFolder():
	try:
		for subFolder in folderDataList:
			folderName = subFolder["folderName"]
			audioExtension = subFolder["audioExtension"]
			audioChannels = subFolder["audioChannels"]
			tag = subFolder["tag"]

			audioQuality = ""
			if len(subFolder["audioQuality"]) == 1:
				audioQuality = subFolder["audioQuality"][0]
			else:
				for i in range(len(subFolder["audioQuality"])):
					if i == 0:
						audioQuality += subFolder["audioQuality"][0]
					else:
						audioQuality += "／" + subFolder["audioQuality"][i]

			newFolderName = f"{folderName} [{audioExtension.upper()}][{audioChannels}ch][{tag}][{audioQuality}]"
			newFolderName = newFolderName.replace("[FLAC]", "").replace("[None]", "").replace("[2ch]", "")
			subFolder.update({"folderName" : newFolderName})

			os.rename(folderName, newFolderName)
	except:
		shutil.move(subFolder["folderName"], error_unknown_path)

def checkSpecialCharacters():
	folderWithSpecialCharacter = []
	try:
		for subFolder in glob.glob("*/"):
			if subFolder[:-1] == "[00] Error":
				continue
			else:
				for root, directories, files in os.walk(subFolder):
					for file in files:
						extension = os.path.splitext(file)[1][1:]
						if extension in audioExtension.keys():
							audio = audioExtension[extension](os.path.join(root, file))
							for char in specialCharacters:
								if (char in audio["ALBUM"][0]) or (char in audio["ARTIST"][0]):
									if subFolder not in folderWithSpecialCharacter:
										folderWithSpecialCharacter.append(subFolder)
				for folderData in folderWithSpecialCharacter:
					shutil.move(folderData, error_special_character_path)
	except:
		shutil.move(subFolder, error_album_check)

def errorLog():
	file = open("[00] Error/error_log.txt", "w",encoding="utf-8")
	for root, directories, files in os.walk("[00] Error"):
		for dire in directories:
			file.write(os.path.join(root, dire))
			file.write("\n")
	file.close()

def main():
	"""Implementation"""
	deleteDesktopIni()
	getFolderData()
	getFlag()
	renameFolder()
	checkSpecialCharacters()
	errorLog()

if __name__ == "__main__":
    main()
