#!/usr/bin/env python

from pydub import AudioSegment
from glob import glob
import os
try:
    inputPathy = raw_input('please provide path to files to concatentate: ')
    if inputPathy[:1] == '~':
        inputPathy = os.path.expanduser(inputPathy[:1])+inputPathy[1:]
    if inputPathy[-1] != '/':
        inputPathy = inputPathy+'/'
    inputPathy = inputPathy+'*.mp3'
    print inputPathy

outputPathy = raw_input('Please provide output path: ')
if outputPathy[-1] != '/':
    outputPathy = outputPathy+'/'
if onputPathy[:1] == '~':
    ouputPathy = os.path.expanduser(outputPathy[:1])+outputPathy[1:]
outputName = raw_input('Please provide output file name: ')
if outputName[-4:] != '.mp3':
    outputName = outputName + '.mp3'
outputPathy = outputPathy+outputName
print outputPathy

inputPath = inputPathy #'/Users/apsnooz/Desktop/Beginners/Beginners 1-7.mp3'
outputPath = outputPathy #'/Users/apsnooz/Desktop/testOutPut.mp3'
## empty sound to put the combined files into
fullaudio = AudioSegment.empty()
## get all files from the path
#files = os.listdir(inputPath)
# AudioSegment.from_mp3(inputPath)

# playlist_songs = [AudioSegment.from_mp3(mp3_file) for mp3_file in glob("/Users/apsnooz/Desktop/Beginners/*.mp3")]

# ideas - parse text to list only file name
num_mp3 = 0
print('compling folder contents into single file...')
#for mp3 in glob("/Users/apsnooz/Desktop/testmp3/*.mp3"):
for mp3 in glob(inputPath):
    print('concatenating '+mp3)
    segment = AudioSegment.from_mp3(mp3)
    fullaudio = fullaudio + segment
    #num_mp3 += 1
    #print(num_mp3)

# newfile = open(outputPath,'w')
# for each in playlist_songs:
#     fullaudio += each
#
# # writing mp3 files is a one liner
fullaudio.export(outputPath, format="mp3").close()
print('file generation complete. See '+outputPath)
