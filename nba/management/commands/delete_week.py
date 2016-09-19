from django.core.management.base import BaseCommand, CommandError
from nba.models import Team, Ranking
import json
import re
import sys

class Command(BaseCommand):
    help = 'Delete a week\'s data from the DB.'

    def add_arguments(self, parser):
        parser.add_argument('--week',
                action='store',
                type=int,
                dest='week',
                nargs='1',
                help='Delete the specified week')

        parser.add_argument('--year',
                action='store',
                type=int,
                dest='year',
                nargs='1',
                help='Delete the specified year')

    def handle(self, *args, **options):
        week = options['week']
        year = options['year']

        print 'Deleting data for week {0} ({1})...'.format(week, year)
        deleted = Ranking.objects.filter(year=year, week=week).delete()
        print 'Deleted {0} rankings.'.format(deleted[0])

