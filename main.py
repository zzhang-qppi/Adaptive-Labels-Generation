from initial_label_generation import generate_labels_from_many_posts
from label_refinement import search_for_new_labels_in_posts, select_posts_less_relevant_to_existing_labels
import json
from random import sample
import pandas as pd

def create_initial_labels_from_random_samples(posts, sample_size, save_path):
    samples = sample(posts, sample_size)
    labels = generate_labels_from_many_posts(samples, cleaning_period=30)
    with open(save_path, 'w') as outfile:
        json.dump(labels, outfile)

def create_new_labels_in_least_relevant_posts(labeled_posts_df, selection_size, save_path):
    labels = labeled_posts_df.columns.to_list()
    selected_posts = select_posts_less_relevant_to_existing_labels(labeled_posts_df, selection_size)
    new_labels = search_for_new_labels_in_posts(selected_posts, labels)
    with open(save_path, 'w') as outfile:
        json.dump({"current": labels, "expansion": new_labels}, outfile)

if __name__ == "__main__":
    ### 初始标签生成 ###
    all_posts = []  # 所有帖子内容，
    # 随机取样，参数：样本大小，标签保存地址
    create_initial_labels_from_random_samples(all_posts, 100, "labels/labels_1.0.json")
    
    ### 标签迭代，更新 ###
    labeled_posts_df = pd.DataFrame()  # 打标完成的文件，columns为标签，index为帖子内容
    # 检测与当前标签集适配性差的帖子，从这些帖子中生成新的补充标签，参数：选择的帖子数量大小，补充标签保存地址
    create_new_labels_in_least_relevant_posts(labeled_posts_df, 100, "labels/expansion_to_labels_1.0(待人工检查).json")