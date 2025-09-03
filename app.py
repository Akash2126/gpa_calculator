from flask import Flask, render_template, request

app = Flask(__name__)

# ---- SRM Grading: marks -> (grade, grade_point) ----
def srm_from_marks(m):
    if m >= 91:       return "O", 10
    elif m >= 81:     return "A+", 9
    elif m >= 71:     return "A", 8
    elif m >= 61:     return "B+", 7
    elif m >= 56:     return "B", 6
    elif m >= 50:     return "C", 5
    elif m >= 0:      return "F", 0  # Fail
    else:             return "F", 0

# ---- Direct grade -> grade_point ----
GRADE_POINTS = {
    "O": 10, "A+": 9, "A": 8, "B+": 7, "B": 6, "C": 5,
    "F": 0, "W": 0, "I": 0, "AB": 0
}

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        mode = request.form.get("mode")   # "marks" or "grades"
        subjects = request.form.getlist("subject")
        credits = request.form.getlist("credit")
        values = request.form.getlist("value")

        records = []
        total_points, total_credits = 0, 0

        # For bar chart
        subjects_list, grade_points_list = [], []

        for i in range(len(subjects)):
            try:
                c = int(credits[i]) if credits[i] else 0
                if c == 0: 
                    continue

                if mode == "marks":
                    m = int(values[i])
                    grade, gp = srm_from_marks(m)
                else:
                    grade = values[i].strip().upper()
                    gp = GRADE_POINTS.get(grade, 0)

                records.append((subjects[i], c, grade, gp))
                total_points += gp * c
                total_credits += c

                subjects_list.append(subjects[i])
                grade_points_list.append(gp)

            except:
                continue

        gpa = round(total_points / total_credits, 2) if total_credits else 0

        result = {
            "records": records,
            "gpa": gpa,
            "subjects": subjects_list,
            "points": grade_points_list
        }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
# ---- SRM Grading: marks -> (grade, grade_point) ----