from django.core.management.base import BaseCommand, CommandError
import json
from nba.models import Ranking
from nba.scrapper.week_data import WeekData

class Command(BaseCommand):
    help = 'Upload a json representation of a week\'s worth of data'

    def add_arguments(self, parser):
        parser.add_argument('json',
                help='json file to load into database')

    def handle(self, *args, **options):
        json_file = options['json']

        with open(json_file, 'r') as f:
            json_data = json.load(f)

        week = json_data['week']
        year = json_data['year']
        rankings = json_data['rankings']

        lookup = Ranking.objects.filter(year=year, week=week)
        if len(lookup) > 0: 
            print 'Ranking data for Year: {0} Week: {1} already present. Quiting.'.format(year, week)
            sys.stdout.write('Ranking data for Year: ' + str(year) + ' Week: ' + str(week) + ' already present. Quiting.\n')
            sys.stdout.flush()
            return

        data = WeekData(year, week)
        data.load_from_json(json_data)

        try:
            data.save()
        except ValueError as err:
            print err
