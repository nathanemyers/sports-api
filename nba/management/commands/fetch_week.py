from django.core.management.base import BaseCommand, CommandError
from bs4 import BeautifulSoup, NavigableString
import urllib2
import json
import re
import sys
from nba.models import Ranking
from nba.scrapper.week_data import WeekData

def stripTags(html, invalid_tags):
    for tag in html:
        if tag.name in invalid_tags:
            s = ""
            for c in tag.contents:
                if not isinstance(c, NavigableString):
                    c = stripTags(unicode(c), invalid_tags)
                s += unicode(c)

            tag.replaceWith(s)
    return html

class Command(BaseCommand):
    help = 'Fetches the weekly ranking data from ESPN. If no week is specified, fetch rankings from the current week'

    def add_arguments(self, parser):
        parser.add_argument('--week',
                action='store',
                type=int,
                dest='week',
                nargs='?',
                default='',
                help='Fetch the specified week')

        parser.add_argument('--year',
                action='store',
                type=int,
                dest='year',
                nargs='?',
                default='2017',
                help='Fetch the specified week')

        parser.add_argument('--dump',
                action='store_true',
                dest='dump',
                default=False,
                help='Dump data to json instead of to DB')

    def handle(self, *args, **options):
        url = 'http://espn.go.com/nba/powerrankings'
        year = options['year']
        week = options['week']
        if week != '':
            url = 'http://espn.go.com/nba/powerrankings/_/year/{0}/week/{1}'.format(year, week)

        sys.stdout.write('Scraping URL: ' + url + '\n')
        sys.stdout.flush()
        response = urllib2.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')

        table = soup.find('table', 'tablehead')

        # Figure out what week we're looking at
        table_head = table.find('tr', 'stathead').find('td').getText()
        m = re.search('Rankings: (Preseason|Week \w+)', table_head)
        matched_week = m.group(1)
        if matched_week == 'Preseason':
            week = 0
        else:
            week = int(re.search('Week (\w+)', matched_week).group(1))

        data = WeekData(year, week)
        data.set_url(url)

        if not options['dump']:
            lookup = Ranking.objects.filter(year=year, week=week)
            if len(lookup) > 0:
                sys.stdout.write('Ranking data for Year: {0} Week: {1} already present. Quiting.\n'.format(year, week))
                sys.stdout.flush()
                return

        rows = table.find_all('tr', ['evenrow', 'oddrow'])

        for row in rows:
            cols = row.find_all('td')

            # Here comes all the messy soup
            rank = cols[0].string

            city_col = cols[1].find_all('a')
            team = city_col[0].get('href')

            summary_raw = cols[3]
            summary_raw = stripTags(summary_raw, ['b', 'i', 'a', 'u'])

            # TODO summary.getText() will sometimes leave a bunch of whitespace at the end, doesn't seem to effect webapp though
            summary = summary_raw.getText()

            record = row.find('span', class_='pr-record').string

            data.add_rank({
                'record': record,
                'team': team,
                'summary': summary,
                'rank': rank
                })
        # end for

        if options['dump']:
            print data.to_json()

        try:
            data.save()
        except ValueError as err:
            print err
            dump_filename = 'nba-dump-{0}-{1}.json'.format(year, week)
            with open(dump_filename, 'w') as f:
                f.write(data.to_json())
            print 'Dumped week scrape to {0}. Repair the file and manually upload with:'.format(dump_filename)
            print 'python manage.py upload_json'

        sys.stdout.write('Finished scrape of Year: ' + str(year) + ' Week: ' + str(week) + '.\n')
