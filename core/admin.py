from datetime import date
from django.contrib import admin

# Register your models here.
from django.forms import TextInput
from django.http import HttpResponse
from django.utils.encoding import smart_unicode
from forms import MemberForm
from models import Member, Ministry, SundayService, \
    Venue, VictoryGroup


admin.site.disable_action('delete_selected')


def batch_download_csv(self, request, queryset):
    export_fields = self.list_for_export
    display_fields = self.list_display[1:]
    export_dict = dict(request.GET.items())
    export_dict.pop("q", None)
    field_index = int(export_dict.pop("o", 0)) - 1
    sort_by = export_dict.pop("ot", None)
    if 0 <= field_index < len(display_fields) and sort_by in ["asc", "desc"]:
        sort_column = display_fields[field_index]
        if sort_by == "asc":
            sort_order = ""
        else:
            sort_order = "-"
        try:
            result_set = queryset.filter(**export_dict).order_by(
                "%s%s" % (sort_order, sort_column)
            )
        except:
            result_set = queryset.filter(**export_dict)
    else:
        result_set = queryset.filter(**export_dict)

    f = '|'.join(export_fields)
    for obj in result_set:
        f += '\n' + '|'.join(
            [smart_unicode(getattr(obj, field)) for field in export_fields]
        )

    response = HttpResponse(f,content_type='text/csv')
    response['Content-Disposition'] = "attachment; filename=%s_%s.csv" % (
        self.model.__name__,
        date.today()
    )
    return response

def batch_download_xls(self, request, queryset):
    export_fields = self.list_for_export
    display_fields = self.list_display[1:]
    export_dict = dict(request.GET.items())
    export_dict.pop("q", None)
    field_index = int(export_dict.pop("o", 0)) - 1
    sort_by = export_dict.pop("ot", None)
    if 0 <= field_index < len(display_fields) and sort_by in ["asc", "desc"]:
        sort_column = display_fields[field_index]
        if sort_by == "asc":
            sort_order = ""
        else:
            sort_order = "-"
        try:
            result_set = queryset.filter(
                **export_dict).order_by("%s%s" % (sort_order, sort_column))
        except:
            result_set = queryset.filter(**export_dict)
    else:
        result_set = queryset.filter(**export_dict)

    import xlwt
    workbook = xlwt.Workbook(encoding = 'ascii')
    worksheet = workbook.add_sheet('report')
    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'yyyy-mm-dd'
    for field in export_fields:
        worksheet.write(0, export_fields.index(field), field)
    INDEX_START = 1
    for index, obj in enumerate(result_set, INDEX_START):
        for field in export_fields:
            if field in ['age', 'member_count', 'year_started']:
                worksheet.write(
                    index,
                    export_fields.index(field),
                    getattr(obj, field)
                )
            elif field in ['birthdate']:
                try:
                    worksheet.write(
                        index,
                        export_fields.index(field),
                        getattr(obj, field),
                        date_format
                    )
                except:
                    worksheet.write(
                        index,
                        export_fields.index(field),
                        smart_unicode(getattr(obj, field))
                        )
            else:
                worksheet.write(
                    index,
                    export_fields.index(field),
                    smart_unicode(getattr(obj, field))
                    )

    xls_response = HttpResponse(content_type="application/ms-excel")
    xls_response['Content-Disposition'] = 'attachment; filename=%s_%s.xls' % (
        self.model.__name__,
        date.today()
    )
    workbook.save(xls_response)
    return xls_response

batch_download_csv.short_description = "Export as CSV"
batch_download_xls.short_description = "Export as XLS"


class MemberAdmin(admin.ModelAdmin):
    model = Member
    form = MemberForm

    list_display = ('full_name', 'contact_number', 'service_attended',
        'life_stage', 'ministry', 'coach',
        'is_vg_leader', 'is_active'
    )
    list_editable = ('contact_number', 'service_attended',
        'life_stage', 'ministry', 'coach',
        'is_vg_leader', 'is_active'
    )
    list_filter = ('gender', 'life_stage', 'service_attended', 'ministry',
        'one2one', 'victory_weekend', 'church_community', 'purple_book',
        'making_disciples', 'empowering_leaders', 'leadership113', 'doing_one2one'
    )
    list_for_export = (
        'first_name', 'last_name', 'nickname',
        'birthdate', 'gender', 'life_stage',
        'contact_number', 'facebook_id', 'email',
        'service_attended', 'ministry', 'coach', 'victory_group',
        'doing_one2one', 'is_vg_leader', 'is_active',
        'one2one', 'victory_weekend', 'church_community',
        'purple_book', 'making_disciples',
        'empowering_leaders', 'leadership113'
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
    actions = [batch_download_csv, batch_download_xls]


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
        'year_started', 'day', 'time', 'venue', 'is_active'
    )
    list_for_export = (
        'leader', 'co_leader', 'vg_intern',
        'demographic', 'group_type', 'group_age',
        'month_started', 'year_started',
        'day', 'time', 'venue',
        'member_count', 'is_active'
    )
    readonly_fields = ('member_count',)
    search_fields = ('leader', 'co_leader', 'vg_intern')
    inlines = (MemberInline,)
    actions = [batch_download_csv, batch_download_xls]

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
