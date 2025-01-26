from flask import Flask, render_template, request, redirect, flash, url_for, g
import sqlite3

app = Flask(__name__, static_url_path='/static')
app.secret_key = "your_secret_key"  # Replace with your actual secret key

DATABASE = "feedback.db"

def get_db():
    """Get a database connection for the current request."""
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  # Return rows as dictionaries
    return g.db

@app.teardown_appcontext
def close_db(exception):
    """Close the database connection at the end of the request."""
    db = g.pop("db", None)
    if db is not None:
        db.close()

# Create feedback table if it doesn't exist
with sqlite3.connect(DATABASE) as conn:
    conn.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        rating INTEGER NOT NULL,
        comment TEXT
    )
    """)
    conn.commit()

# Common Feedback Functions
def fetch_feedbacks():
    """Fetch all feedbacks from the database."""
    db = get_db()
    return db.execute("SELECT * FROM feedback ORDER BY id DESC").fetchall()

def add_feedback(name, rating, comment):
    """Add a feedback entry to the database."""
    db = get_db()
    db.execute(
        "INSERT INTO feedback (name, rating, comment) VALUES (?, ?, ?)",
        (name, rating, comment if comment else None)
    )
    db.commit()

def delete_feedback_entry(feedback_id):
    """Delete a feedback entry by its ID."""
    db = get_db()
    db.execute("DELETE FROM feedback WHERE id = ?", (feedback_id,))
    db.commit()

# Routes
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form.get("name")
        rating = int(request.form.get("rating"))
        comment = request.form.get("comment")
        add_feedback(name, rating, comment)
        flash("Feedback submitted successfully!", "success")
        return redirect(url_for("home"))

    feedbacks = fetch_feedbacks()
    return render_template("home.html", feedbacks=feedbacks)

@app.route("/delete-feedback/<int:feedback_id>", methods=["POST"])
def delete_feedback(feedback_id):
    secret_key = request.form.get("secret_key")
    ADMIN_SECRET_KEY = "admin123"  # Replace with your admin secret key

    if secret_key != ADMIN_SECRET_KEY:
        flash("You are not authorized to delete feedback.", "danger")
        return redirect(request.referrer or url_for("home"))

    delete_feedback_entry(feedback_id)
    flash("Feedback deleted successfully!", "success")
    return redirect(request.referrer or url_for("home"))

@app.route('/calculation1', methods=['GET', 'POST'])
def calculation1():
    feedbacks = fetch_feedbacks()
    if request.method == 'POST':
        try:
            odd_sgpa = float(request.form['odd_sgpa'])
            even_sgpa = float(request.form['even_sgpa'])
            odd_subjects = int(request.form['odd_subjects'])
            even_subjects = int(request.form['even_subjects'])

            odd_percentage = (odd_sgpa * 10) - 7.5
            even_percentage = (even_sgpa * 10) - 7.5
            ygpa = (odd_sgpa + even_sgpa) / 2
            total_marks = (odd_subjects + even_subjects) * 100
            obtained_marks = ((odd_percentage * odd_subjects * 100) +
                              (even_percentage * even_subjects * 100)) / 100
            year_percentage = (obtained_marks / total_marks) * 100

            return render_template(
                'calculation1.html',
                feedbacks=feedbacks,
                odd_percentage=odd_percentage,
                even_percentage=even_percentage,
                ygpa=ygpa,
                total_marks=total_marks,
                obtained_marks=obtained_marks,
                year_percentage=year_percentage
            )
        except ValueError:
            flash("Invalid input! Please enter valid numbers.", "danger")
            return redirect(url_for("calculation1"))
    return render_template("calculation1.html", feedbacks=feedbacks)

@app.route('/calculation2', methods=['GET', 'POST'])
def calculation2():
    feedbacks = fetch_feedbacks()
    sgpa_percentage = None
    if request.method == 'POST':
        try:
            sgpa = float(request.form['odd_sgpa'])
            sgpa_percentage = (sgpa * 10) - 7.5
        except ValueError:
            flash("Invalid input! Please enter valid numbers.", "danger")
            return redirect(url_for("calculation2"))
    return render_template("calculation2.html", sgpa_percentage=sgpa_percentage, feedbacks=feedbacks)

@app.route('/calculation3', methods=['GET', 'POST'])
def calculation3():
    feedbacks = fetch_feedbacks()
    ygpa = None
    ygpa_percentage = None
    if request.method == 'POST':
        try:
            odd_sgpa = float(request.form['odd_sgpa'])
            even_sgpa = float(request.form['even_sgpa'])
            ygpa = (odd_sgpa + even_sgpa) / 2
            ygpa_percentage = (ygpa * 10) - 7.5
        except ValueError:
            flash("Invalid input! Please enter valid numbers.", "danger")
            return redirect(url_for("calculation3"))
    return render_template("calculation3.html", feedbacks=feedbacks, ygpa=ygpa, ygpa_percentage=ygpa_percentage)

@app.route('/calculation4', methods=['GET', 'POST'])
def calculation4():
    feedbacks = fetch_feedbacks()
    average_grade = None
    overall_percentage = None
    if request.method == 'POST':
        try:
            semester_count = int(request.form['semester_count'])
            sgpa_marks = [float(request.form[f'sgpa_sem{i}']) for i in range(1, semester_count + 1)]
            average_grade = sum(sgpa_marks) / len(sgpa_marks)
            overall_percentage = (average_grade * 10) - 7.5
        except (ValueError, KeyError):
            flash("Invalid input! Please enter valid numbers.", "danger")
            return redirect(url_for("calculation4"))
    return render_template("calculation4.html", feedbacks=feedbacks, average_grade=average_grade, overall_percentage=overall_percentage)

@app.route('/calculation5', methods=["GET", "POST"])
def calculation5():
    feedbacks = fetch_feedbacks()
    dgpa = None
    percentage = None
    if request.method == "POST":
        try:
            course_type = request.form.get("course_type")
            semester_start = 1
            semester_end = 8
            if course_type == "3_year":
                semester_end = 6
            elif course_type == "3_year_lateral":
                semester_start = 3

            total_sgpa = 0
            count = 0
            for i in range(semester_start, semester_end + 1):
                sgpa = request.form.get(f"sgpa_sem{i}")
                if sgpa:
                    total_sgpa += float(sgpa)
                    count += 1

            if count > 0:
                dgpa = total_sgpa / count
                percentage = (dgpa * 10) - 7.5
        except ValueError:
            flash("Invalid input! Please enter valid numbers.", "danger")
            return redirect(url_for("calculation5"))
    return render_template("calculation5.html", feedbacks=feedbacks, dgpa=dgpa, percentage=percentage)

if __name__ == "__main__":
    app.run(debug=True, port=3000)



















# from flask import Flask, render_template, request,redirect, flash, url_for
# import sqlite3

# app = Flask(__name__, static_url_path='/static')
# app.secret_key = "your_secret_key"  # Replace with your actual secret key


# # Database setup
# conn = sqlite3.connect("feedback.db", check_same_thread=False)
# cursor = conn.cursor()

# # Create feedback table if it doesn't exist
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS feedback (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT NOT NULL,
#     rating INTEGER NOT NULL,
#     comment TEXT
# )
# """)
# conn.commit()




# @app.route('/calculation1', methods=['GET', 'POST'])

# def calculation1():
#     if request.method == 'POST':
#         try:
#             a = float(request.form['odd_sgpa'])
#             c = float(request.form['even_sgpa'])
#             g = int(request.form['odd_subjects'])
#             h = int(request.form['even_subjects'])

#             b = ((a * 10) - 7.5)
#             d = ((c * 10) - 7.5)
#             e = ((a + c) / 2)

#             g_total = g * 100
#             h_total = h * 100
#             i = g_total + h_total

#             j = (b * g_total) / 100
#             k = (d * h_total) / 100
#             l = j + k

#             f = ((l * 100) / i)

            

#             return render_template('calculation1.html', 
#                                    odd_percentage=b, even_percentage=d, 
#                                    ygpa=e, total_marks=i, obtained_marks=l, 
#                                    year_percentage=f)
#         except ValueError:
#             return "Invalid Input! Please enter valid numbers."
#     return render_template('calculation1.html')



# @app.route('/calculation2', methods=['GET', 'POST'])

# def calculation2():
#     if request.method == 'POST':
#         try:
#             a1 = float(request.form['odd_sgpa'])  # Reusing this field for SGPA input
#             b = ((a1 * 10) - 7.5)

#             return render_template('calculation2.html', 
#                                    sgpa_percentage=b)
#         except ValueError:
#             return "Invalid Input! Please enter valid numbers."
#     return render_template('calculation2.html')



# @app.route('/calculation3', methods=['GET', 'POST'])

# def calculation3():
#     if request.method == 'POST':
#         try:
#             a2 = float(request.form['odd_sgpa'])
#             b = ((a2 * 10) - 7.5)

#             c1 = float(request.form['even_sgpa'])
#             d = ((c1 * 10) - 7.5)

#             e = ((a2 + c1) / 2)

#             f = ((e * 10) - 7.5)

#             return render_template('calculation3.html', 
#                                    odd_percentage=b, even_percentage=d,
#                            ygpa=e, ygpa_percentage=f)
#         except ValueError:
#             return "Invalid Input! Please enter valid numbers."
#     return render_template('calculation3.html')


# @app.route('/calculation4', methods=['GET', 'POST'])
# def calculation4():
#     if request.method == 'POST':
#         try:
#             # Get the number of semesters
#             semester_count = int(request.form['semester_count'])
            
#             # Collect SGPA marks from the form
#             sgpa_marks = [
#                 float(request.form[f'sgpa_sem{i}'])
#                 for i in range(1, semester_count + 1)
#             ]
            
#             # Calculate average grade and overall percentage
#             average_grade = sum(sgpa_marks) / len(sgpa_marks)
#             overall_percentage = (average_grade - 0.75) * 10
            
#             return render_template(
#                 'calculation4.html',
#                 average_grade=round(average_grade, 2),
#                 overall_percentage=round(overall_percentage, 2)
#             )
#         except (ValueError, KeyError):
#             return "Invalid Input! Please enter valid numbers."
#     return render_template('calculation4.html')






# @app.route('/calculation5', methods=["GET", "POST"])
# def calculation5():
#     dgpa = None
#     percentage = None

#     if request.method == "POST":
#         course_type = request.form.get("course_type")
#         semester_start = 1
#         semester_end = 8

#         if course_type == "3_year":
#             semester_end = 6
#         elif course_type == "3_year_lateral":
#             semester_start = 3

#         total_sgpa = 0
#         count = 0

#         for i in range(semester_start, semester_end + 1):
#             sgpa = request.form.get(f"sgpa_sem{i}")
#             if sgpa:
#                 total_sgpa += float(sgpa)
#                 count += 1

#         if count > 0:
#             dgpa = total_sgpa / count
#             percentage = (dgpa - 0.75) * 10

#     return render_template("calculation5.html", dgpa=dgpa, percentage=percentage)








# @app.route("/", methods=["GET", "POST"])
# def home():
#     if request.method == "POST":
#         name = request.form.get("name")
#         rating = request.form.get("rating")
#         comment = request.form.get("comment")

#         # Insert new feedback into the database
#         cursor.execute(
#             "INSERT INTO feedback (name, rating, comment) VALUES (?, ?, ?)",
#             (name, int(rating), comment if comment else None),
#         )
#         conn.commit()
#         flash("Feedback submitted successfully!", "success")
#         return redirect(url_for("home"))

#     # Fetch all feedbacks
#     cursor.execute("SELECT * FROM feedback")
#     feedbacks = cursor.fetchall()
#     return render_template("home.html", feedbacks=feedbacks)


# @app.route("/delete-feedback/<int:feedback_id>", methods=["POST"])
# def delete_feedback(feedback_id):
#     secret_key = request.form.get("secret_key")
#     ADMIN_SECRET_KEY = "admin123"  # Replace with your admin secret key

#     if secret_key != ADMIN_SECRET_KEY:
#         flash("You are not authorized to delete feedback.", "danger")
#         return redirect(url_for("home"))

#     cursor.execute("DELETE FROM feedback WHERE id = ?", (feedback_id,))
#     conn.commit()
#     flash("Feedback deleted successfully.", "success")
#     return redirect(url_for("home"))







# if __name__ == '__main__':
#     app.run(debug=True, port=3000)
