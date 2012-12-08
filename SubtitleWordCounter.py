# -*- coding: UTF-8 –*-

import re
import sys

def main(argv):
	subtitleFileName = sys.argv[1]
	if not len(sys.argv) < 3:
		outputFileName = sys.argv[2]
	else:
		outputFileName = ''
	
	if subtitleFileName.endswith('.srt'):
		try:
			with open(subtitleFileName, 'r') as fileHandler:
				wordsLists = parseSRT(fileHandler)
		except:
			print('ERROR: File not opened, or file is blank.\n')
			sys.exit(2)
	else:
		print('ERROR: file format not supported.\n')
		sys.exit(2)
	
	if wordsLists != {}:
		if outputFileName != '':
			try:
				with open(outputFileName, 'w') as outputFileHandler:
					for word in sorted(wordsLists.keys()):
						outputFileHandler.write('{}: {}\n'.format(word, wordsLists[word]))
			except:
				print('ERROR: output file saving failed.\n')
		for word in sorted(wordsLists.keys()):
			print('{}: {}'.format(word, wordsLists[word]))
	else:
		print('No word found.\n')
			
def parseSRT(fileHandler):
	fileContent = fileHandler.readlines()
	fileLine = fileContent[0]
	lineType = 1
	wordsLists = {}
	for fileLine in fileContent:
		if lineType == 1:
			if re.search('^\d+$', fileLine):
				lineType = 2
			continue
		elif lineType == 2:
			if re.search('\d{2}:\d{2}:\d{2}\,\d{3} --> \d{2}:\d{2}:\d{2}\,\d{3}', fileLine):
				lineType = 3
			continue
		elif lineType == 3:
			wordsFound =  re.findall("[a-zA-Z']+",fileLine.lower())
			lineType = 1
			for word in wordsFound:
				if word not in wordsLists:
					wordsLists[word] = 0
				wordsLists[word] = wordsLists[word] + 1
	return wordsLists

if __name__ == '__main__':
	if len(sys.argv) < 2 or len(sys.argv) > 3:
		print('''USAGE: SubtitleWordCounter.py <subtitle_file> [output_file]
  subtitle_file: the file name of subtitle file. Support SRT format.
  output_file: the file name of the result of word counter. Leave it blank to skip saving to a file.''')
		sys.exit(1)
	else:
		main(sys.argv)
		
		