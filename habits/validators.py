from django.core.exceptions import ObjectDoesNotExist
from rest_framework.validators import ValidationError
from datetime import datetime, timedelta
from cron_converter import Cron
from habits.models import Habit


class HabitDuration:
    """ Check if the habit execution time is no more than 120 seconds. """

    def __call__(self, value):
        # print(f'value ===== {value=}')
        if value['duration'] > timedelta(seconds=120):
            message = 'The execution time should be no more than 120 seconds.'
            raise ValidationError(message)


class HabitRelatedIsPleasant:
    """ Check if the related habit should be pleasant. """

    def __call__(self, value):
        try:
            is_pleasant = Habit.objects.values_list('is_pleasant').get(operation=value['related_habit'])

            if value['related_habit'] and not is_pleasant:
                message = 'The related habit should be pleasant.'
                raise ValidationError(message)

        except ObjectDoesNotExist:
            print('habits.models.Habit.DoesNotExist: Habit matching query does not exist.')


class HabitRewardOrRelatedIsPleasant:
    """ Check if simultaneous selection is excluded """

    def __call__(self, value):
        # is_pleasant = Habit.objects.values_list('is_pleasant').get(operation=value['related_habit'])
        # reward = Habit.objects.values_list('reward')

        related_habit = value['related_habit']
        reward = value['reward']
        # print(related_habit, reward)
        if related_habit and reward:
            message = 'Simultaneous selection of the reward and related pleasant habit is excluded'
            raise ValidationError(message)


class HabitRelatedOrIsPleasant:
    """ checking a pleasant habit can't have a reward or a related habit """

    def __call__(self, value):
        is_pleasant = value['is_pleasant']
        related_habit = value['related_habit']
        reward = value['reward']
        # print(is_pleasant, related_habit, reward)

        if is_pleasant and (related_habit or reward):
            message = 'A pleasant habit can\'t have a reward or a related habit'
            raise ValidationError(message)


class FrequencyLessOneWeek:
    """ checking frequency of the habit """

    def __call__(self, value):
        crontab = value['task_crontab']
        print('crontab', crontab)
        crontab_str = ' '.join(crontab.values())
        print('crontab_str', crontab_str)
        cron_instance = Cron()
        # Parse a string to init a schedule
        cron_instance.from_string(crontab_str)

        # Raw datetime without timezone info (not aware)
        reference = datetime.now()
        # Get the iterator, initialised to now
        schedule = cron_instance.schedule(reference)

        # Calls to .next()
        next_time = schedule.next()

        delta_time = next_time - reference
        # print(next_time, 'delta_time = ', delta_time, '<', timedelta(days=7))

        if not delta_time < timedelta(days=7):
            message = 'The frequency of the habit should be less than a week'
            raise ValidationError(message)
