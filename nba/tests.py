from django.test import TestCase
from django.core.management import call_command

from nba.scrapper.week_data import WeekData


class WeekDataTest(TestCase):
    def setupDB():
        call_command('loaddata', 'nba/fixtures/clean_db')

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
            json = f.read()
        test.load_from_json(json)
        
        self.assertTrue(test.verify_ranks())
        self.assertTrue(test.verify_length())

    def test_save(self):
        call_command('loaddata', 'clean_db')

        test = WeekData()
        with open('nba/fixtures/week1data.json', 'r') as f:
            json = f.read()
        test.load_from_json(json)

        test.save()

