import os
import spacy
import csv
import gender_guesser.detector as gender
import wikipediaapi

# Wikipedia API setup
wiki_wiki = wikipediaapi.Wikipedia(user_agent="DataScienceProject/1.0", language='en')

# The topic to analyze
topic_title = "Artificial Intelligence"

# Load the English NLP model
nlp = spacy.load("en_core_web_sm")

def detect_gender(name):
    """Detects the gender of a person based on their first name."""
    d = gender.Detector()
    name_parts = name.split()
    first_name = name_parts[0] if name_parts else name
    gender_result = d.get_gender(first_name)
    
    if gender_result in ['male', 'mostly_male']:
        return 'Male'
    elif gender_result in ['female', 'mostly_female']:
        return 'Female'
    else:
        return 'Unknown'

def is_person_name(text):
    """Checks if the given text is recognized as a person's name."""
    doc = nlp(text)
    return any(ent.label_ == "PERSON" for ent in doc.ents)

def process_page(title):
    """Fetches links for a Wikipedia page and determines the gender of identified persons."""
    page = wiki_wiki.page(title)
    if not page.exists():
        return []

    links = list(page.links.keys())
    person_data = []
    
    for link in links:
        if is_person_name(link):
            gender_result = detect_gender(link)
            person_data.append((link, gender_result))
    
    print(f"Found {len(person_data)} persons in the page.")
    return person_data

def save_to_csv(topic, person_data):
    """Saves identified names and genders to a CSV file."""
    filename = f"{topic}_Linked People.csv"
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Gender"])
        writer.writerows(person_data)
    print(f"Data saved to {filename}")

# Process the specified topic page and save results
data = process_page(topic_title)
save_to_csv(topic_title.replace(" ", "_"), data)
