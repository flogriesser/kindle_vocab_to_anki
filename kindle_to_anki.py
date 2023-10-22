import sqlite3
import csv
from googletrans import Translator, LANGUAGES

# Replace with the path to your actual SQLite database file
database_file = "vocab.db"

# Name of the output CSV file
csv_file_name = "translated_words.csv"

# Translate the word to your language
target_language = 'de'

table_name = "WORDS"

# Create a Translator object
translator = Translator()

try:
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    query = f"SELECT word FROM {table_name} WHERE id NOT LIKE 'de:%';"
    cursor.execute(query)

    rows = cursor.fetchall()

    if len(rows) == 0:
        print(f"No entries found under specified conditions in the table {table_name}.")
    else:
        with open(csv_file_name, mode='w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)

            csv_writer.writerow(["Original Word", "Translated Word"])

            for row in rows:
                try:
                    original_word = row[0]
                    print(original_word)

                    translated = translator.translate(original_word, dest=target_language)
                    translated_word = translated.text
                    
                    csv_writer.writerow([original_word, translated_word])
                except:
                    print("NO Translation for:" + str(row))

        print(f"Words and their translations have been exported to '{csv_file_name}' successfully.")

except sqlite3.Error as e:
    print(f"An SQLite error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    if conn:
        conn.close()
