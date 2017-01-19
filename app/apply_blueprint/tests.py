import unittest
import models
import flask
from app import app, db, mail
import os
import cli
from click.testing import CliRunner
import json
import flask_restful

blueprint_name = os.path.dirname(os.path.realpath(__file__)).split("/")[-1]

class TestCase(unittest.TestCase):
    def setUp(self):
        db.session.commit() # fixes hang - see http://stackoverflow.com/questions/24289808/drop-all-freezes-in-flask-with-sqlalchemy
        db.drop_all()
        db.create_all()
        r = CliRunner().invoke(cli.seed)
        if r.exception: raise r.exception
        self.guid = models.SurveyMonkey.Response.responses("cambridge", "foo")["data"][0]["custom_variables"]["response_guid"]
        # with open("{0}/sample-survey-monkey-responses-bulk.json".format(os.path.dirname(os.path.realpath(__file__))), 'rb') as f:
        #     self.guid = json.load(f)["data"][0]["custom_variables"]["response_guid"]

    def test_survey(self):
        s = models.SurveyMonkey.Survey("cambridge")
        self.assertIsInstance(s.data, dict)
        self.assertIsInstance(s.pages, list)
        self.assertIsInstance(s.pages[0].questions, list)
        self.assertIsInstance(s.pages[0].questions[0], models.SurveyMonkey.Survey.Question)

    def test_response(self):
        response = models.SurveyMonkey.Response("cambridge", guid=self.guid)
        self.assertIsInstance(response.data, dict)
        self.assertGreater(len(response.schools), 0)
        with app.app_context():
            with mail.record_messages() as outbox:
                response.email_response()
                i = len(outbox)
                self.assertGreater(i, 0)
                response.email_next_steps()
                self.assertGreater(len(outbox), i)

    def test_redirect_to_survey_monkey_with_guid(self):
        with app.test_request_context():
            url = flask.url_for("{0}.redirect_to_survey_monkey_with_guid".format(blueprint_name), hub="cambridge")
            response = app.test_client().get(url)
            self.assertEqual(response.status_code, 200)

    def test_after_survey_monkey(self):
        with app.test_request_context():
            url = flask.url_for("{0}.after_survey_monkey".format(blueprint_name)) + "?hub=cambridge&response_guid={0}".format(self.guid)
            response = app.test_client().get(url)
            self.assertEqual(response.status_code, 200)

    def test_non_text_answer(self):
        r = models.SurveyMonkey.Response("cambridge", guid=self.guid)
        assert r.answer_for(app.config['HUBS']['CAMBRIDGE']['ANSWER_KEY']['CHILD']['GENDER']['SURVEY_MONKEY'])

    def test_transparent_classroom_submit_application(self):
        r = models.SurveyMonkey.Response("cambridge", guid=self.guid)
        models.TransparentClassroom(r.schools[0]).submit_application(r)
