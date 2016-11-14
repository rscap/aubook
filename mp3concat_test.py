#!/usr/bin/env python

from pydub import AudioSegment
from glob import glob
import os

while True:
    try:
        inputPathy = raw_input('please provide path to files to concatentate: ')
        if not inputPathy:
            raise ValueError('no input')
        if inputPathy[:1] == '~':
            inputPathy = os.path.expanduser(inputPathy[:1])+inputPathy[1:]
        if inputPathy[-1] != '/':
            inputPathy = inputPathy+'/'
        inputPathy = inputPathy+'*.mp3'
        print inputPathy
        break
    except ValueError as e:
        print(e)
while True:
  try:
    outputPathy = raw_input('Please provide output path: ')
    if not outputPathy:
        raise ValueError('no input')
    if outputPathy[:1] == '~':
        print ('~ is first character')
        outputPathy = os.path.expanduser(outputPathy[:1])+outputPathy[1:]
    if outputPathy[-1] != '/':
        outputPathy = outputPathy+'/'
    print outputPathy
    break
  except ValueError as e:
      print(e)

while True:
  try:
    outputName = raw_input('Please provide output file name: ')
    if not outputName:
        raise ValueError('no input')
    if outputName[-4:] != '.mp3':
        print('does not end in .mp3')
        outputName = outputName + '.mp3'
    outputPathy = outputPathy+outputName
    print outputPathy
    break
  except ValueError as e:
       print(e)

inputPath = inputPathy
outputPath = outputPathy
## empty sound to put the combined files into
fullaudio = AudioSegment.empty()
## get all files from the path

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

fullaudio.export(outputPath, format="mp3").close()
print('file generation complete. See '+outputPath)
