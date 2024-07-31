from django.shortcuts import render
from django.http import StreamingHttpResponse
from g.models import Player, PlayerLevel, Prize, LevelPrize, Level
import csv

class Echo:


    def write(self, value):
        return value

def streaming_export_csv(request):
    rows = ([PlayerLevel.objects.all()[j].player_id,
               PlayerLevel.objects.all()[j].level.title,
               PlayerLevel.objects.all()[j].is_completed,
               LevelPrize.objects.filter(player_id = PlayerLevel.objects.all()[j].player_id)[0].prize.title]
               for j in range(len(PlayerLevel.objects.all())))
    print(type(rows))
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    var = (writer.writerow(row) for row in rows)
    return StreamingHttpResponse(var, content_type='text/csv',
                                 headers= {'Content-Disposition': 'attachment;filename="answer.csv"'}, )

