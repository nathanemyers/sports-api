from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from nba.models import Team, Ranking
from nba.serializers import RankingSerializer, TeamSerializer
from rest_framework import generics

# Create your views here.

class WeekList(generics.ListAPIView):
    serializer_class = RankingSerializer

    def get_queryset(self):
        week = self.kwargs['week']
        year = self.kwargs['year']
        return Ranking.objects.filter(week=week, year=year)

class YearList(generics.ListAPIView):
    serializer_class = TeamSerializer

    def get_queryset(self):
        year = self.kwargs['year']
        teams = Team.objects.all()
        results = []
        for team in teams:
            team.rankings = Ranking.objects.filter(
                    year=year,
                    team=team.id
                    )
            results.append(team)

        return results

def info(request):
    most_recent = Ranking.objects.last()
    return JsonResponse({'most_recent_week': most_recent.week})

