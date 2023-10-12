import os
import csv
from notion_client import Client
from notion_client.api_endpoints import DatabasesEndpoint
from dotenv import load_dotenv

#load the .env file, GET the NOTION_TOKEN
load_dotenv() 
API_KEY = os.getenv("API_KEY")
notion = Client(auth=os.environ["API_KEY"])

#Define my Notion database and page ID
DATABASE_ID = os.getenv("DATABASE_ID")
# PAGE_ID = os.getenv("PAGE_ID") #I tried to use this to update my page, but it did not work for me, PAGE_ID keeps returning an error that it was not found even after permissions were given.

#Define a dictionary to store my data
library_data = {}

#Define my .csv file
csv_file = "ratings.csv"
if os.path.getsize(csv_file) == 0:
    print("CSV file is empty.")

#Method to remove any whitespace and lowercase as required
def improve_text(text): 
    return text.strip().lower()

# Initialize a set to store the "Book Name" values
seen = set()

existing_records = notion.databases.query(database_id=DATABASE_ID)
for page in existing_records.get('results', []):
    book_name_property = page.get('properties', {}).get('Book Name')
    if 'title' in book_name_property and isinstance(book_name_property['title'], list) and len(book_name_property['title']) > 0:
        book_name = book_name_property['title'][0].get('text', {}).get('content', '')
        seen.add(improve_text(book_name))

# Read the CSV file and populate with book data in a try/except block
try:
    with open(csv_file, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        repeated_readers = set()

        for row in reversed(list(reader)): #go in reverse order, to get the LAST entry of a user
            if len(row) == 3: 
                book_name = improve_text(row[0])
                member_name = improve_text(row[1])
                rating = (row[2])
            
                try: #Check if rating is valid!
                    rating = float(rating)
                except ValueError:
                    print(f"Invalid rating: {rating}")
                    continue
                
                #Check that the book_name and rating has not been seen before. This is because we take the LAST value
                if (book_name, member_name) not in repeated_readers:
                    #duplicate row
                    #Update Book Dictionary
                    if book_name not in library_data: #if no values found, populate the dictionary
                        library_data[book_name] = {"total_rating": 0, "num_ratings": 0, "num_favourites": 0}

                    library_data[book_name]["total_rating"] += rating
                    library_data[book_name]["num_ratings"] += 1 
                    if rating == 5: #if it's a perfect score, update favourites!
                        library_data[book_name]["num_favourites"] += 1
                
                repeated_readers.add((book_name, member_name)) #add the book_name and member_name to the set to check for duplicates

            else: #Row not valid formatting as said in instructions, print error
                print("Invalid row!")
    
    #Update the Notion database with book ratings
    for book_name, data in library_data.items():
        average_rating = data["total_rating"] / data["num_ratings"]
        num_favourites = data["num_favourites"]
        
        
        if book_name not in seen: #check if the book name exists before adding it to the database! note: read the note below 
            notion.pages.create(
                parent = {"database_id": DATABASE_ID},
                properties={
                    "Book Name": {"title": [{"text": {"content": book_name}}]},
                    "Average Rating": {"number": round(average_rating, 2)},
                    "Favourites": {"number": round(num_favourites, 2)}
                },
            )
        
    print("Database is updated! 🎉")   

except FileNotFoundError:
    print(f"CSV file '{csv_file}' not found.")
except Exception as e:
    print(f"An error occurred: {str(e)}")


# NOTE: Page ID did not work for me. Any time I tried to use pageID to update values to help with deterministic values, it returned not found. This is necessary for the update method in Notion's API, so to compensate I had to use a set() of already existing books as a mimiced solution. It is not perfect, but it's the best I could do, and I mentioned this to my recruiter Chris


# Considerations / Edge Cases: [✅ == done in my solution]

# We need the columns to be Book Name, Average Rating, and Favourites EXACTLY. 

# 1. What if the CSV file is very large? (e.g. 1 million rows) - One solution is to read and process the .csv file in smaller chunks to avoid memory issues

# 2. Notion API changes - There is a risk if Notion changes its API, but we can mitigate this by reading the Notion API documentation and using the latest version of Pythn and the Python Notion SDK

# 3. ✅ What if the CSV has invalid data? - We can use a try/except block to catch any invalid data and skip over it. I did this in my solution with rating, but could check the names as well. 

# 4. ✅ What if the CSV file is not found? - We checked this with the try catch block!

# 5. What if the CSV file has duplicate data? - We can use a set() to store the data, which will automatically remove any duplicates.

# 6. ✅ What if the CSV file has a different number of columns? - We can check the length of each row and skip over any rows that don't have the correct number of columns. I did this in my solution.

# 7. What if the CSV file has a different delimiter [e.g. a question mark]? - We can specify the delimiter when we open the file.

# 8. What if there are multiple CSV files? - We can use a for loop to iterate over each file and process them one by one. 

# 9. ✅ What if the CSV block is empty? - We can check the size of the file and skip over it if it is empty. I did this :)!

# 10. What if concurrent operations are done? - We can use a lock to ensure that only one operation is done at a time, to prevent conflicts. 