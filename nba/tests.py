import json
from django.test import TestCase
from django.core.management import call_command
from rest_framework.test import APIRequestFactory

from nba.scrapper.week_data import WeekData
from nba.views import info, WeekList, YearList

#TODO: There's a problem with the fixture loading, I need to regenerate the fixtures using:
# python manange.py dumpdata --indent=4 -e sessions admin contenttypes (or something like that)

# class ApiTest(TestCase):
    # def setUp(self):
        # self.factory = APIRequestFactory()
        # call_command('loaddata', 'full2016')

    # def test_week_rankings(self):
        # view = WeekList.as_view()
        # request = self.factory.get('/rankings/2016/1')
        # response = view(request, year=2016, week=1)
        # response.render()
        # rankings = json.loads(response.content)

        # self.assertEquals(response.status_code, 200)
        # self.assertEquals(rankings.__len__(), 30)

    # def test_year_rankings(self):
        # view = YearList.as_view()
        # request = self.factory.get('/rankings/2016')
        # response = view(request, year=2016)
        # response.render()
        # results = json.loads(response.content)

        # self.assertEquals(response.status_code, 200)
        # self.assertEquals(results.__len__(), 30)
        # self.assertEquals(results[0]['rankings'].__len__(), 24)

    # def test_most_recent(self):
        # request = self.factory.get('/rankings/info')

# class WeekDataTest(TestCase):

    # def test_init(self):
        # test = WeekData(2016, 1)
        # self.assertEqual(test.year, 2016)

    # def test_verify_length(self):
        # test = WeekData(2016, 1)
        # self.assertFalse(test.verify_length())

    # def test_verify_ranks(self):
        # test = WeekData(2016, 1)
        # self.assertFalse(test.verify_ranks())

    # def test_load_json(self):
        # test = WeekData()
        # with open('nba/data/week1data.json', 'r') as f:
            # json_data = f.read()
        # test.load_from_json(json.loads(json_data))
        
        # self.assertTrue(test.verify_ranks())
        # self.assertTrue(test.verify_length())

    # def test_save(self):
        # call_command('loaddata', 'clean_db')

        # test = WeekData()
        # with open('nba/data/week1data.json', 'r') as f:
            # json_data = f.read()
        # test.load_from_json(json.loads(json_data))

        # test.save()

