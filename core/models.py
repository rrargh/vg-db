from __future__ import unicode_literals

from django.db.models import Model, ForeignKey, \
    CharField, DateField, DateTimeField, \
    EmailField, PositiveIntegerField


GENDER = (
    ("M", "Male"),
    ("F", "Female")
)

LIFE_STAGES = (
    ("Kids", "Kids"),
    ("High School", "High School"),
    ("College", "College"),
    ("Single", "Single"),
    ("Married", "Married"),
    ("Solo Parent", "Solo Parent"),
    ("Senior", "Senior"),
    ("Other", "Other")
)

VG_DAYS = (
    ("Sun", "Sun"),
    ("Mon", "Mon"),
    ("Tue", "Tue"),
    ("Wed", "Wed"),
    ("Thu", "Thu"),
    ("Fri", "Fri"),
    ("Sat", "Sat")
)

VG_TIMES = (
    ("Morning", "Morning"),
    ("Afternoon", "Afternoon"),
    ("Evening", "Evening")
)


# Create your models here.
class CoreModel(Model):
    created = DateTimeField(auto_now_add=True)
    last_updated = DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SundayService(CoreModel):
    schedule = CharField(max_length=20)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.schedule


class MemberModel(CoreModel):
    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100)
    contact_number = CharField(max_length=100, null=True, blank=True)
    gender = CharField(max_length=1, choices=GENDER)
    birthdate = DateField(null=True, blank=True)
    facebook_id = CharField(
        "Facebook ID", max_length=200, null=True, blank=True
    )
    email = EmailField(null=True, blank=True)
    life_stage = CharField(max_length=20, choices=LIFE_STAGES)
    service_attended = ForeignKey(SundayService, null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ('last_name',)

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)


class VictoryGroupLeader(MemberModel):
    vg_venue = CharField("Victory group venue", max_length=200)
    vg_day = CharField("Victory group day", max_length=3, choices=VG_DAYS)
    vg_time = CharField("Victory group time", max_length=10, choices=VG_TIMES)


class Disciple(MemberModel):
    victory_group_leader = ForeignKey(VictoryGroupLeader, null=True, blank=True)

    @property
    def vg_venue(self):
        return self.victory_group_leader.vg_venue

    @property
    def vg_day(self):
        return self.victory_group_leader.vg_day

    @property
    def vg_time(self):
        return self.victory_group_leader.vg_time

