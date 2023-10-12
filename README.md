# Book Ratings Notion Database Updater

This Python script is designed to read book ratings data from a CSV file and update a Notion database with the following information for each book:

- Book Name
- Average Rating
- Number of "Favorites" (ratings of 5 stars)

## Requirements

To use this script, you need the following:

1. A Notion account.
2. A Notion API key, which you can obtain by following the [Notion API documentation](https://developers.notion.com/docs/getting-started). You must have the API key set up with the token pasted in .env before starting.
3. A Notion database where you want to store the book ratings data. Make sure to create the database with the following properties:

   - Book Name (Title)
   - Average Rating (Number)
   - Favourites (Number)

4. A CSV file containing the book ratings data, with each row having three fields: book name, member name, and book rating.

## Setup

1. Clone or download this repository to your local machine.

2. Install the required Python3 packages by running the following command:

   ```
   pip3 install notion-client python-dotenv
   ```

3. Create a `.env` file in the same directory as the script and add your Notion API key as follows:

   ```
   API_KEY=your_api_key_here
   ```

4. Replace the following variables in the script with your own values:

   - `DATABASE_ID`: Set this to the ID of your Notion database where you want to store the book ratings data, this being a table! Make sure to have the exact names necessary!
   - `csv_file`: Set this to the path of your CSV file containing the book ratings data. In our case, it was ratings.csv

## Usage

Run the script using Python:

```
python3 Notion.py
```

I personally chose to run my code in Visual Studio Code instead! Simply click Run, then click Run Python File!

## Script Behavior

The script performs the following tasks:

- Reads the book ratings data from the specified CSV file.
- Normalizes the book names and member names (removes extra whitespace and converts to lowercase).
- Calculates the average rating and counts the number of "Favourites" (ratings of 5 stars) for each book.
- Updates the Notion database with the book ratings data, including book name, average rating, and number of "Favourites."

## Error Handling

The code includes error handling for the following cases:

- Empty CSV file: If the CSV file is empty, it prints a message.
- Invalid data in the CSV: It checks for rows with an incorrect number of fields and rows with invalid ratings (non-numeric).
- FileNotFoundError: If the specified CSV file is not found, it prints an error message.
- General Exception: It handles other exceptions gracefully and prints an error message.

## Edge Cases

The code handles various edge cases, including empty CSV files, invalid data, and more. Read the comments in the .py file to find more!

Feel free to modify the script to fit your specific requirements and database schema. 

## Thank you! - josh  

Note: Would've added test files with more time, universal standard. Remember to cd into the Notion directory before running!


## FAQ / Questions:


I did admittedly almost get stuck on connecting my page to my integration, until I googled on Stackoverflow to figure it out.

I understand this was done to develop more understanding of the API as well as Notion, so that isn't a complaint for me. Really, I enjoyed this takehome exercise.

The main thing I would say is to have more documentation on why specific errors show up. For example, I don't know why document ID worked for me every time, whilst Page ID failed, even if the guides to get both online say the same thing. I couldn't get PAGEID to work for Notion's .update() for their database. I decided to make an alternative solution using dictionaries and sets to make it work out. 

No real major open source libraries were used, we used Python's major libraries as well as Notion's! 