import os
import pandas as pd
import json
from collections import deque

# Function to extract data from a combined file
def extract_combined_data(file_path):
    # Define a deque with a maximum length of 6
    last_6_lines = deque(maxlen=6)

    # Open the file in binary mode
    with open(file_path, 'rb') as file:
        # Iterate through each line in the file
        for line in file:
            # Decode the line and strip whitespace
            decoded_line = line.decode().strip()

            # Add the decoded line to the deque
            last_6_lines.append(decoded_line)

    # Extract the required information from the last 6 rows
    followers_line = last_6_lines[-4]
    following_line = last_6_lines[-1]

    # Split the lines to get followers and following
    followers = followers_line.split(',')
    following = following_line.split(',')

    # Extract username from the filename without extension
    user = os.path.splitext(os.path.basename(file_path))[0]
    user = user[:-5]  # Subtract the last 5 characters

    # Load movies information from the rest of the file
    movies_df = pd.read_csv(file_path, skipfooter=6, engine='python')

    # Convert stars in the Rating column to a numeric value
    movies_df['Rating'] = movies_df['Rating'].apply(lambda x: len(x) if isinstance(x, str) and '★' in x else (len(x) + 0.5) if isinstance(x, str) and '½' in x else x)
    
    # Replace NaN values in 'Review' with "null"
    movies_df['Review'] = movies_df['Review'].apply(lambda x: None if pd.isna(x) else x)

    return user, followers, following, movies_df

# Path to the folder containing combined files
folder_path = "userdata/"

# Create a folder for output files if it doesn't exist
output_folder = "output_data"
os.makedirs(output_folder, exist_ok=True)

# Create empty lists to store information
follow_info_list = []
movies_info_list = []

# Original user list from file names
original_users = set(os.path.splitext(f)[0][:-5] for f in os.listdir(folder_path) if f.endswith('.csv'))

# Iterate through each combined file in the folder
for file in os.listdir(folder_path):
    if file.endswith('.csv'):
        file_path = os.path.join(folder_path, file)

        # Extract information from the combined file
        user, followers, following, movies_df = extract_combined_data(file_path)

        # Filter followers and followees based on original_users
        filtered_followers = [follower for follower in followers if follower in original_users]
        filtered_following = [followee for followee in following if followee in original_users]

        # Add the following and follower information to the list
        follow_info_list.append({
            'User': user,
            'Followers': filtered_followers,
            'Following': filtered_following
        })

        # Add the movie review data to the list
        movies_info_list.append({
            'User': user,
            'Movies': movies_df.to_dict(orient='records')
        })

# Save follower and following information to a JSON file
output_follow_info_path_json = os.path.join(output_folder, "output_follow_information.json")
with open(output_follow_info_path_json, 'w') as json_follow_file:
    json.dump(follow_info_list, json_follow_file, indent=2)

# Save follower and following information to a CSV file
output_follow_info_path_csv = os.path.join(output_folder, "output_follow_information.csv")
follow_df = pd.DataFrame(follow_info_list)
follow_df.to_csv(output_follow_info_path_csv, index=False)

# Save movie review data to a JSON file
output_movies_info_path_json = os.path.join(output_folder, "output_movies_information.json")
with open(output_movies_info_path_json, 'w') as json_movies_file:
    json.dump(movies_info_list, json_movies_file, indent=2)

# Save movie review data to a CSV file with selected string columns enclosed in quotes
output_movies_info_path_csv = os.path.join(output_folder, "output_movies_information.csv")
movies_df_concatenated = pd.concat([pd.DataFrame(data['Movies']).assign(User=data['User']) for data in movies_info_list], ignore_index=True)

"""
# Enclose selected string columns in quotes if they exist
string_columns = ['Movie', 'Review']  # Add more columns if needed
for col in string_columns:
    movies_df_concatenated[col] = "'" + movies_df_concatenated[col] + "'"
"""

movies_df_concatenated.to_csv(output_movies_info_path_csv, index=False)

