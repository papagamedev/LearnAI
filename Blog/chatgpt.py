import os
from openai import OpenAI

def CallChatGpt(systemPrompt, userPrompt, model, temperature, maxTokens):
  client = OpenAI(
      # This is the default and can be omitted
      api_key=os.environ['OPENAI_API_KEY'],
  )

  print("Sending prompt to OpenAI API")
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
