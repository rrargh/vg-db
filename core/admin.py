from django.contrib import admin

# Register your models here.
from django.forms import TextInput
from models import Member, Ministry, SundayService, \
    Venue, VictoryGroup


class MemberAdmin(admin.ModelAdmin):
    model = Member
    list_display = ('full_name', 'contact_number', 'service_attended',
        'life_stage', 'ministry', 'coach', 'victory_group', 'is_vg_leader', 'is_active'
    )
    list_editable = ('contact_number', 'service_attended',
        'life_stage', 'ministry', 'coach', 'victory_group', 'is_vg_leader', 'is_active'
    )
    list_filter = ('gender', 'life_stage', 'service_attended', 'ministry',
        'one2one', 'victory_weekend', 'church_community', 'purple_book',
        'making_disciples', 'empowering_leaders', 'leadership113', 'doing_one2one'
    )
    search_fields = ('first_name', 'last_name', 'facebook_id', 'email')
    fieldsets = (
            ("Personal Info", {
                'fields': (
                    'first_name', 'last_name', 'nickname',
                    'birthdate', 'gender', 'life_stage',
                     'contact_number', 'facebook_id', 'email'
                )
            }),
            ('Victory Membership', {
                'fields': (
                    'service_attended', 'ministry', 'coach', 'victory_group',
                    'doing_one2one', 'is_vg_leader', 'is_active'
                )
            }),
            ('Discipleship Journey', {
                'fields': (
                    'one2one', 'victory_weekend', 'church_community',
                    'purple_book', 'making_disciples',
                    'empowering_leaders', 'leadership113'
                )
            }),
    )


class MemberInline(admin.TabularInline):
    model = Member
    extra = 0
    can_delete = False
    verbose_name_plural = "Members (excluding VG leaders)"


class VictoryGroupAdmin(admin.ModelAdmin):
    model = VictoryGroup
    list_display = ('leader', 'demographic', 'day',
        'time', 'venue', 'member_count'
    )
    list_editable = ('demographic', 'day', 'time', 'venue')
    list_filter = ('demographic', 'group_type', 'group_age',
        'year_started', 'day', 'time', 'venue'
    )
    readonly_fields = ('member_count',)
    search_fields = ('leader', 'co_leader', 'vg_intern')
    inlines = (MemberInline,)

# FIXME: pastoral ministry?  staff?
class MinistryAdmin(admin.ModelAdmin):
    model = Ministry


class SundayServiceAdmin(admin.ModelAdmin):
    model = SundayService


class VenueAdmin(admin.ModelAdmin):
    model = Venue


admin.site.register(Member, MemberAdmin)
admin.site.register(Ministry, MinistryAdmin)
admin.site.register(SundayService, SundayServiceAdmin)
admin.site.register(Venue, VenueAdmin)
admin.site.register(VictoryGroup, VictoryGroupAdmin)
