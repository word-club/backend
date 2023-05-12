from django.contrib import admin

from community.models import Community
from community.sub_models.moderator import Moderator
from community.sub_models.rule import Rule
from community.sub_models.subscription import Subscription
from community.sub_models.theme import Theme

admin.site.register(Community)
admin.site.register(Moderator)
admin.site.register(Rule)
admin.site.register(Subscription)
admin.site.register(Theme)
