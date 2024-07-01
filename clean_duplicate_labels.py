from utils import request_GPT, parse_gpt_answer_to_list

def clean_duplicate_labels(labels_list):
    write_message = lambda labels: [
        {
            "role": "user",
            "content": "Here's a list of keywords. For each keyword, compare it with the previous ones for duplicate meanings. Exclude duplicates and keep only the unique ones. Here is the list:\n\n"+
            "\n".join(f"-- {label}" for label in labels) +
            "\n\nReturn a cleaned-up list with duplicates removed."
        }
    ]
    response = request_GPT(write_message(labels_list))
    if response is None:
        print("unsucessful cleaning duplicates")
        return response
    else:
        cleaned_labels = parse_gpt_answer_to_list(response.choises[0].message.content)
        print("successfull cleaned "+(len(labels_list)-len(cleaned_labels))+" duplicates")
        return cleaned_labels