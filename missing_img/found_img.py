import csv
import os

# Path to the CSV file
csv_file_path = 'r.csv'

# Path to the folder containing images
image_folder_path = 'missing_images'

# Function to check if image exists in the folder
def check_image_existence(image_name):
    image_path = os.path.join(image_folder_path, image_name)
    return os.path.exists(image_path)
i = 0
# Open the CSV file for reading
with open(csv_file_path, 'r') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    fieldnames = csv_reader.fieldnames + ['found']
    
    # Create a new CSV file for writing with the additional 'found' column
    with open('updated_file.csv', 'w', newline='') as updated_csv_file:
        csv_writer = csv.DictWriter(updated_csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        
        # Iterate through each row in the original CSV
        for row in csv_reader:
            image_name = row.get('image_name_new')
            if image_name:
                if check_image_existence(image_name):
                    i+=1
                    print(f"{i}")
                    row['found'] = 'Yes'
            csv_writer.writerow(row)

