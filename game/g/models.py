from django.db import models
import csv
from datetime import datetime

class Player(models.Model):
    player_id = models.CharField(max_length=100)

    def get_prize(self, level:int):
        # проверка прошел ли игрок уровень
        if PlayerLevel.objects.filter(player__player_id=self.player_id)[0].is_completed:
            # обращаемся к призу по заданному уровню
            answer = LevelPrize.objects.filter(level__order = level)[0].prize.title
            return answer
        # если игрок не прошел уровень, возвращаем False
        else:
            return False

    def get_prize1(self, level: int, prize: str):
        a = LevelPrize()
        # проверка есть ли такой уровень и прошел ли игрок уровень
        try:
            if PlayerLevel.objects.filter(player__player_id=self.player_id)[0].is_completed:
                a.level = Level.objects.filter(order=level)[0]
            else:
                print('level is not completed')
        except:
            print('level does not exist')
            # проверка есть ли такой приз
        try:
            a.prize = Prize.objects.filter(title=prize)[0]
            a.player = Player.objects.filter(player_id=self.player_id)[0]
            a.received = datetime.today()
            a.save()

        except:
            print('prize does not exist')


class Level(models.Model):
    title = models.CharField(max_length=100)
    order = models.IntegerField(default=0)


class Prize(models.Model):
    title = models.CharField(max_length=100)


class PlayerLevel(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    completed = models.DateField()
    is_completed = models.BooleanField(default=False)
    score = models.PositiveIntegerField(default=0)



class LevelPrize(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE)
    received = models.DateField()
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
