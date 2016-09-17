from django.test import TestCase
from django.core.management import call_command

from nba.scrapper.week_data import WeekData

# Create your tests here.

# class ScrapperTest(TestCase):

    # def test_initial_data_load(self):
        # call_command('init_teams')
        # return

    # def test_scrape_connection(self):
        # call_command('fetch_week')
        # return

    # def test_delte_week(self):
        # call_command('delete_week')

    # def test_got_full_league(self):
        # return

    # def test_no_rank_duplicates(self):
        # return
    
# class QueryTest(TestCase):

    # def test_get_week(self):
        # return

    # def test_get_year(self):
        # return

class WeekDataTest(TestCase):

    def test_init(self):
        test = WeekData(2016)
        self.assertEqual(test.year, 2016)

    def test_verify_length(self):
        test = WeekData(2016)
        self.assertFalse(test.verify_length())

    def test_verify_ranks(self):
        test = WeekData(2016)
        self.assertFalse(test.verify_ranks())















