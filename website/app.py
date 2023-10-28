from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Create a database connection and a cursor
conn = sqlite3.connect('social_media.db')
cursor = conn.cursor()

# Create a table to store social media handles
# Create a table to store social media handles with email as primary key
cursor.execute('''
    CREATE TABLE IF NOT EXISTS social_media (
        email TEXT PRIMARY KEY,
        instagram TEXT,
        linkedin TEXT,
        facebook TEXT,
        twitter TEXT
    )
''')
conn.commit()
conn.close()


# Establish connection and create the database file
conn = sqlite3.connect('questionnaire.db')
cursor = conn.cursor()

# Create a table to store user data and questionnaire responses
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_responses (
        email TEXT,
        question_id TEXT,
        category TEXT,
        answer INTEGER
    )
''')

conn.commit()
conn.close()

current_question = 0

questions = [
    {'question': 'This is a sample statement.', 'id': 'question1', 'category':'abcd'},
    {'question': 'This is another sample statement.', 'id': 'question2', 'category':'abef'}
    # Add more questions in the same format
]

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        email = request.form['email']
        instagram = request.form['instagram']
        linkedin = request.form['linkedin']
        facebook = request.form['facebook']
        twitter = request.form['twitter']

        # Store the data in the SQLite database
        conn = sqlite3.connect('social_media.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO social_media (email, instagram, linkedin, facebook, twitter)
            VALUES (?, ?, ?, ?, ?)
        ''', (email, instagram, linkedin, facebook, twitter))
        conn.commit()
        conn.close()

        global current_question
        question = questions[current_question]['question']
        global question_id
        question_id = questions[current_question]['id']

        return render_template('question.html', question_no=current_question+1, question=question, question_id=question_id)

@app.route('/Done', methods=['POST'])
def Done():
    if request.method == 'POST':
        global current_question
        email = 'example@example.com'  # Replace with the email from the previous form submission
        global question_id 
        answer = request.form['answer']
        question_cat=questions[current_question]['category']
        # Establish a connection to the database
        conn = sqlite3.connect('questionnaire.db')
        cursor = conn.cursor()

        # Insert the questionnaire answer along with the question ID into the database
        cursor.execute('''
            INSERT INTO user_responses (email, question_id, category, answer)
            VALUES (?, ?, ?, ?)
        ''', (email, question_id, question_cat, answer))

        conn.commit()
        conn.close()

        current_question += 1  # Move to the next question
        if current_question < len(questions):
            question = questions[current_question]['question']
            question_id = questions[current_question]['id']
            return render_template('question.html', question_no=current_question+1, question=question, question_id=question_id)
        else:
            return "Thank you for completing the questionnaire!"

if __name__ == '__main__':
    app.run(debug=True)
