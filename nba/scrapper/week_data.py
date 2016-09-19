import json
from nba.models import Ranking, Team

class WeekData:
    
    def __init__(self, year=None, week=None):
        self.rankings = []
        self.year = year
        self.week = week

    def add_rank(self, data):
        self.rankings.append(data)

    def verify_length(self):
        if self.rankings.__len__() != 30:
            return False
        return True

    def verify_ranks(self):
        ''' Make sure each ranking appears once and only once'''
        for current_rank in range(1, 31):
            count = 0
            for rank in self.rankings:
                if rank['rank'] == str(current_rank):
                    count = count + 1
            if count != 1:
                return False
        return True

    def save(self):
        if not self.verify_length():
            raise ValueError('Missing Teams!')
        if not self.verify_ranks():
            raise ValueError('Ranks are not uniform!')

        self.rankings = map(lambda x: process_rank(x, self.year, self.week), self.rankings)

        for rank in self.rankings:
            rank_object = Ranking(
                    year = self.year,
                    week = self.week,
                    rank = data.rank,
                    record = data.record,
                    team = team,
                    summary = data.comment_string
                    )
            rank_object.save()

    def to_json(self):
        serialized = {
                'year': self.year,
                'week': self.week,
                'rankings': self.rankings
                }
        return json.dumps(serialized, sort_keys=True, 
                indent=4, separators=(',', ': '))

    def load_from_json(self, json_data):
        data = json.loads(json_data)
        self.year = data['year']
        self.week = data['week']
        self.rankings = data['rankings']

def process_rank(rank, year, week):
    rank['team']= resolve_team(rank['team'])
    rank['summary'] = stripTags(rank['summary'], ['b', 'i', 'a', 'u'])
    return rank

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

def resolve_team(team_html_link):
    if 'lakers' in team_html_link:
        return Team.objects.get(name='Lakers')
    if 'clippers' in team_html_link:
        return Team.objects.get(name='Clippers')
    if 'warriors' in team_html_link:
        return Team.objects.get(name='Warriors')
    if 'cavaliers' in team_html_link:
        return Team.objects.get(name='Cavaliers')
    if 'spurs' in team_html_link:
        return Team.objects.get(name='Spurs')
    if 'thunder' in team_html_link:
        return Team.objects.get(name='Thunder')
    if 'rockets' in team_html_link:
        return Team.objects.get(name='Rockets')
    if 'grizzlies' in team_html_link:
        return Team.objects.get(name='Grizzlies')
    if 'hawks' in team_html_link:
        return Team.objects.get(name='Hawks')
    if 'heat' in team_html_link:
        return Team.objects.get(name='Heat')
    if 'bulls' in team_html_link:
        return Team.objects.get(name='Bulls')
    if 'pelicans' in team_html_link:
        return Team.objects.get(name='Pelicans')
    if 'raptors' in team_html_link:
        return Team.objects.get(name='Raptors')
    if 'celtics' in team_html_link:
        return Team.objects.get(name='Celtics')
    if 'bucks' in team_html_link:
        return Team.objects.get(name='Bucks')
    if 'wizards' in team_html_link:
        return Team.objects.get(name='Wizards')
    if 'pacers' in team_html_link:
        return Team.objects.get(name='Pacers')
    if 'pistons' in team_html_link:
        return Team.objects.get(name='Pistons')
    if 'jazz' in team_html_link:
        return Team.objects.get(name='Jazz')
    if 'kings' in team_html_link:
        return Team.objects.get(name='Kings')
    if 'suns' in team_html_link:
        return Team.objects.get(name='Suns')
    if 'mavericks' in team_html_link:
        return Team.objects.get(name='Mavericks')
    if 'hornets' in team_html_link:
        return Team.objects.get(name='Hornets')
    if 'magic' in team_html_link:
        return Team.objects.get(name='Magic')
    if 'knicks' in team_html_link:
        return Team.objects.get(name='Knicks')
    if 'wolves' in team_html_link:
        return Team.objects.get(name='Timberwolves')
    if 'nuggets' in team_html_link:
        return Team.objects.get(name='Nuggets')
    if 'blazers' in team_html_link:
        return Team.objects.get(name='Trail Blazers')
    if 'nets' in team_html_link:
        return Team.objects.get(name='Nets')
    if '76ers' in team_html_link:
        return Team.objects.get(name='76ers')
    raise ValueError('Could not find team!')

