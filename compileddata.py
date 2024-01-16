import os
import pandas as pd
import json
from collections import deque
from fractions import Fraction

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

    # Convert DataFrame to a list of dictionaries
    movies_list = movies_df.to_dict(orient='records')

    return user, movies_list, followers, following

# Path to the folder containing combined files
folder_path = "userdata/"

# Output file for saving combined information
output_file_path = "output_combined_information.json"

# Create an empty list to store the combined information
combined_list = []

# Iterate through each combined file in the folder
for file in os.listdir(folder_path):
    if file.endswith('.csv'):
        file_path = os.path.join(folder_path, file)

        # Extract information from the combined file
        user, movies, followers, following = extract_combined_data(file_path)

        # Add the information to the combined list
        combined_list.append({
            'User': user,
            'Movies': movies,
            'Followers': followers,
            'Following': following
        })

# Save the combined information to a JSON file
with open(output_file_path, 'w') as json_file:
    json.dump(combined_list, json_file, indent=2)
