from flask import Flask, render_template, request
from flask import redirect
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


conn = sqlite3.connect('game.db')
cursor = conn.cursor()

# Create a table to store social media handles
# Create a table to store social media handles with email as primary key
cursor.execute('''
    CREATE TABLE IF NOT EXISTS games (
        email TEXT PRIMARY KEY,
        Achievements TEXT
        Time_Taken INT
        Score INT
    )
''')
conn.commit()
conn.close()

current_question = 0


questions = [
    # Openness to Experience
    {'id': 'question1', 'question': 'I enjoy trying new things.', 'category': 'Openness to Experience'},
    {'id': 'question2', 'question': 'I am intellectually curious.', 'category': 'Openness to Experience'},
    {'id': 'question3', 'question': 'I have a vivid imagination.', 'category': 'Openness to Experience'},
    {'id': 'question4', 'question': 'I appreciate art and beauty.', 'category': 'Openness to Experience'},
    {'id': 'question5', 'question': 'I like to explore new ideas.', 'category': 'Openness to Experience'},
    {'id': 'question6', 'question': 'I like to meet new people and go to gatherings.', 'category': 'Openness to Experience'},
    
    # Conscientiousness
    {'id': 'question7', 'question': 'I am organized and tidy.', 'category': 'Conscientiousness'},
    {'id': 'question8', 'question': 'I pay attention to detail.', 'category': 'Conscientiousness'},
    {'id': 'question9', 'question': 'I am responsible and reliable.', 'category': 'Conscientiousness'},
    {'id': 'question10', 'question': 'I follow a strict schedule.', 'category': 'Conscientiousness'},
    {'id': 'question11', 'question': 'I am diligent in my work.', 'category': 'Conscientiousness'},
    
    # Extroversion
    {'id': 'question12', 'question': 'I enjoy social gatherings and parties.', 'category': 'Extroversion'},
    {'id': 'question13', 'question': 'I am talkative and outgoing.', 'category': 'Extroversion'},
    {'id': 'question14', 'question': 'I feel comfortable in social situations.', 'category': 'Extroversion'},
    {'id': 'question15', 'question': 'I am energized by being around people.', 'category': 'Extroversion'},
    {'id': 'question16', 'question': 'I have a wide circle of friends.', 'category': 'Extroversion'},
    {'id': 'question17', 'question': 'I like to meet new people and go to gatherings.', 'category': 'Extroversion'},

    # Agreeableness
    {'id': 'question18', 'question': 'I am considerate and compassionate.', 'category': 'Agreeableness'},
    {'id': 'question19', 'question': 'I avoid conflicts and arguments.', 'category': 'Agreeableness'},
    {'id': 'question20', 'question': 'I am easy to get along with.', 'category': 'Agreeableness'},
    {'id': 'question21', 'question': 'I am sympathetic to others\' feelings.', 'category': 'Agreeableness'},
    {'id': 'question22', 'question': 'I often go out of my way to help others or resolve conflicts peacefully.', 'category': 'Agreeableness'},
    {'id': 'question23', 'question': 'It is important for me to maintain harmonious relationships with those around me.', 'category': 'Agreeableness'},

    # Neuroticism
    {'id': 'question24', 'question': 'I often feel anxious or nervous.', 'category': 'Neuroticism'},
    {'id': 'question25', 'question': 'I am easily upset or stressed.', 'category': 'Neuroticism'},
    {'id': 'question26', 'question': 'I worry about things.', 'category': 'Neuroticism'},
    {'id': 'question27', 'question': 'I often feel down or depressed.', 'category': 'Neuroticism'},
    {'id': 'question28', 'question': 'I am emotionally sensitive.', 'category': 'Neuroticism'}
]

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        global email
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
        global email
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
            return render_template('game.html')

@app.route('/game', methods=['POST'])
def game():
    if request.method == 'POST':
        global email
        game = request.form['game_option']
        # conn = sqlite3.connect('game.db')
        # cursor = conn.cursor()

        # cursor.execute('''
        #     INSERT INTO games (email, game_chosen)
        #     VALUES (?, ?)
        # ''', (email, game))

        # conn.commit()
        # conn.close()

        return redirect("https://supermarioplay.com/")

if __name__ == '__main__':
    app.run(debug=True)
