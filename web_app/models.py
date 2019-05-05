from django.db import models

import datetime
from django.utils import timezone


# User visit model
class Visit(models.Model):
    username = models.TextField('user', default='anonymous', null=False, blank=False)
    visit_start = models.DateTimeField('start', default=timezone.now)
    visit_end = models.DateTimeField('end', default=timezone.now)

    def __str__(self):
        return '{} on {}'.format(self.username, self.visit_start)

    def visited_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.visit_start <= now

    visited_recently.admin_order_field = 'visit_time'
    visited_recently.boolean = True
    visited_recently.short_description = 'Visited recently?'


# Posts made by users model
class Message(models.Model):
    visit = models.ForeignKey(Visit, on_delete=models.DO_NOTHING,)
    time = models.DateTimeField(auto_now_add=True, null=True)
    message_text = models.CharField('message', max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return '{}: "{}" on {}'.format(self.visit.username, self.message_text, self.time.date())
