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
    data = pd.read_csv("")  #csv file that has personid, firstname, lastname, and final classification for each individual
    row = data[data['personid'] == person_id]
    # Extract the 'lastname' from the filtered row
    if not row.empty:
        last_name = row['lastname'].values[0]
        return last_name
    else:
        return "PersonID not found"

def extract_features(row):
    features = []
    # Adjust weight for race predictions based on the 'black' race condition
    if row['deepface_race'] == 'black':
        deepface_weight = 0.51
        ethnicolr_weight = 0.49
    else:
        deepface_weight = 0.5
        ethnicolr_weight = 0.5
    
    # Accumulate features based on race predictions and their weights
    races = ['white', 'black', 'asian', 'hispanic']  # Example list of races
    for race in races:
        # Add weighted feature based on 'deepface_race' prediction
        deepface_feature = deepface_weight if row['deepface_race'] == race else 0
        # Add weighted feature based on 'ethnicolr_race' prediction
        ethnicolr_feature = ethnicolr_weight * float(row.get('ethnicolr_race', {}).get(f'pct{race}', 0))
        # Sum the features for each race
        features.append(deepface_feature + ethnicolr_feature)
    
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

# Function to make predictions with the loaded or newly trained model
def make_predictions(new_image_path, new_last_name):
    new_image_features = get_deepface_race(new_image_path)
    new_name_features = get_ethnicolr_race(new_last_name)
    new_features = extract_features({'deepface_race': new_image_features, 'ethnicolr_race': new_name_features})
    prediction = model.predict([new_features])
    return prediction

# Check if a previously trained model exists
model_filename = '' #path to model
if os.path.exists(model_filename):
    # Load the existing model
    print("Loading Existing Model")
    model = load(model_filename)

    folder_path = ""
    count = 0
    for image in os.listdir(folder_path):
        image_path = os.path.join(folder_path, image)
        personid = image.split(".")[0]
        lastname = get_last_name(personid)

else:
    # No model exists, train a new one
    print("Training New Model")
    info = collect_data('') #path to model
    X, y = info[0], info[1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Save the newly trained model
    dump(model, model_filename)
    
    # Evaluate model if it's newly trained
    y_pred = model.predict(X_test)
    print("Accuracy of newly trained model:", accuracy_score(y_test, y_pred))