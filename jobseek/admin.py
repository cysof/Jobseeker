from django.contrib import admin
from .models import Company, Job, JobSkill, Skill, Application, CustomUser


admin.site.register(Company)
admin.site.register(Job)
admin.site.register(JobSkill)
admin.site.register(Skill)
admin.site.register(Application)
admin.site.register(CustomUser)
