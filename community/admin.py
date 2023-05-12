from django.contrib import admin

from community.models import Community
from community.sub_models.moderator import Moderator
from community.sub_models.rule import Rule
from community.sub_models.subscription import Subscription
from community.sub_models.theme import Theme


class CommunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at', 'updated_at')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Community, CommunityAdmin)
admin.site.register(Moderator)
admin.site.register(Rule)
admin.site.register(Subscription)
admin.site.register(Theme)
