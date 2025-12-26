import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_explanation(etf_a, etf_b):
    prompt = f"""
    You are a financial analyst.

    ETF A: {etf_a}
    ETF B: {etf_b}

    Explain which ETF looks stronger and why.
    """

    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a professional financial analyst."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.3
)

    return response.choices[0].message.content
