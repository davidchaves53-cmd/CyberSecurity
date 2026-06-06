from openai import OpenAI

client = OpenAI()

def explain_event(event: dict):
    prompt = f"Explain this security event in clear language and assess its risk: {event}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message["content"]
