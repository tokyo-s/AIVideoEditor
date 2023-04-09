import os
import openai
import config

os.environ['OPENAI_API_KEY'] = config.OPEN_API_KEY

openai.api_key = os.getenv("OPENAI_API_KEY")


def summarize(prompt, question = '\n\n write this text as a newsletter'):
    response = openai.Completion.create(
  model="text-davinci-003",
  prompt= prompt+question,   #Tl;dr
  temperature=0.5,
  max_tokens=300,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=1
)
    return response['choices'][0]['text']