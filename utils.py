from openai import OpenAI, APITimeoutError, RateLimitError, InternalServerError
from GPT_parameters import *

def request_GPT(messages):
    CLIENT = OpenAI(api_key=api_key)
    response = None
    try:
        response = CLIENT.chat.completions.create(
            messages=messages,
            model=model,
            temperature=temperature,
        )
    except APITimeoutError as timeout:
        print("time out:", timeout)
    except RateLimitError as ratelimit:
        print("hit rate limit:", ratelimit)
    except Exception as e:
        print("error:", e)
    finally:
        if response is not None:
            return response.choices[0].message.content
        return None
    
    
def parse_gpt_answer_to_list(answer, bullet):
    listed_answers = answer.split("\n")
    stripped_answers = [ans.strip(bullet+" ") for ans in listed_answers if ans.strip()[0] == "-"]
    if len(stripped_answers) == 0:
        print("no items. invalid answer:")
        print(answer)
        return None
    clean_answers = [ans.split(":")[-1] for ans in stripped_answers if ans]
    return clean_answers