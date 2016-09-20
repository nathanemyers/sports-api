import json
from django.test import TestCase, RequestFactory
from django.core.management import call_command

from nba.scrapper.week_data import WeekData
from .views import week_rankings, year_rankings, info

class ApiTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        call_command('loaddata', 'full2016')

    def test_week_rankings(self):
        request = self.factory.get('/rankings/2016/1')
        response = week_rankings(request, 2016, 1)
        rankings = json.loads(response.content)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(rankings['rankings']['Warriors'], 1)
        self.assertEquals(rankings['rankings']['Pacers'], 25)

    def test_year_rankings(self):
        request = self.factory.get('/rankings/2016')
        response = year_rankings(request, 2016)
        data = json.loads(response.content)
        results = data['results']

        self.assertEquals(response.status_code, 200)
        self.assertEquals(results.__len__(), 30)
        self.assertEquals(results[0].__len__(), 24)

    def test_most_recent(self):
        request = self.factory.get('/rankings/info')

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
        with open('nba/data/week1data.json', 'r') as f:
            json_data = f.read()
        test.load_from_json(json.loads(json_data))
        
        self.assertTrue(test.verify_ranks())
        self.assertTrue(test.verify_length())

    def test_save(self):
        call_command('loaddata', 'clean_db')

        test = WeekData()
        with open('nba/data/week1data.json', 'r') as f:
            json_data = f.read()
        test.load_from_json(json.loads(json_data))

        test.save()

