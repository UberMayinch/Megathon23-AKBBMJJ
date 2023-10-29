from tensorflow import keras
import tensorflow as tf
import pandas as pd
from flask import Flask, render_template, request, redirect
import sqlite3
import numpy as np
import random
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
        Achievements TEXT,
        Time_Taken INT,
        Score INT
    )
''')
conn.commit()
conn.close()

current_question = 0
qno = 0

# Create a dictionary to store scores for each category
OCEAN_scores = {
    'Openness to Experience': 0,
    'Conscientiousness': 0,
    'Extroversion': 0,
    'Agreeableness': 0,
    'Neuroticism': 0,
}
OCEAN_ambi = {
    'Openness to Experience': 1,
    'Conscientiousness': 1,
    'Extroversion': 1,
    'Agreeableness': 1,
    'Neuroticism': 1,
}

OCEAN_normalise = {
    'Openness to Experience': 0,
    'Conscientiousness': 0,
    'Extroversion': 0,
    'Agreeableness': 0,
    'Neuroticism': 0,
}

questions = [
    # Openness to experience
    {'id': 'question1', 'question': 'I enjoy trying new things.', 'categories': [
        ['Openness to Experience', 3], ['Agreeableness', 1], ['Neuroticism', 1]]},
    {'id': 'question2', 'question': 'I am intellectually curious.', 'categories': [
        ['Openness to Experience', 3], ['Conscientiousness', 1], ['Neuroticism', 1]]},
    {'id': 'question3', 'question': 'I have a vivid imagination.',
        'categories': [['Openness to Experience', 3]]},
    {'id': 'question4', 'question': 'I appreciate art and beauty.',
        'categories': [['Openness to Experience', 3]]},
    {'id': 'question5', 'question': 'I like to explore new ideas.',
        'categories': [['Openness to Experience', 3]]},
    # {'id': 'question6', 'question': 'I like to meet new people and go to gatherings.', 'categories': [['Openness to Experience',3]]},

    # Conscientiousness
    {'id': 'question7', 'question': 'I am organized and tidy.',
        'categories': [['Conscientiousness', 3], ['Neuroticism', 1]]},
    {'id': 'question8', 'question': 'I pay attention to detail.',
        'categories': [['Conscientiousness', 3]]},
    {'id': 'question9', 'question': 'I am responsible and reliable.',
        'categories': [['Conscientiousness', 3], ['Agreeableness', 1]]},
    {'id': 'question10', 'question': 'I follow a strict schedule.',
        'categories': [['Conscientiousness', 3]]},
    # {'id': 'question11', 'question': 'I am diligent in my work.', 'categories': [['Conscientiousness',3]]},

    # Extroversion
    # {'id': 'question12', 'question': 'I enjoy social gatherings and parties.', 'categories': [['Extroversion',3]]},
    # {'id': 'question13', 'question': 'I am talkative and outgoing.', 'categories': [['Extroversion',3]]},
    # {'id': 'question14', 'question': 'I feel comfortable in social situations.', 'categories': [['Extroversion',3]]},
    {'id': 'question15', 'question': 'I am energized by being around people.',
        'categories': [['Extroversion', 3]]},
    {'id': 'question16', 'question': 'I have a wide circle of friends.',
        'categories': [['Extroversion', 3]]},
    {'id': 'question17', 'question': 'I like to meet new people and go to gatherings.',
        'categories': [['Extroversion', 3], ['Openness to Experience', 1]]},

    # Agreeableness
    {'id': 'question18', 'question': 'I am considerate and compassionate.',
        'categories': [['Agreeableness', 3]]},
    {'id': 'question19', 'question': 'I avoid conflicts and arguments.',
        'categories': [['Agreeableness', 3]]},
    {'id': 'question20', 'question': 'I am easy to get along with.',
        'categories': [['Agreeableness', 3]]},
    {'id': 'question21', 'question': 'I am sympathetic to others\' feelings.',
        'categories': [['Agreeableness', 3]]},
    # {'id': 'question22', 'question': 'I often go out of my way to help others or resolve conflicts peacefully.', 'categories': [['Agreeableness',3]]},
    # {'id': 'question23', 'question': 'It is important for me to maintain harmonious relationships with those around me.', 'categories': [['Agreeableness',3]]},

    # Neuroticism
    {'id': 'question24', 'question': 'I often feel anxious or nervous.',
        'categories': [['Neuroticism', 3]]},
    {'id': 'question25', 'question': 'I am easily upset or stressed.',
        'categories': [['Neuroticism', 3]]},
    {'id': 'question26', 'question': 'I worry about things.',
        'categories': [['Neuroticism', 3]]},
    {'id': 'question27', 'question': 'I often feel down or depressed.',
        'categories': [['Neuroticism', 3]]},
    # {'id': 'question28', 'question': 'I am emotionally sensitive.', 'categories': [['Neuroticism',3]]}
]

asked = []


def find_best_question():
    req_trait = max(OCEAN_ambi, key=OCEAN_ambi.get)
    cur = len(questions)
    max_wt = 0
    for i in range(len(questions)):
        if i in asked:
            continue
        if cur == len(questions):
            cur = i
        q = questions[i]
        for j in q['categories']:
            if j[0] == req_trait:
                if j[1] > max_wt:
                    cur = i
                    max_wt = j[1]
    req_q = questions[cur]
    for j in req_q['categories']:
        if j[0] == req_trait:
            if j[1] > max_wt:
                cur = i
                max_wt = j[1]
        OCEAN_ambi[j[0]] = max(0, OCEAN_ambi[j[0]] - 0.05 * j[1])
    asked.append(cur)
    return cur


@app.route('/')
def form():
    return render_template('form.html')


name = ''


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        global email
        global name
        name = request.form['name']
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
        current_question = find_best_question()
        question = questions[current_question]['question']
        global question_id
        question_id = questions[current_question]['id']

        return render_template('question.html', question_no=current_question, question=questions[current_question]['question'], question_id=questions[current_question]['id'], OCEAN_scores=OCEAN_scores, OCEAN_ambi=OCEAN_ambi)


@app.route('/Done', methods=['POST'])
def Done():
    if request.method == 'POST':
        global current_question
        global qno
        global email
        global question_id
        answer = int(request.form['answer'])
        categories = questions[current_question]['categories']

        # Update scores for each category based on their weights
        for category, weight in categories:
            OCEAN_scores[category] += (weight * (answer/7))
            OCEAN_normalise[category] += weight

        # Establish a connection to the database
        conn = sqlite3.connect('questionnaire.db')
        cursor = conn.cursor()

        # Insert the questionnaire answer along with the question ID into the database
        for category, _ in categories:
            cursor.execute('''
                INSERT INTO user_responses (email, question_id, category, answer)
                VALUES (?, ?, ?, ?)
            ''', (email, question_id, category, answer))

        conn.commit()
        conn.close()

        current_question = find_best_question()

        qno += 1
        # current_question += 1  # Move to the next question
        if qno < 10:
            question = questions[current_question]['question']
            question_id = questions[current_question]['id']
            print(OCEAN_ambi, asked)
            return render_template('question.html', question_no=current_question + 1, question=question, question_id=question_id, OCEAN_scores=OCEAN_scores, OCEAN_ambi=OCEAN_ambi)
        else:
            # Normalize scores based on OCEAN_normalise values
            for category, weight in OCEAN_scores.items():
                if OCEAN_normalise[category] > 0:
                    OCEAN_scores[category] /= OCEAN_normalise[category]
            print(OCEAN_scores)
            return render_template('game.html')


@app.route('/game', methods=['POST'])
def game():
    if request.method == 'POST':
        return redirect('/result')


@app.route('/result', methods=['GET'])
def result():
    global email
    global name
    model = load_model()

    fin_score = []
    fin_score.append(OCEAN_scores['Openness to Experience'])
    fin_score.append(OCEAN_scores['Conscientiousness'])
    fin_score.append(OCEAN_scores['Extroversion'])
    fin_score.append(OCEAN_scores['Agreeableness'])
    fin_score.append(OCEAN_scores['Neuroticism'])

    df = pd.DataFrame(fin_score)

    dataset = pd.read_csv('data.csv')

    dataset = dataset.sample(frac=1)
    # print(dataset.head())
    # print(dataset.tail())
    features = dataset.iloc[:, :5].values
    labels = dataset.iloc[:, 5].values

    print(features.shape)

    model = keras.Sequential([
        keras.layers.Dense(64, activation='relu', input_shape=(5,)),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(32, activation='relu'),
        keras.layers.Dense(3, activation='softmax')  # Three output labels
    ])

    train_features = features[:8000]
    train_labels = labels[:8000]

    print(train_features.shape)
    print(train_labels.shape)

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    print(model.summary())
    model.fit(train_features, train_labels)

    df = df.transpose()
    print(df)
    pred = model.predict(df)
    print(pred)

    max = np.max(pred, axis=1)
    print(max)

    if max == pred[0][0]:
        job = 1
    elif max == pred[0][1]:
        job = 2
    else:
        job = 0
    return render_template('result.html', data=fin_score, name=name, job=job)


def load_model():
    dataset = pd.read_csv('data.csv')

    dataset = dataset.sample(frac=1)
    # print(dataset.head())
    # print(dataset.tail())
    features = dataset.iloc[:, :5].values
    labels = dataset.iloc[:, 5].values

    print(features.shape)

    global model
    model = keras.Sequential([
        keras.layers.Dense(64, activation='relu', input_shape=(5,)),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(32, activation='relu'),
        keras.layers.Dense(3, activation='softmax')  # Three output labels
    ])

    train_features = features[:8000]
    train_labels = labels[:8000]

    print(train_features.shape)
    print(train_labels.shape)

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    print(model.summary())
    model.fit(train_features, train_labels)
    return model


if __name__ == '__main__':
    app.run(debug=True)
    load_model()
