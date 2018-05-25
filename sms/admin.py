from django.contrib import admin

from .models import Person, Job, Major, NextMajor, School, SchoolType, Parent, Inbox, Outbox, Graduate, MessageStatus

admin.site.register(Person)
admin.site.register(Job)
admin.site.register(Major)
admin.site.register(NextMajor)
admin.site.register(School)
admin.site.register(SchoolType)
admin.site.register(Parent)
admin.site.register(Inbox)
admin.site.register(Outbox)
admin.site.register(Graduate)
admin.site.register(MessageStatus)