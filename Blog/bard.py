import google.generativeai as genai
import os

def CallBard(systemPrompt, userPrompt, model, temperature, maxTokens):
  # to set the env var, use:
  # setx GENAI_API_KEY xxxxxxxxxxxxxxxxxxxxxxxxxx 
  api_key = os.environ['GENAI_API_KEY']
  genai.configure(api_key=api_key)

  # Set up the model
  generation_config = {
    "temperature": temperature,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": maxTokens,
  }

  safety_settings = [
    {
      "category": "HARM_CATEGORY_HARASSMENT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_HATE_SPEECH",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    }
  ]

  model = genai.GenerativeModel(model_name=model,
                                generation_config=generation_config,
                                safety_settings=safety_settings)

  print("Sending prompt to Bard API")
  prompt_parts=[systemPrompt, userPrompt]
  response = model.generate_content(prompt_parts)
  return response.text
