import csv

senior_titles = [
    "Partner",
    "Director",
    "Principal",
    "President",
    "Executive",
    "Chief",
    "Manager",
    "Senior",
    "Head",
    "Founder",
    "Co-founder", 
    "Chairman", 
    "Co-founding", 
    "Owner", 
    "Founding"
]

senior_titles_lower = [title.lower() for title in senior_titles]

# Function to check if any word in the line matches senior titles
def check_line(line):
    words = line.split('&')
    for word in words:
        # Convert the word to lowercase for comparison
        word = word.strip().lower()
        # Check if any senior title is in the word
        for title in senior_titles_lower:
            if title in word:
                return True  # Return True if any title matches
    for word in words:
        # Print each word and ask the user whether to keep it
        print(word) 
        user = input("keep?\n")
        if user == "y":
            return True  # Return True if the user chooses to keep the word
    return False  # Return False if no title or user-approved word is found

with open('relevant_titles.csv', 'r') as file, open('titles.txt', 'w') as output:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        line = ','.join(row) 
        # If no senior title is found in the line, write it to the output file
        if not check_line(line):
            output.write(line + '\n')

