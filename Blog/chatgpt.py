import os
import requests
from openai import OpenAI

def CreateOpenAIClient():
  return OpenAI(
      # This is the default and can be omitted
      api_key=os.environ['OPENAI_API_KEY']
  )

def CallChatGpt(systemPrompt, userPrompt, model, temperature, maxTokens):
  client = CreateOpenAIClient()
  print("Sending prompt to ChatGPT model " + model)
  chatCompletion = client.chat.completions.create(
    messages=[
      {
        "role": "system", 
        "content": systemPrompt
      },
      {
        "role": "user",
        "content": userPrompt
      }
    ],
    model=model,
    temperature=temperature,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    max_tokens=maxTokens
  )
  response = chatCompletion.choices[0].message.content
  return response

def CallDallE(prompt, model, size, quality, style, outputFile):
  client = CreateOpenAIClient()
  print("Sending prompt to Dall-E model " + model)
  sizeStr=str(size)+"x"+str(size)
  response = client.images.generate(
    prompt=prompt,
    model=model,
    size=sizeStr,
    quality=quality,
    style=style
  )
  url = response.data[0].url
  DownloadImage(url, outputFile)

def DownloadImage(url, filename):
  print("Download image from " + url)
  with open(filename, 'wb') as handle:
    response = requests.get(url, stream=True)
    if not response.ok:
      print(response)
    for block in response.iter_content(1024):
      if not block:
        break
      handle.write(block)
