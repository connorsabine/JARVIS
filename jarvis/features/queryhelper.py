import openai
from jarvis import config

openai.api_key = config.OPENAI_API_KEY

def openaiapi(history):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an assistant named JARVIS. Respond briefly and clearly."}
            ] + history[-4:],
        )
        return completion.choices[0].message["content"]

    except Exception as e:
        return False
