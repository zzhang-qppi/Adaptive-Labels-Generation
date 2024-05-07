from util import request_GPT, parse_gpt_answer_to_list

def search_for_new_labels_in_posts(posts, labels):
    write_message = lambda posts_str, labels_str:[
        {
            "role": "user",
            "content": f'''
Please analyze the selection of social media content provided below to identify themes or topics not currently captured by our existing labels. List potential keywords that can be considered for addition as new labels. These keywords should be distinct and relevant, excluding any that overlap with the following existing labels:

{labels_str}

Provide a concise list of these new keyword suggestions for potential addition to our label set. Use '--' to denote each item in your output list
The social media contents:

{posts_str}


'''
        }
    ]
    
    posts_str = "\n** ".join(posts)
    labels_str = "\n-- ".join(labels)

    answer = request_GPT(write_message(posts_str, labels_str))
    new_labels = parse_gpt_answer_to_list(answer, bullet='-')
    return new_labels
    
def select_posts_less_relevant_to_existing_labels(labeled_posts_df, selection_size):
    '''
    ReadME.md 解释相关性计算的考虑
    '''
    
    labeled_posts_df['ones_count'] = labeled_posts_df.sum(axis=1)

    # Calculate the length of each comment
    labeled_posts_df['comment_length'] = labeled_posts_df.index.map(len)

    # Calculate percentile ranks
    labeled_posts_df['ones_count_percentile'] = labeled_posts_df['ones_count'].rank(pct=True)
    labeled_posts_df['comment_length_percentile'] = labeled_posts_df['comment_length'].rank(pct=True)

    # Calculate inverse percentile for comment length
    labeled_posts_df['comment_length_inv_percentile'] = 1 - labeled_posts_df['comment_length_percentile']

    # Calculate the final relevance score
    labeled_posts_df['relevance_score'] = labeled_posts_df['ones_count_percentile'] * labeled_posts_df['comment_length_inv_percentile']
    sorted_df = labeled_posts_df.sort_values(by='relevance_score', ascending=True)

    # Select the top N least relevant comments
    # Let's choose N = 5 for this example
    least_relevant_comments = sorted_df.head(selection_size).index.tolist()
    return least_relevant_comments
