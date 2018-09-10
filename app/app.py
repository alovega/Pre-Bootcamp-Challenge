from datetime import datetime
import json

from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from models.models import AppDb


AppDao = AppDb()

DTime = datetime.now()


class QuestionDao(object):

    def __init__(self,title, details):
        self.title = title
        self.details = details
        self.date = str(DTime.date())

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

class AnswerDao(object):

    def __init__(self,answer,id):
        self.answer = answer
        self.id = id


class Questions(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, location='json')
        self.reqparse.add_argument('details', type=str, location='json')
        super(Questions, self).__init__()
    @jwt_required
    def get(self):
        questions = AppDao.get_all_questions()

        return questions
    @jwt_required
    def post(self):

        args = self.reqparse.parse_args()
        title = args['title']
        details = args['details']

        if not title.replace(" ", ""):
            return {"message":"title can not be empty"}, 400
        elif not details.replace(" ", ""):
            return {"message":"details can not be empty"}, 400

        questions = QuestionDao(title = title, details= details)
        if AppDao.check_question_title_exists(questions.title):
            return {"message": "title already used"}, 202

        AppDao.insert_question(questions)
        return {questions.title: questions.details}


class Question(Resource):
    @jwt_required
    def get(self, id):
        questions = AppDao.get_question_with_answers(id)
        print(questions)

        if questions:
            return questions

    @jwt_required
    def delete(self, id):
        questions = AppDao.get_question(id)
        if questions:
            AppDao.delete_question(id)
            return{"message":"successfully deleted"}

        else:
            return {"message": "question id not existing"}


class Answers(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('answer', type=str, location='json')
        self.reqparse.add_argument('id', type=int, location='json')
        super(Answers, self).__init__()
    @jwt_required
    def post(self, id):
        args = self.reqparse.parse_args()
        answer = args['answer']
        if not answer.replace(" ", ""):
            return {"message":"can't post an empty answer"}, 400
        answers = AnswerDao(answer=answer, id=id)
        print(answers)
        if AppDao.check_answer_exists(answers.answer):
            return {"message": "answer already posted"}, 400
        AppDao.insert_answer(answers)
        return {"answer": answers.answer}

    @jwt_required
    def get(self):
        answer = AppDao.get_all_answers()

        return answer


class Answer(Resource):


    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('answer', type=str, location='json')
        self.reqparse.add_argument('id', type=str, location='json')
        super(Answer, self).__init__()
    @jwt_required
    def put(self, id,answer_id):
        args = self.reqparse.parse_args()
        answer = args['answer']
        if not answer.replace(" ", ""):
            return {"message":"can't post an empty answer"}, 400
        answers = AnswerDao(answer=answer, id=id)
        print(answers)
        check = AppDao.get_answers(answer_id)
        print(check)
        if check:
            result =AppDao.update_answer(answers.answer, answer_id)
            return result

        return {"answer does not exist"}


