import pandas as pd
from deepface import DeepFace
from ethnicolr import pred_fl_reg_name_five_cat
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from joblib import dump, load
import os
import csv

def get_deepface_race(image_path):
    # Function to get predictions from DeepFace
    try:
        result = DeepFace.analyze(img_path=image_path, enforce_detection=False, actions=['race'])
        dominant_race = result[0]['dominant_race']
        return dominant_race
    except Exception as e:
        print(f"Error analyzing image: {e}")
        return "Error"

def get_ethnicolr_race(firstname, lastname):
    # Create a DataFrame with the first and last name
    row = {'firstname': firstname, 'lastname': lastname}
    # Call the ethnicolr function using the row data
    predictions = pred_fl_reg_name_five_cat(pd.DataFrame([row]), 'lastname', 'firstname').iloc[0]
    # Extract the desired result
    return predictions.to_dict()

def get_last_name(person_id):
    # Filter the DataFrame for the row where 'personid' matches the provided PersonID
    data = pd.read_csv("") #csv file that has personid, firstname, lastname, and final classification for each individual
    row = data[data['personid'] == person_id]
    # Extract the 'lastname' from the filtered row
    if not row.empty:
        last_name = row['lastname'].values[0]
        first_name = row['FirstName'].values[0]
        return (first_name, last_name)
    else:
        return "PersonID not found"

def extract_features(row):
    features = []
    # Handle DeepFace race results with conditional weighting
    races = ['white', 'black', 'asian', 'hispanic']  # example list of races
    for race in races:
        if race == 'black' and row['deepface_race'] == race:
            weight = 10  # Higher weight for black
        else:
            weight = 1  # Standard weight for other races
        features.append(weight if row['deepface_race'] == race else 0)
    
    # Handle ethnicolr race predictions with standard weight
    if row['ethnicolr_race']:
        for race in ['pctwhite', 'pctblack', 'pctasian', 'pcthispanic']: 
            score = row['ethnicolr_race'].get(race, 0)
            try:
                features.append(float(score) if pd.notna(score) and score != '(S)' else 0)
            except ValueError:
                features.append(0)
    
    return features

    
    return features

def collect_data(csv):
    # Collecting data and labels (simulated process)
    data = pd.read_csv(csv)

    # Applying prediction functions
    data['deepface_race'] = data['image_path'].apply(get_deepface_race)
    data['ethnicolr_race'] = data.apply(lambda x: get_ethnicolr_race(x['firstname'], x['lastname']), axis=1)

    # Apply feature extraction and handle NaNs directly in the DataFrame
    data['features'] = data.apply(extract_features, axis=1).fillna(0)  # Filling NaN values with 0 after feature extraction

    # Convert list of lists to a DataFrame or suitable structure for training
    X = pd.DataFrame(data['features'].tolist())  # Convert feature lists into a DataFrame
    X.fillna(0, inplace=True)  # Ensure no NaN values remain
    y = data['true_race']

    return (X, y)

# Load the pre-trained model
model_filename = '' #path to the trained model
model = load(model_filename)

def get_person_details(person_id, data):
    row = data[data['PersonID'] == person_id]
    return row

# Function to make predictions with the loaded or newly trained model
def model_prediction(new_image_path, firstname, lastname):
    new_image_features = get_deepface_race(new_image_path)
    new_name_features = get_ethnicolr_race(firstname, lastname)
    new_features = extract_features({'deepface_race': new_image_features, 'ethnicolr_race': new_name_features})
    prediction = model.predict([new_features])
    print("prediction:", prediction)
    return prediction

# Load the titles data to check conditions
characteristics = pd.read_csv("") #csv file that contains a personid's involvement in an alumni org

results = []

def make_prediction(image_path):
    person_id = image_path.split(".")[0]
    person_details = get_person_details(person_id, characteristics)

    if not person_details.empty and person_details.iloc[0]['keyword_count'] == 1:
        race = person_details.iloc[0]['race']
    else:
        firstname, lastname = get_last_name(person_id)[0], get_last_name(person_id)[1]
        race = model_prediction(image_path, firstname, lastname)

    results.append({'personid': person_id, 'predicted_race': race})

# Convert results to DataFrame and save to CSV
make_prediction("") #image_path
results_df = pd.DataFrame(results)
results_df.to_csv("") #save to desired file of choice
