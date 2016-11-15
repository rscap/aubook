#!/usr/bin/env python

from pydub import AudioSegment
from glob import glob
import os

class concatAudio:

    def __init__(self,dir,name):
        #self.filenames = filenames
        self.dir = dir
        self.name = name

    def concat(self):
        outputPath = self.dir+'/'+self.name+'.mp3'
        # print('outputPath = '+str(outputPath))
        # print('\n')
        # print('...starting concat')

        mp3_files = self.dir+'/*.mp3'
        # print('mp3_files = '+mp3_files)
        ## empty sound to put the combined files into
        fullaudio = AudioSegment.empty()
        # count = 0
        # for item in glob(mp3_files):
        #     print(str(count)+' '+item)
        #     count += 1
        # print('glob(self.dir) = '+str(glob(self.dir)))
        # num_mp3 = 0
        print('compling folder contents into single file...')
        for file in glob(mp3_files):
            print('concatenating '+file)
            segment = AudioSegment.from_mp3(file)
            fullaudio = fullaudio + segment
            #num_mp3 += 1
            #print(num_mp3)
        fullaudio.export(outputPath, format="mp3").close()
        print('self.name = '+self.name)
        for file in glob(mp3_files):
            # print('file = '+file)
            # print('os.path.basename(file) = '+os.path.basename(file))
            if file != outputPath:
                os.remove(file)


# a = concatAudio('/Users/snooz/Downloads/mp3','test')
# print(a)
# # print('a.name = '+a.name)
# # print('a.dir = '+a.dir)
# a.concat()
