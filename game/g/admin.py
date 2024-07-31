from django.contrib import admin

from g.models import Player, Level, Prize, PlayerLevel, LevelPrize

# Register your models here.
admin.site.register(Player)
admin.site.register(Level)
admin.site.register(Prize)
admin.site.register(PlayerLevel)
admin.site.register(LevelPrize)