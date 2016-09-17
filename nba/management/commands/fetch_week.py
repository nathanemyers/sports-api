from django.core.management.base import BaseCommand, CommandError
from bs4 import BeautifulSoup, NavigableString
import urllib2
import json
import re
import sys
from nba.models import Ranking
from nba.scrapper.week_data import WeekData

import pdb

# TODO add this as an option
YEAR = 2016

class Command(BaseCommand):
    help = 'Fetches the weekly ranking data from ESPN. If no week is specified, fetch rankings from the current week'

    def add_arguments(self, parser):
        parser.add_argument('--week',
                action='store',
                type=int,
                dest='week',
                nargs='?',
                help='Fetch the specified week')

        parser.add_argument('--year',
                action='store',
                type=int,
                dest='year',
                nargs='?',
                default='2017',
                help='Fetch the specified week')

        parser.add_argument('--test',
                action='store_true',
                dest='test',
                default=False,
                help='Output data to stdout instead of DB')

    def handle(self, *args, **options):
        url = 'http://espn.go.com/nba/powerrankings'
        if 'week' in options and options['week'] is not None:
            url = 'http://espn.go.com/nba/powerrankings/_/week/' + str(options['week'])

        sys.stdout.write('Scraping URL: ' + url + '\n')
        sys.stdout.flush()
        response = urllib2.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')

        table = soup.find('table')

        # Figure out what week we're looking at
        table_head = table.find('tr', 'stathead').find('td').getText()
        m = re.search('Rankings: (Preseason|Week \w+)', table_head)
        matched_week = m.group(1)
        if matched_week == 'Preseason':
            week = 0
        else:
            week = int(re.search('Week (\w+)', matched_week).group(1))

        data = WeekData(options['year'], week)

        if not options['test']:
            lookup = Ranking.objects.filter(year=YEAR, week=week)
            if len(lookup) > 0: 
                sys.stdout.write('Ranking data for Year: ' + str(YEAR) + ' Week: ' + str(week) + ' already present. Quiting.\n')
                sys.stdout.flush()
                return

        rows = table.find_all('tr', ['evenrow', 'oddrow'])

        if options['test']:
            print 'Year: ' + str(YEAR)
            print 'Week: ' + str(week) + '\n'

        for row in rows:
            cols = row.find_all('td')

            # Here comes all the messy soup
            rank = cols[0].string

            city_col = cols[1].find_all('a')
            team = city_col[0].get('href') 

            summary_raw = cols[3]
            
            # TODO summary.getText() will sometimes leave a bunch of whitespace at the end, doesn't seem to effect webapp though
            summary = summary_raw.getText()

            record = row.find('span', class_='pr-record').string

            if options['test']:
                print 'Team: ' + str(team)
                print 'Rank: ' + rank
                print 'Record: ' + record
                print 'Summary: ' + summary + '\n'
            else:
                data.add_rank({
                    'record': record,
                    'team': team,
                    'summary': summary,
                    'rank': rank
                    })
            # end for

        print data.to_json()
        sys.stdout.write('Finished scrape of Year: ' + str(YEAR) + ' Week: ' + str(week) + '.\n')
            
