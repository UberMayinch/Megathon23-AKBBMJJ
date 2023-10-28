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


# Route for the form page
@app.route('/')
def form():
    return render_template('form.html')

# Route to handle form submission
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

        return "Data received and stored successfully!"

if __name__ == '__main__':
    app.run(debug=True)
