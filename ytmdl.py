import subprocess
import os

running = True
formats = ["ogg", "opus", "mp3", "wav", "flac"]

print("Welcome to music-dl, a tool built on youtube-dl!")

# printOptions: Prints the current options for music-dl
def printOptions():
	print("(d)ownload a new album")
	print("(q)uit music-dl")


# verifyFolder: Prompts the user until a new folder is created, or an existing one is entered
def verifyFolder(location):
	if os.path.isdir(location):
		return location
	else:
		print("The folder '" + location + "' doesn't exist.")
		newFolder = input("Create one? (note that it'll need a cover image inside later) [y/n]: ")
		if (newFolder == "y"):
			os.mkdir(location)
			print("Folder '" + location + "' created!")
			return location
		else:
			location = verifyFolder(input("Enter a folder name for the playlist: "))
	return location

# verifyFormat: Checks if the entered file format is supported
def verifyFormat(fileFormat):
	if (fileFormat in formats):
		return fileFormat
	else:
		print("Supported formats: ogg, opus, mp3, wav, flac")
		fileFormat = verifyFormat(input("Enter a format: "))
	return fileFormat

# downloadPrompt: Prompts the user for a link to the youtube-playlist
def downloadPrompt():
	playlist = input("Enter the playlist URL: ")
	location = verifyFolder(input("Enter a folder name for the playlist: "))
	print("Downloading...")
	subprocess.run(["youtube-dl", "-x", playlist], cwd=os.getcwd() + "/" + location)
	print("Album downloaded.")
	convertAlbum(location)

# convertAlbum: Converts the album to the format entered by the user
def convertAlbum(location):
	print("Downloaded albums tend to have songs in multiple filetypes.")
	print("Would you like to convert them?")
	print("Common formats are: ogg, opus, mp3, wav, flac")
	print("ogg is reccomended because it supports metadata and album covers")
	albumFormat = verifyFormat(input("Enter a format (no period): "))
	os.chdir(location)
	songs = os.listdir()
	print("Converting album...")
	for song in songs:
		# Exclude images
		if (song[-3:] != "png" and song[-3:] != "jpg" and song[-4:] != "jpeg"):
			songData = song.split(".")
			subprocess.run(["ffmpeg", "-loglevel", "panic", "-i", song, songData[0] + "." + albumFormat])
			print("Removing " + song)
			subprocess.run(["rm", song])
	os.chdir("..")


# The main loop, asks the user for what option to run
while (running):
	printOptions()
	selection = input("What would you like to do: ")
	if (selection == "d"):
		downloadPrompt()
	elif (selection == "q"):
		running = False
	else:
		print("\nInvalid option '" + selection + "'. Usage:")

print("Exiting...")

