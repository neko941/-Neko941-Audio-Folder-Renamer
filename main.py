from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.wavpack import WavPack
from mutagen.wave import WAVE
from mutagen.dsf import DSF
from mutagen.dsdiff import DSDIFF
from mutagen.aiff import AIFF
import pathlib
import glob
import os
import sys
import shutil
import array

"""Global Variables"""
folderDataList = []
audioExtensionWishlist = ["mp3", "flac", "wav", "wv", "dsf", "dff", "aiff"]

"""Create Folder to Store Error"""
if not os.path.exists("[00] Error"):
	os.mkdir(os.path.join("[00] Error", "./"))
errorLog = open("[00] Error/errorLog.txt","w+")

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

def checkAudioExtension():
	"""Put Folder with 2 or more Extensions into [00] Error"""
	"""Get Folder Names and Audio Extentions"""
	for subFolder in glob.glob("*/"):
		if subFolder[:-1] == "[00] Error":
			continue
		else:
			extensionsInFolder = []
			for root, directories, files in os.walk(subFolder):
				for file in files:
					if os.path.splitext(file)[1][1:] in audioExtensionWishlist:
						if os.path.splitext(file)[1][1:] not in extensionsInFolder:
							extensionsInFolder.append(os.path.splitext(file)[1][1:])
		if len(extensionsInFolder) != 1:
			errorLog.write("Folder has Audio Files with Different Extensions: %s\n" %subFolder[:-1])
			shutil.move(subFolder, "[00] Error")
		else:
			folderData = {"folderName" : subFolder[:-1] , "audioExtension" : extensionsInFolder[0]}
			folderDataList.append(folderData)

def checkMP3(subFolder):
	"""Rename MP3 Folders"""
	checkBitRate = []

	for root, directories, files in os.walk(subFolder):
		for file in files:
			if file.endswith(".mp3"):
				audio = MP3(os.path.join(root, file))
				bitrate = audio.info.bitrate/1000
				if bitrate not in checkBitRate:
					checkBitRate.append(bitrate)

	if len(checkBitRate) == 1:
		if (audio.info.channels == 2):
			if (audio.info.encoder_settings == "-V 0"):
				dest = subFolder + " [MP3][V0]"
				os.rename(subFolder , dest)
			else:
				dest = subFolder + " [MP3][%iKbps]" %checkBitRate[0]
				os.rename(subFolder , dest)
		else:
			if (audio.info.encoder_settings == "-V 0"):
				dest = subFolder + " [MP3][%ich][V0]" %audio.info.channels
				os.rename(subFolder , dest)
			else:
				dest = subFolder + " [MP3][%ich][%iKbps]" %(audio.info.channels, checkBitRate[0])
				os.rename(subFolder , dest)
	else:
		errorLog.write("Folder has Audio Files with Different Qualities: %s\n" %subFolder[:-1])
		shutil.move(subFolder, "[00] Error")

def checkFLAC(subFolder):
	"""Rename FLAC Folders"""
	checkBitsPerSample = []
	checkSampleRate = []

	for root, directories, files in os.walk(subFolder):
		for file in files:
			if file.endswith(".flac"):
				audio = FLAC(os.path.join(root, file))
				bitsPerSample = audio.info.bits_per_sample
				sampleRate = checkNumber(audio.info.sample_rate/1000)
		        
				if bitsPerSample not in checkBitsPerSample:
					checkBitsPerSample.append(bitsPerSample)
				if sampleRate not in checkSampleRate:	
					checkSampleRate.append(sampleRate)

	if len(checkBitsPerSample) == 1 and len(checkSampleRate) == 1:
		if "MQA" in str(audio.get("encoder")):
			if (audio.info.channels == 2):
				dest = subFolder + " [MQA][%i-%s]" %(checkBitsPerSample[0], checkSampleRate[0])
				os.rename(subFolder , dest)
			else:
				dest = subFolder + " [MQA][%ich][%i-%s]" %(audio.info.channels, checkBitsPerSample[0], checkSampleRate[0])
				os.rename(subFolder , dest)
		else:
			if (audio.info.channels == 2):
				dest = subFolder + " [%i-%s]" %(checkBitsPerSample[0], checkSampleRate[0])
				os.rename(subFolder , dest)
			else:
				dest = subFolder + " [%ich][%i-%s]" %(audio.info.channels, checkBitsPerSample[0], checkSampleRate[0])
				os.rename(subFolder , dest)
	else:
		errorLog.write("Folder has Audio Files with Different Qualities: %s\n" %subFolder[:-1])
		shutil.move(subFolder, "[00] Error")

def checkWAVE(subFolder):
	"""Rename WAVE Folders"""
	checkBitsPerSample = []
	checkSampleRate = []

	for root, directories, files in os.walk(subFolder):
		for file in files:
			if file.endswith(".wav"):
				audio = WAVE(os.path.join(root, file))
				bitsPerSample = audio.info.bits_per_sample
				sampleRate = checkNumber(audio.info.sample_rate/1000)
		        
				if bitsPerSample not in checkBitsPerSample:
					checkBitsPerSample.append(bitsPerSample)
				if sampleRate not in checkSampleRate:	
					checkSampleRate.append(sampleRate)

	if len(checkBitsPerSample) == 1 and len(checkSampleRate) == 1:
		if (audio.info.channels == 2):
			dest = subFolder + " [WAV][%i-%s]" %(checkBitsPerSample[0], checkSampleRate[0])
			os.rename(subFolder , dest)
		else:
			dest = subFolder + " [WAV][%ich][%i-%s]" %(audio.info.channels, checkBitsPerSample[0], checkSampleRate[0])
			os.rename(subFolder , dest)
	else:
		errorLog.write("Folder has Audio Files with Different Qualities: %s\n" %subFolder[:-1])
		shutil.move(subFolder, "[00] Error")

def checkWAVEPACK(subFolder):
	"""Rename WAVEPACK Folders"""
	checkBitsPerSample = []
	checkSampleRate = []

	for root, directories, files in os.walk(subFolder):
		for file in files:
			if file.endswith(".wv"):
				audio = WavPack(os.path.join(root, file))
				bitsPerSample = audio.info.bits_per_sample
				sampleRate = checkNumber(audio.info.sample_rate/1000)
		        
				if bitsPerSample not in checkBitsPerSample:
					checkBitsPerSample.append(bitsPerSample)
				if sampleRate not in checkSampleRate:	
					checkSampleRate.append(sampleRate)

	if len(checkBitsPerSample) == 1 and len(checkSampleRate) == 1:
		if (audio.info.channels == 2):
			dest = subFolder + " [WV][%i-%s]" %(checkBitsPerSample[0], checkSampleRate[0])
			os.rename(subFolder , dest)
		else:
			dest = subFolder + " [WV][%ich][%i-%s]" %(audio.info.channels, checkBitsPerSample[0], checkSampleRate[0])
			os.rename(subFolder , dest)
	else:
		errorLog.write("Folder has Audio Files with Different Qualities: %s\n" %subFolder[:-1])
		shutil.move(subFolder, "[00] Error")

def checkDSF(subFolder):
	"""Rename DSF Folders"""
	checkBitsPerSample = []
	checkSampleRate = []

	for root, directories, files in os.walk(subFolder):
		for file in files:
			if file.endswith(".dsf"):
				audio = DSF(os.path.join(root, file))
				bitsPerSample = audio.info.bits_per_sample
				sampleRate = "{:.1f}".format(audio.info.sample_rate/1000000)
		        
				if bitsPerSample not in checkBitsPerSample:
					checkBitsPerSample.append(bitsPerSample)
				if sampleRate not in checkSampleRate:	
					checkSampleRate.append(sampleRate)

	if len(checkBitsPerSample) == 1 and len(checkSampleRate) == 1:
		if (checkBitsPerSample[0] == 1):
			if (audio.info.channels == 2):
				dest = subFolder + " [DSF][%i-%s]" %(checkBitsPerSample[0], checkSampleRate[0])
				os.rename(subFolder , dest)
			else:
				dest = subFolder + " [DSF][%ich][%i-%s]" %(audio.info.channels, checkBitsPerSample[0], checkSampleRate[0])
				os.rename(subFolder , dest)
	else:
		errorLog.write("Folder has Audio Files with Different Qualities: %s\n" %subFolder[:-1])
		shutil.move(subFolder, "[00] Error")

def checkDFF(subFolder):
	"""Rename DFF Folders"""
	checkBitsPerSample = []
	checkSampleRate = []

	for root, directories, files in os.walk(subFolder):
		for file in files:
			if file.endswith(".dff"):
				audio = DSDIFF(os.path.join(root, file))
				bitsPerSample = audio.info.bits_per_sample
				sampleRate = "{:.1f}".format(audio.info.sample_rate/1000000)
		        
				if bitsPerSample not in checkBitsPerSample:
					checkBitsPerSample.append(bitsPerSample)
				if sampleRate not in checkSampleRate:	
					checkSampleRate.append(sampleRate)

	if len(checkBitsPerSample) == 1 and len(checkSampleRate) == 1:
		if (checkBitsPerSample[0] == 1):
			if (audio.info.channels == 2):
				dest = subFolder + " [DFF][%i-%s]" %(checkBitsPerSample[0], checkSampleRate[0])
				os.rename(subFolder , dest)
			else:
				dest = subFolder + " [DFF][%ich][%i-%s]" %(audio.info.channels, checkBitsPerSample[0], checkSampleRate[0])
				os.rename(subFolder , dest)
	else:
		errorLog.write("Folder has Audio Files with Different Qualities: %s\n" %subFolder[:-1])
		shutil.move(subFolder, "[00] Error")

def checkAIFF(subFolder):
	"""Rename AIFF Folders"""
	checkBitsPerSample = []
	checkSampleRate = []

	for root, directories, files in os.walk(subFolder):
		for file in files:
			if file.endswith(".aiff"):
				audio = AIFF(os.path.join(root, file))
				bitsPerSample = audio.info.bits_per_sample
				sampleRate = checkNumber(audio.info.sample_rate/1000)
		        
				if bitsPerSample not in checkBitsPerSample:
					checkBitsPerSample.append(bitsPerSample)
				if sampleRate not in checkSampleRate:	
					checkSampleRate.append(sampleRate)

	if len(checkBitsPerSample) == 1 and len(checkSampleRate) == 1:
		if (audio.info.channels == 2):
			dest = subFolder + " [AIFF][%i-%s]" %(checkBitsPerSample[0], checkSampleRate[0])
			os.rename(subFolder , dest)
		else:
			dest = subFolder + " [AIFF][%ich][%i-%s]" %(audio.info.channels, checkBitsPerSample[0], checkSampleRate[0])
			os.rename(subFolder , dest)
	else:
		errorLog.write("Folder has Audio Files with Different Qualities: %s\n" %subFolder[:-1])
		shutil.move(subFolder, "[00] Error")

def renameFolders():
	"""Rename Folders by Audio Quality"""
	try:
		for folderData in folderDataList:
			if folderData["audioExtension"] == "mp3":
				checkMP3(folderData["folderName"])
			elif folderData["audioExtension"] == "flac":
				checkFLAC(folderData["folderName"])
			elif folderData["audioExtension"] == "wav":
				checkWAVE(folderData["folderName"])
			elif folderData["audioExtension"] == "wv":
				checkWAVEPACK(folderData["folderName"])
			elif folderData["audioExtension"] == "dsf":
				checkDSF(folderData["folderName"])
			elif folderData["audioExtension"] == "dff":
				checkDFF(folderData["folderName"])
			elif folderData["audioExtension"] == "aiff":
				checkAIFF(folderData["folderName"])
	except Exception as e:
		errorLog.write("%s: %s\n" %(folderData["folderName"]), e)
		shutil.move(folderData["folderName"], "[00] Error")

def main():
	"""Implementation"""
	deleteDesktopIni()
	checkAudioExtension()
	renameFolders()
	errorLog.close() 

if __name__ == "__main__":
    main()
