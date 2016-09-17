from django.test import TestCase
from django.core.management import call_command

# Create your tests here.

class ScrapperTest(TestCase):

    def test_initial_data_load(self):
        call_command('init_teams')
        return

    def test_scrape_connection(self):
        call_command('fetch_week')
        return

    def test_delte_week(self):
        call_command('delete_week')

    def test_got_full_league(self):
        return

    def test_no_rank_duplicates(self):
        return
    
class QueryTest(TestCase):

    def test_get_week(self):
        return

    def test_get_year(self):
        return

class ModelTest(TestCase):

    def get_name(self):
        return
