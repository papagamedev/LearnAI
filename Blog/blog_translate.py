import os
import argparse
import frontmatter

def CallModel(systemPrompt, userPrompt, model, temperature, maxTokens):
  if args.model == "gemini-pro":
    import bard
    return bard.CallBard(systemPrompt, userPrompt, model, temperature, maxTokens)
  else:
    import chatgpt
    return chatgpt.CallChatGpt(systemPrompt, userPrompt, model, temperature, maxTokens)

def TranslateShortText(text, model, temperature, maxTokens):
  systemPrompt = "You are a kind and helpful assistant."
  userPrompt = "Translate this text to English:\n" + text
  return CallModel(systemPrompt, userPrompt, model, temperature, maxTokens)

def TranslateArticle(article, model, temperature, maxTokens):
  systemPrompt = "You are a kind and helpful assistant.\n" +\
              "Follow the writing style of the original author when translating.\n" +\
              "Do not change the contents of the {% and %} tags.\n" +\
              "Use context specific words, phrases and English idioms instead of just doing a literal translation.\n"
  userPrompt = "Translate this text to English:\n" + article
  return CallModel(systemPrompt, userPrompt, model, temperature, maxTokens)

# check arguments

parser = argparse.ArgumentParser("blog_translate")
parser.add_argument("inputFile", help="File name to be sent to google api", type=str)
parser.add_argument("-m", "--model", help="Model to use", choices=["gemini-pro","gpt-3.5-turbo","gpt-4","gpt-4-1106-preview"], type=str, default="gpt-4-1106-preview")
parser.add_argument("-o","--outputFile", help="File name to write with translated article", type=str)
parser.add_argument("-t","--temperature", required=False, type=float, default=1.0)
parser.add_argument("-mt", "--maxTokens", required=False, type=int, default=4096)
args = parser.parse_args()

# read file to translate
print("Reading file to translate: " + args.inputFile)
try:
  with open(args.inputFile, encoding="utf-8") as f:
    fileContents = f.read()
except IOError as e:
  print("Failed to read input file: " + args.inputFile)
  exit(2)

# if no output file was provided, use a default name
if args.outputFile is not None:
  outputFile = args.outputFile
else:
  outputFile = args.inputFile + "_" + args.model + "_" + str(args.temperature) + ".md"

# check if output file exists
if os.path.isfile(outputFile):
  print("Output file already exists!")
  exit(1)

# parse the input file
post = frontmatter.loads(fileContents)
article = post.content
description = post.metadata['description']
title = post.metadata['title']

# translate texts using the model  
translatedDescription = TranslateShortText(description, args.model, args.temperature, args.maxTokens)
translatedTitle = TranslateShortText(title, args.model, args.temperature, args.maxTokens)
translatedArticle = TranslateArticle(article, args.model, args.temperature, args.maxTokens)

# update the post with the translations
post.content = translatedArticle
post.metadata['lang'] = "en"
post.metadata['description'] = translatedDescription
post.metadata['title'] = translatedTitle

# Write the output file
print("Writing file " + outputFile)

try:
  with open(outputFile, mode="wt", encoding="utf-8") as fo:
    outputFileContents = frontmatter.dumps(post) 
    fo.write(outputFileContents)
except IOError as e:
  print("Failed to write output file: " + outputFile)
  print("Writing output to console")
  print(outputFileContents)
  exit(3)
