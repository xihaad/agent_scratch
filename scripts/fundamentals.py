from dotenv import load_dotenv
from openai import OpenAI
from IPython.display import Markdown, display

load_dotenv(override=True)


import os
openai_api_key = os.getenv('OPENAI_API_KEY')

if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set - please head to the troubleshooting guide in the setup folder")



openai = OpenAI()

messages = [{"role": "user", "content": "Tell me a fun fact"}]
print(messages)

response = openai.chat.completions.create(model="gpt-5.4-nano", messages=messages)
print(response.choices[0].message.content)


question = "Please propose a hard, challenging question to assess someone's IQ. Respond only with the question."
messages = [{"role": "user", "content": question}]


response = openai.chat.completions.create(model="gpt-5.4-mini", messages=messages)
question = response.choices[0].message.content
print(question)




messages = [{"role": "user", "content": question}]
print(messages)


response = openai.chat.completions.create(model="gpt-5.4-mini", messages=messages)
answer = response.choices[0].message.content
print(answer)


display(Markdown(answer))
message = f"""
Here is a question:
{question}

And here is a possible answer that might be correct or incorrect:
{answer}

Please evaluate if the answer is correct or incorrect.
"""

print(message)
messages = [{"role": "user", "content": message}]
response = openai.chat.completions.create(model="gpt-5.4", messages=messages)
print(response.choices[0].message.content)