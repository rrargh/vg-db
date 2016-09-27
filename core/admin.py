from django.contrib import admin

# Register your models here.
from django.db.models import PositiveIntegerField
from django.forms import TextInput
from models import Disciple, SundayService, VictoryGroupLeader


class DiscipleInline(admin.TabularInline):
    model = Disciple
    extra = 0


class VictoryGroupLeaderAdmin(admin.ModelAdmin):
    model = VictoryGroupLeader
    list_display = ('full_name', 'contact_number', 'service_attended',
        'life_stage', 'vg_venue', 'vg_day', 'vg_time'
    )
    list_editable = ('contact_number', 'service_attended',
        'life_stage', 'vg_venue', 'vg_day', 'vg_time'
    )
    list_filter = ('gender', 'life_stage', 'service_attended',
        'vg_venue', 'vg_day', 'vg_time'
    )
    search_fields = ('first_name', 'last_name', 'facebook_id', 'email')
    formfield_overrides = {
        PositiveIntegerField: {'widget': TextInput(attrs={'size':'20'})},
    }
    inlines = (DiscipleInline,)


class DiscipleAdmin(admin.ModelAdmin):
    model = Disciple
    list_display = ('full_name', 'contact_number', 'service_attended',
        'life_stage', 'victory_group_leader', 'vg_venue', 'vg_day', 'vg_time'
    )
    list_editable = ('contact_number', 'service_attended',
        'life_stage', 'victory_group_leader'
    )
    list_filter = ('gender', 'life_stage', 'service_attended',
        'victory_group_leader'
    )
    search_fields = ('first_name', 'last_name', 'facebook_id', 'email')
    formfield_overrides = {
        PositiveIntegerField: {'widget': TextInput(attrs={'size':'20'})},
    }

    
class SundayServiceAdmin(admin.ModelAdmin):
    model = SundayService


admin.site.register(VictoryGroupLeader, VictoryGroupLeaderAdmin)
admin.site.register(Disciple, DiscipleAdmin)
admin.site.register(SundayService, SundayServiceAdmin)
