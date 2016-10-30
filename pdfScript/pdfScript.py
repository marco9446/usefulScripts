#!Python
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
import os, argparse



# parse args
parser = argparse.ArgumentParser(description='Short sample app')
parser.add_argument('-a', action="store", dest='action', choices=['merge', 'notes'], required=True)
parser.add_argument('-i', action="store", dest='input', nargs='+', required=True)
parser.add_argument('-o', action="store", dest='outputFile', default='./output.pdf')
parser.add_argument('--t', action="store", dest='template', default='./lines.pdf')

# Now, parse the command line arguments and store the values in the `args` variable
args = parser.parse_args()


'''
insert between each slide, one blanck slide with some lines for taking notes
'''
def printWithLines():
	# check if the input is multiple or is a directory
	if len(args.input) != 1 or os.path.isdir(args.input[0]):
		print("only one file permitted as input");
		return
	# rb stands for read bynary
	inp = PdfFileReader(open(args.input[0], 'rb'))
	template = PdfFileReader(open(args.template, 'rb')).pages[0]

	out = PdfFileWriter()

	for x in inp.pages:
	    out.addPage(x)
	    out.addPage(template)

	with open(args.outputFile, 'wb') as f:
	    out.write(f)


'''
merge multiple pdf in just one big file
'''
def mergePdfs():
	files = []
	merger = PdfFileMerger()

	if (os.path.isdir(args.input[0])):
		files = [x for x in os.listdir(args.input[0]) if x.endswith('.pdf')]
	else:
		files = args.input
	for fname in files:
		if os.path.isdir(args.input[0]):
			merger.append(PdfFileReader(open(os.path.join(args.input[0], fname), 'rb')))
		else:
			merger.append(PdfFileReader(open(fname, 'rb')))
	merger.write(args.outputFile)



if args.action == 'merge':
	mergePdfs();
elif args.action == 'notes':
	printWithLines();
