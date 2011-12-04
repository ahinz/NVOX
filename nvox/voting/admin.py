from voting.models import Project, Vote, Community, CommunityProject
from django.contrib import admin

admin.site.register(Project)
admin.site.register(Vote)
admin.site.register(Community)
admin.site.register(CommunityProject)
