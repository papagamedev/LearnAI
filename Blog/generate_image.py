import os
import argparse
import chatgpt

# check arguments

parser = argparse.ArgumentParser("generate_image")
parser.add_argument("prompt", help="Prompt to generate the image", type=str)
parser.add_argument("-o","--outputFile", help="File name to write with translated article", type=str)
parser.add_argument("-m", "--model", help="Model to use", choices=["dall-e-2","dall-e-3"], type=str, default="dall-e-3")
parser.add_argument("-s", "--size", help="Size of the output image", choices=["512", "1024"], type=str, default="1024")
parser.add_argument("-q", "--quality", help="Size of the output image", choices=["standard", "hd"], type=str, default="standard")
parser.add_argument("-st", "--style", help="Style of the output image", choices=["vivid", "natural"], type=str, default="natural")
args = parser.parse_args()

# if no output file was provided, use a default name
if args.outputFile is not None:
  outputFile = args.outputFile
else:
  outputFile = args.prompt + "_" + args.model + "_" + args.quality + "_" + args.style + ".png"

# check if output file exists
if os.path.isfile(outputFile):
  print("Output file already exists!")
  exit(1)

chatgpt.CallDallE(args.prompt, args.model, args.size, args.quality, args.style, outputFile)
