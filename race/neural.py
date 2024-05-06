import pandas as pd
import numpy as np
from deepface import DeepFace
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from ethnicolr import pred_fl_reg_name_five_cat
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
    data = pd.read_csv(csv)
    data['deepface_race'] = data['image_path'].apply(get_deepface_race)
    data['ethnicolr_race'] = data.apply(lambda x: get_ethnicolr_race(x['firstname'], x['lastname']), axis=1)
    data['features'] = data.apply(extract_features, axis=1).fillna(0)
    X = pd.DataFrame(data['features'].tolist())
    X.fillna(0, inplace=True)
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(data['true_race'])
    y = to_categorical(y)
    return X, y

def build_model(input_shape):
    model = Sequential([
        Dense(64, input_shape=(input_shape,), activation='relu'),
        Dropout(0.3),
        Dense(32, activation='relu'),
        Dropout(0.3),
        Dense(4, activation='softmax')
    ])
    model.compile(optimizer=Adam(lr=0.001), loss='categorical_crossentropy', metrics=['accuracy'])
    return model

model_filename = '' #path to model
if os.path.exists(model_filename):
    model = load_model(model_filename)
    print("Loading Existing Model")
else:
    print("Training New Model")
    X, y = collect_data('') #path to mdoel
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = build_model(X_train.shape[1])
    model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))
    model.save(model_filename)
    print("Model trained and saved.")

loss, accuracy = model.evaluate(X_test, y_test)
print(f"Model accuracy: {accuracy * 100:.2f}%")
