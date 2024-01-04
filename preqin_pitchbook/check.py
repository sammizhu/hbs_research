import csv

with open('Preqin_PitchBook_org.csv', 'r') as file:
    reader = csv.reader(file)
    
    with open('Preqin_PitchBook.csv', 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        
        for row in reader:
            Fund_Name = row[4].strip()
            fundname = row[5].strip()
            if Fund_Name == fundname:
                writer.writerow(row)
            else:
                print(Fund_Name, " -- ", fundname)
                
                # Ask the user if they want to keep this line
                user_input = input("Keep?: ")
                
                # If the user wants to keep the line, write it to the new file
                if user_input.lower() == 'n':
                    print("Line not kept.")
                else:
                    writer.writerow(row)
                    print("Line written to output.csv")

print("Process completed.")
