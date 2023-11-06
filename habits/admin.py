from django.contrib import admin

# Register your models here.
from habits.models import Habit

admin.site.register(Habit)
