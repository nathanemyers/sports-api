import json
from django.test import TestCase, RequestFactory
from django.core.management import call_command

from nba.scrapper.week_data import WeekData

class ApiTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_week_rankings(self):
        request = self.factory.get('/rankings/2016/1')
        return

    def test_year_rankings(self):
        request = self.factory.get('/rankings/2016')
        return

    def test_most_recent(self):
        request = self.factory.get('/rankings/info')
        return

class WeekDataTest(TestCase):

    def test_init(self):
        test = WeekData(2016, 1)
        self.assertEqual(test.year, 2016)

    def test_verify_length(self):
        test = WeekData(2016, 1)
        self.assertFalse(test.verify_length())

    def test_verify_ranks(self):
        test = WeekData(2016, 1)
        self.assertFalse(test.verify_ranks())

    def test_load_json(self):
        test = WeekData()
        with open('nba/fixtures/week1data.json', 'r') as f:
            json_data = f.read()
        test.load_from_json(json.loads(json_data))
        
        self.assertTrue(test.verify_ranks())
        self.assertTrue(test.verify_length())

    def test_save(self):
        call_command('loaddata', 'clean_db')

        test = WeekData()
        with open('nba/fixtures/week1data.json', 'r') as f:
            json_data = f.read()
        test.load_from_json(json.loads(json_data))

        test.save()

