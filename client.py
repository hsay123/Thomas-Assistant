from openai import OpenAI
import os
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY", ""),
    )

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a virtual assistant names thomas skilled in tasks like Alexa and Google Cloud "},
        {"role": "user", "content": "What is coding"}
    ]
)

print(completion.choices[0].message.content)