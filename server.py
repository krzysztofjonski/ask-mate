from flask import Flask, render_template, request, redirect, url_for
import data_handler
import time
import util

app = Flask(__name__)

DATAPATHQ = r"C:\Users\krzys\PycharmProjects\CODECOOL\modul_2\homework\my\ask-mate-1-python-krzysztofjonski\sample_data\question.csv"
DATAPATHA = r"C:\Users\krzys\PycharmProjects\CODECOOL\modul_2\homework\my\ask-mate-1-python-krzysztofjonski\sample_data\answer.csv"


@app.route("/")
def home_page():
    return render_template("index.html")


@app.route("/list", methods=['GET', 'POST'])
def question_table():
    table = data_handler.read_csv(DATAPATHQ)
    reversed_table = reversed(table)
    return render_template("list.html", table=reversed_table)

@app.route("/question/<id>", methods=['GET', 'POST'])
def display_a_question(id):

    question_table = data_handler.pick_id(str(id), DATAPATHQ)
    answers = data_handler.read_csv(DATAPATHA)
    print(answers)
    data_handler.view_number(DATAPATHQ, question_table)
    return render_template('question.html', answers=answers, question=question_table)

@app.route('/add-question', methods=["GET", "POST"])
def add_question():
    if request.method == "GET":
        return render_template("ask_question.html")
    elif request.method == "POST":
        question = {
            "id": 0,
            "submission_time": int(time.time()),
            "view_number": 0,
            "vote_number": 0,
            "title": request.form['questiontitle'],
            "message": request.form['question_body'],
            "image": ""
        }
        data_handler.append_question_csv_row(DATAPATHQ, question)
        return redirect("/list")



@app.route('/question/<id>/new-answer', methods=['GET', 'POST'])
def add_new_answer(id):
    if request.method == 'GET':
        question = data_handler.pick_id(id, DATAPATHQ)
        return render_template('post_answers.html', question=question)
    elif request.method == "POST":

        data = request.form.to_dict()
        print(data)
        data['question_id'] = id
        data_handler.append_csv_row(DATAPATHA, data)
        return redirect(url_for('display_a_question', id=id))

        # answer = {
        #     "id": 0,
        #     "submission_time": int(time.time()),
        #     "vote_number": 0,
        #     "question_id": request.form['question_id'],
        #     "message": request.form['new_answer'],
        #     "image": ""
        # }
        #
        # answer["question_id"] = id
        # data_handler.append_csv_row(DATAPATHA, answer)
        # return redirect("/question/<id>")


        # answers = data_handler.read_csv(DATAPATHA)
        # questions = data_handler.read_csv(DATAPATHQ)
        # form = request.form.to_dict()
        # form_list = [util.add_new_id(answers), int(time.time()), 0, 0, form['post_answers'], answers, '']
        # answers.append(form_list)
        # data_handler.write_csv(DATAPATHA, answers)
        # return redirect('/question/<id>')

@app.route('/question/<id>/delete', methods=["GET"])
def remove_question(id):
    question = data_handler.pick_id(id, DATAPATHQ)
    data_handler.delete_question(DATAPATHQ, question)
    data_handler.delete_answers_to_question(DATAPATHA, id)
    return redirect(url_for('question_table'))


@app.route('/answer/<answer_id>/delete', methods=["GET"])
def remove_answer(answer_id):
    answer = data_handler.pick_id(answer_id, DATAPATHA)
    # print(answer)
    data_handler.delete_question(DATAPATHA, answer)
    return redirect(url_for('question_table', answer_id=answer['question_id']))

@app.route('/question/<question_id>/vote-up', methods=["GET"])
def question_vote_up(question_id):
    question = data_handler.pick_id(question_id, DATAPATHQ)
    data_handler.vote_changer(DATAPATHQ, question, True)
    return redirect(url_for('question_table'))


@app.route('/question/<question_id>/vote-down', methods=["GET"])
def question_vote_down(question_id):
    question = data_handler.pick_id(question_id, DATAPATHQ)
    data_handler.vote_changer(DATAPATHQ, question, False)
    return redirect(url_for('question_table'))


@app.route('/answer/<answer_id>/vote_up', methods=["GET"])
def answer_vote_up(answer_id):
    answer = data_handler.pick_id(answer_id, DATAPATHA)
    data_handler.vote_changer(DATAPATHA, answer, True)
    return redirect(url_for('display_a_question', id=answer['question_id']))


@app.route('/answer/<answer_id>/vote_down', methods=["GET"])
def answer_vote_down(answer_id):
    answer = data_handler.pick_id(answer_id, DATAPATHA)
    data_handler.vote_changer(DATAPATHA, answer, False)
    return redirect(url_for('display_a_question', id=answer['question_id']))

@app.route('/question/<id>/edit', methods=["GET", "POST"])
def edit_question(id):
    question = data_handler.pick_id(id, DATAPATHQ)
    if request.method == 'GET':
        return render_template("edit_question.html", question=question)
    else:
        data = request.form.to_dict()
        data_handler.edit_data(DATAPATHQ, data, question)
        return redirect(url_for("display_a_question", id=id))

# def hello():
#     return "Hello World!"


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8001,
        debug=True,
    )
