from openai import OpenAI, APITimeoutError, RateLimitError, InternalServerError
import sys
from clean_duplicate_labels import clean_duplicate_labels
from util import request_GPT, parse_gpt_answer_to_list

def extract_keywords_from_a_post(post):
    write_message = lambda text: [
        {
            "role": "user", 
            "content": f'''
Given the following social media post, identify and list the key topics and relevant keywords that capture the users' experiences and sentiments about the vape product. Provide the keywords in a concise, bullet-point format.

Post:
{text}

Extracted Keywords:

-- Keyword 1
-- Keyword 2
-- Keyword 3
-- (Continue as needed)
'''
        }
    ]
    answer = request_GPT(write_message(post))
    return answer
    

def expand_labels_to_pos_and_neg(labels_list):
    write_message = lambda labels: [
        {
            "role": "user",
            "content": "Given a list of keywords, I need to expand each one by including both a positive and negative sentiment, where applicable. For keywords that do not naturally lend themselves to binary sentiments, keep them unchanged. Here's the list of keywords:\n\n"+
            "\n".join(f"-- {label}" for label in labels) +
            "\n\nGenerate a new single-level list where each applicable keyword is transformed into two versions: one with a positive sentiment and another with a negative sentiment. For example, transform 'Wait time' into 'long wait time' and 'short wait time'. Keywords without binary sentiments should be kept but listed in a modified or descriptive form. Ensure that the original keywords do not appear in the final list. Maintain using '--' to denote each item in your output list."
        }
    ]
    answer = request_GPT(write_message(labels_list))
    return answer
    
    
    
def generate_labels_from_many_posts(posts_list, cleaning_period=50):
    all_labels = []
    old_length = len(all_labels)
    for post in posts_list:
        initial_labels = extract_keywords_from_a_post(post)
        expanded_labels = expand_labels_to_pos_and_neg(parse_gpt_answer_to_list(initial_labels, "-"))
        final_labels = parse_gpt_answer_to_list(expanded_labels, "-")
        all_labels += final_labels
        # 定期清理重复标签
        if len(all_labels) - old_length >= cleaning_period:
            all_labels = clean_duplicate_labels(all_labels)
            old_length = len(all_labels)
    all_labels = clean_duplicate_labels(all_labels)
    return all_labels