from openai import OpenAI



def generate_replies(message: str, api_key: str, tone: str, platform: str) -> dict:

    client = OpenAI(api_key=api_key)


    prompt = f"""

You are an expert communication assistant.


The user will paste a comment, DM, email, or message.

Generate 3 strong reply options.


Tone: {tone}

Platform: {platform}


Rules:

- Make each reply natural and human

- Make each option meaningfully different

- Keep replies polished and practical

- Fit the selected tone and platform

- Do not sound robotic

- Do not add explanations outside the replies


Input message:

"{message}"


Return exactly in this format:


REPLY OPTION 1:

...


REPLY OPTION 2:

...


REPLY OPTION 3:

...

"""


    response = client.chat.completions.create(

        model="gpt-5-mini",

        messages=[{"role": "user", "content": prompt}]

    )


    return {

        "raw": response.choices[0].message.content

    }