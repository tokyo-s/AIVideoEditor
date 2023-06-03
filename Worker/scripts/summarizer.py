import os
import openai
import config
import logging as log

os.environ['OPENAI_API_KEY'] = config.OPEN_API_KEY
openai.api_key = os.getenv("OPENAI_API_KEY")

log.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level='INFO')


def summarize(prompt, question = '\n\n summarize this text please keeping the most important information', model='gpt-4'):
  log.info("Summarizing text: {}".format(prompt))

  messages = [{"role": "user", "content": prompt+question}]

  prompt+question
  response = openai.ChatCompletion.create(
    model=model,
    messages=messages,
    temperature=0
  )

  return response['choices'][0]['message']['content']