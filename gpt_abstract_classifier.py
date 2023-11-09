from openai import OpenAI
import os
import csv

# authentication
key = os.environ.get("OPENAI_API_KEY")
client = OpenAI()

# text files
criteria_file = (
    "/Users/jacksonleb/Desktop/Fall2023/Jonides/GPTAbstractClassification/criteria.txt"
)
original_study_file = "/Users/jacksonleb/Desktop/Fall2023/Jonides/GPTAbstractClassification/yantis-jonides1984.txt"


with open(criteria_file, "r") as file:
    # Read the entire contents of the file into a variable
    criteria_text = file.read()

with open(original_study_file, "r") as file:
    # Read the entire contents of the file into a variable
    original_study_text = file.read()

# prompt set up
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": f"Read the following academic paper abstract: {original_study_text}",
        },
        {
            "role": "user",
            "content": f"I will be giving you a set of abstracts from papers that reference the academic paper I just gave you, You should choose an abstract if it fits the following criteria: {criteria_text}",
        },
    ],
)

csv_file_path = "/Users/jacksonleb/Desktop/Fall2023/Jonides/GPTAbstractClassification/JEP_ 1990 Citation Abstracts for RA Coding - Jackson.csv"

data_to_write = [
    ["Response", "Author"],
]

with open(csv_file_path, "r") as file:
    # Create a CSV reader object
    csv_reader = csv.reader(file)
    next(csv_reader)  # skip header
    i = 0
    # Iterate over each row in the CSV file
    for row in csv_reader:
        print(i)
        i += 1
        # Each row is a list of values
        abstract_text = row[6]
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f"Reply just yes or no, does the following abstract fit the criteria previously mentioned: {abstract_text}",
                }
            ],
        )
        data_to_write.append([response.choices[0].message.content, "GPT"])
        print(response.choices[0].message.content)
        print("____")

with open(
    "/Users/jacksonleb/Desktop/Fall2023/Jonides/GPTAbstractClassification/response.csv",
    "w",
    newline="",
) as file:
    # Create a CSV writer object
    csv_writer = csv.writer(file)

    # Write data to the CSV file
    csv_writer.writerows(data_to_write)
