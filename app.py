from flask import Flask, render_template, request
import sqlite3
import logging

# conn=sqlite3.connect('FEEDBACK.db')
# c=conn.cursor()
app = Flask(__name__)

# initialize logging
LOG_FILE_NAME = 'feedbacklog.txt'
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=LOG_FILE_NAME,
                    filemode='w')


# home page and link to feedback form
@app.route("/")
def home():
    contents_line1 = "<h1>We Appreciate Your Feedback</h1>"
    contents_line2 = "<a href='http://127.0.0.1:5001/feedback'>Click here to submit your feedback</a>"
    contents = contents_line1 + "<br>" + contents_line2
    return contents


# getting data from feedback form
@app.route("/feedback", methods=['POST', 'GET'])
def feedback():
    feedback_form = []
    if request.method == 'POST':
        feedback_form.append(request.form['name'])
        feedback_form.append(request.form['email'])
        feedback_form.append(request.form['phone'])
        feedback_form.append(request.form['gender'])
        feedback_form.append(request.form['course'])
        feedback_form.append(request.form['rate'])
        # print(feedback_form)
        logging.info('collected data from feedback form----> ' + ",".join(feedback_form))
        write_feedback_data(feedback_form)
        get_feedback_data()

    return render_template('feedback.html')


@app.route("/getresponse", methods=['GET'])
def get_response():
    get_feedback_data()
    return "DOne"


def write_feedback_data(feedback_form):
    #  conn = db_connect(FEEDBACK.db)
    # cur = conn.cursor()
    conn = sqlite3.connect('FEEDBACK.db')
    cur = conn.cursor()

    # logging.info('Connected to ' + db_name)

    sql = """insert into feedback_data(
          'name',
          'email',
          'phone',
          'gender',
          'course',
          'rate') values(?,?,?,?,?,?)"""
    # verifying the sql statement for debug
    # print(sql)
    cur.execute(sql, [x for x in feedback_form])
    cur.execute("commit")
    refno = cur.lastrowid
    print(refno)
    cur.close()
    conn.close()
    # logging.info("DB commit successful")
    return refno


def get_feedback_data():
    #  conn = db_connect(FEEDBACK.db)
    # cur = conn.cursor()
    conn = sqlite3.connect('FEEDBACK.db')
    cur = conn.cursor()
    cur.execute("select * from feedback_data")
    result = cur.fetchall()
    for data in result:
        print(data)
    cur.close()
    conn.close()
    # logging.info("DB commit successful")
    return True


if __name__ == "__main__":
    app.run(debug=True, port='5001')
