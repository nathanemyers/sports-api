from rest_framework import serializers
from nba.models import Team, Ranking

class RankingSerializer(serializers.ModelSerializer):
    team = serializers.StringRelatedField(many=False)
    class Meta:
        model = Ranking
        fields = ('year', 'week', 'team', 'rank', 'record', 'summary')

class TeamSerializer(serializers.ModelSerializer):
    rankings = RankingSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ('region', 'name', 'css_slug', 'color', 'conference', 'division', 'rankings')
