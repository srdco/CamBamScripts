#Title: CamBam Regex
#Purpose: Provide a post-build processing script to replace a known
#         string with text defined by user at the time of processing.
#         Original motivation was to provide a touchoff point at every
#         toolchange, while allowing user to determine that touchoff
#         point when the gcode is simple built (helpful for CNC knee mills
#         with limited toolholders).
#Version: 0.1
#Date: 4/15/2016
#Author: Timothy Snowden, Solid Rock Enterprises
#NOTES: Main sources for code patterns were
# Jeff Bauer's "Searching and Replacing Text in a File" in 
# Safari's PYTHON COOKBOOK, and python-course.eu's Entry Widgets page.

#import library for all supported OS'es + OS specific library
import os, sys 
#import GUI libraries (Tkinter = main, tkMessageBox = easy displays)
from Tkinter import *
from tkMessageBox import *

#---
#FUNCTIONS
#---
#Function: display message with script usage directions
def usageInstructions():
	msg = "To use this script, please use command: \n  [" + os.path.basename(sys.argv[0]) + "]\n  >>>[search_text]\n  >>>[original-file-name]\n  >>>[text to append to filename (OPTIONAL - preserves original file)]\nNo changes were made.\nPlease try again."
	showinfo(title=None, message=msg)

#Function: get replacement text from user and do a search/replace
def replaceWithUserText(event):
	replaceText = userText.get() #actually get the text the user inputted
	root.destroy() #close the dialog box
	
	#Check if we actually got any text from the user
	if not replaceText: 
		usageInstructions() #if not, display the usage instructions
		return #and end the script
	
	#Otherwise, search & replace
	searchText = sys.argv[1] #get the text to search for from the arguments passed to the script
	
	#Create the input / output objects
	input = sys.stdin
	output = sys.stdout
	
	input = open(sys.argv[2]) #open the source file to edit
	
	#Check if a new file suffix was given & create a new file if it was
	if numArgs == 4:
		#New file suffix given ... so create the new filename
		splitFilename = sys.argv[2].split('.') #split the filename at every period to get the file extension
		splitLength = len(splitFilename) #count how many pieces the filename was split into
		oldFilename = splitFilename[0] #the old filename is at least the first part
		
		#But...if the filename had many periods (e.g. 'my.file.is.badly.named.txt'), we need everything but the last part
		if splitLength > 2: #so, check if there were more than 2 parts when the filename was split
			i = 1 #initiate a counter
			while i < splitLength-1: #keep gluing the parts together as long as we haven't reached the last part (the file extension)
				oldFilename += "." + splitFilename[i] #glue the next part on with a period
				i=i+1 #increment the counter
		#Now, finally, create the new filename by gluing the last part (the file extension) back onto the end
		newFilename = oldFilename + "-" + sys.argv[3] + "." + splitFilename[splitLength-1]
		
		#Create the new file! (note, this automatically escapes spaces in a Linux filepath)
		output = open(newFilename, 'w')

	#Use regex to search and replace and write the changes to the selected file
	output.write(input.read().replace(searchText, replaceText))
	output.close() #close the output file
	input.close() #close the input (source) file
#END FUNCTIONS

#---
#MAIN so, check if so, check if SCRIPT
#---
#get the number of args passed to the script
numArgs = len(sys.argv)

#Check number or arguments to determine:
# 3 args = just replace the old file with the new one
# 4 args = duplicate the file before editing to preserve original file
if 3 <= numArgs <= 4:
	#Dialog box
	root = Tk() #create dialog box object
	Label(root, text="Please enter the replacement text\nand press RETURN/ENTER: ").grid(row=0, sticky=W+E, padx=4) #create field label
	
	userText = Entry(root) #create entry field
	userText.grid(row=1, sticky=W+E, padx=4) #assign entry field a position in the dialog box
	userText.bind("<Return>", replaceWithUserText) #bind the "RETURN" event in the entry field to the search-and-replace function

	root.mainloop() #actually launch the dialog box

#If insufficient or too many arguments were passed, display instructions for the script
else:
	usageInstructions()
