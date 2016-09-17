from django.core.management.base import BaseCommand, CommandError
import json
from nba.models import Ranking
from nba.scrapper.week_data import WeekData

class Command(BaseCommand):
    help = 'Upload a json representation of a week\'s worth of data'

    def add_arguments(self, parser):

        parser.add_argument('json',
                nargs=1,
                help='json file to load into database')

    def handle(self, *args, **options):
        json_file = options['json']

        with open(json_file, 'r') as f:
            json_data = json.load(f)

        lookup = Ranking.objects.filter(year=json_data.year, week=json_data.week)
        if len(lookup) > 0: 
            sys.stdout.write('Ranking data for Year: ' + str(year) + ' Week: ' + str(week) + ' already present. Quiting.\n')
            sys.stdout.flush()
            return

        data = WeekData(json_data.year, json_data.week)
        data.load_from_json(json_data.rankings)

        try:
            data.save()
        except ValueError as err:
            print err
