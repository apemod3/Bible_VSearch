from flask import Flask, render_template, request
import random
import re

app = Flask(__name__)

def read_bible_verses(filename):
    with open(filename, 'r') as file:
        verses = file.readlines()
    return verses

def search_exact_keyword(keyword, verses):
    matching_verses = []
    for verse in verses:
        if re.search(r'\b' + re.escape(keyword.lower()) + r'\b', verse.lower()):
            matching_verses.append(verse.strip())
    return matching_verses

def get_random_verses(matching_verses):
    if len(matching_verses) <= 3:
        return matching_verses
    else:
        return random.sample(matching_verses, 3)

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    closing_message = None
    if request.method == 'POST':
        keyword = request.form['keyword']
        verses = read_bible_verses("bible.txt")
        matching_verses = search_exact_keyword(keyword, verses)
        if not matching_verses:
            result = "No matching verses found."
        else:
            random_verses = get_random_verses(matching_verses)
            result = [f"- {verse}" for verse in random_verses]
            closing_message = f"These are the verses regarding {keyword} from the Bible. God bless you for seeking the word of God."
    return render_template('index.html', result=result, closing_message=closing_message)

if __name__ == '__main__':
    app.run(debug=True)