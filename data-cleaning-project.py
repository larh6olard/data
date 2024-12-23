import pandas as pd
import numpy as np

user_health_path = "datasets/user_health_data.csv"
supplement_usage_path = "datasets/supplement_usage.csv"
experiments_path = "datasets/experiments.csv"
user_profiles_path = "datasets/user_profiles.csv"

def merge_all_data(user_health_file, supplement_usage_file, experiments_file, user_profiles_file):

    user_health_data = pd.read_csv(user_health_file, parse_dates=['date'])
    supplement_usage_data = pd.read_csv(supplement_usage_file, parse_dates=['date'])
    experiments_data = pd.read_csv(experiments_file)
    user_profiles_data = pd.read_csv(user_profiles_file)

    supplement_usage_data['dosage_grams'] = supplement_usage_data['dosage'] / 1000

    experiments_data['experiment_name'] = experiments_data['name']

    user_health_data['sleep_hours'] = user_health_data['sleep_hours'].str.lower().str.strip('h').astype(float)

    ranges = [0, 18, 26, 36, 46, 56, 66, np.inf]
    group_names = ['Under 18', '18-25', '26-35', '36-45', '46-55', '56-65', 'Over 65']

    user_profiles_data['user_age_group'] = pd.cut(user_profiles_data['age'], bins=ranges,
                                             labels=group_names).astype(str).replace({'nan': 'Unknown'})

    sup_exp_merge = pd.merge(supplement_usage_data, experiments_data, on='experiment_id', how='left')
    health_sup_exp_merge = user_health_data.merge(sup_exp_merge, on=['user_id', 'date'], how='left')
    all_merged = health_sup_exp_merge.merge(user_profiles_data, on='user_id', how='left')

    all_merged['supplement_name'] = all_merged['supplement_name'].fillna('No intake')

    final_columns = [
        'user_id', 'date', 'email', 'user_age_group', 'experiment_name', 'supplement_name',
        'dosage_grams', 'is_placebo', 'average_heart_rate', 'average_glucose', 'sleep_hours', 'activity_level'
    ]

    final_df = all_merged[final_columns]

    return final_df


df = merge_all_data(user_health_path, supplement_usage_path, experiments_path, user_profiles_path)

print(df)
