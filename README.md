Первое задание:

from django.db import models


class Player(models.Model):
    
    player_name = models.CharField(max_length=100)
    # просто поле с типом Дата, для хранения дынных о входе, заполняется при создании экземпляра класса
    # с модулем datetime
    first_visit = models.DateField()
    # Чтобы выдать буст за уровень, нужно эти уровни считать
    player_level = models.IntegerField(default=0)
    # счетчик входов в игру, к нему уже будет привязано начисление нарград, при инициализации экземрлеря
    # равен 1, так как создается при входе в игру
    entrance_counter = models.IntegerField(default=1)
    # manyToMany взаимосвязь, чтобы управлять бустами
    boosts = models.ManyToManyField(Boost)


class Boost(models.Model):
    title = models.CharField(max_length=100)

Первый вариант второго задания, я предположил, что модель LevelPrize содержит информацию о призе за каждый полученный уровень(по 1 награде за каждый уровень). Но тогда вопрос- зачем там поле recieved? Метод возвращает название награды, которую должен получить игрок за пройденный им уровень. Написал это как метод класса Player, можно и отдельной функцией от player id


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


Второй вариант второго задания, я предположил, что в модели LevelPrize не хватает поля 
player = models.ForeignKey(Player, on_delete=models.CASCADE), и мы сами должны выбрать награду для игрока и внести запись об этом в бд. Написал это как метод класса Player, можно и отдельной функцией от player id

class Player(models.Model):
    	player_id = models.CharField(max_length=100)

	def get_prize1(self, level:int, prize:str):
    		a = LevelPrize()
    		# проверка есть ли такой уровень и прошел ли игрок уровень
    		try:
        		if PlayerLevel.objects.filter(player__player_id=self.player_id)[0].is_completed:
           			 a.level = Level.objects.filter(order = level)[0]
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

Второе задание- экспорт CSV, для этого я воспользовался документацией Джанго для работы с большими csv файлами и с помощью генератора и StreamingHttpResponse выгружаю нужный файл с полями по запросу 
from django.http import StreamingHttpResponse
from g.models import Player, PlayerLevel, Prize, LevelPrize, Level
import csv


class Echo:
 def write(self, value):
        return value



Сама функция для экспорта в csv



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


