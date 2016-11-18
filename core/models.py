from __future__ import unicode_literals
from datetime import date
from django.core.exceptions import ValidationError
from django.db.models import Max, Min, Model, ForeignKey, \
    BooleanField, CharField, DateField, DateTimeField, \
    EmailField, NullBooleanField, PositiveIntegerField


DEMOGRAPHICS = (
    ("Kids", "Kids"),
    ("Campus", "Campus"),
    ("Singles", "Singles"),
    ("Family", "Family"),
    ("Single Parents", "Single Parents"),
    ("Seniors", "Seniors")
)

GENDERS = (
    ("M", "Male"),
    ("F", "Female")
)

GROUP_TYPES = (
    ("Males", "All Males"),
    ("Females", "All Females"),
    ("Mixed", "Mixed")
)

LIFE_STAGES = (
    ("Kids", "Kids"),
    ("High School", "High School"),
    ("College", "College"),
    ("Single", "Single"),
    ("Married", "Married"),
    ("Solo Parent", "Solo Parent"),
    ("Senior", "Senior"),
    ("Widow", "Widow"),
    ("Other", "Other")
)

MONTHS = (
    ("Jan", "Jan"),
    ("Feb", "Feb"),
    ("Mar", "Mar"),
    ("Apr", "Apr"),
    ("May", "May"),
    ("Jun", "Jun"),
    ("Jul", "Jul"),
    ("Aug", "Aug"),
    ("Sep", "Sep"),
    ("Oct", "Oct"),
    ("Nov", "Nov"),
    ("Dec", "Dec")
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


class Ministry(CoreModel):
    name = CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Ministries"
        ordering = ('name',)

    def __str__(self):
        return self.name


class SundayService(CoreModel):
    schedule = CharField(max_length=20)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.schedule


class Venue(CoreModel):
    name = CharField(max_length=100)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

#FIXME: what fields should be unique?
class Member(CoreModel):
    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100)
    nickname = CharField(max_length=100, null=True, blank=True)
    contact_number = CharField(max_length=100, null=True, blank=True)
    birthdate = DateField(null=True, blank=True)
    age = PositiveIntegerField(null=True, blank=True)
    gender = CharField(max_length=1, choices=GENDERS)
    facebook_id = CharField(
        "Facebook ID", max_length=200, null=True, blank=True
    )
    email = EmailField(null=True, blank=True)
    life_stage = CharField(max_length=20, choices=LIFE_STAGES)
    service_attended = ForeignKey(SundayService, null=True, blank=True)
    ministry = ForeignKey(Ministry, null=True, blank=True)
    coach = ForeignKey('self', null=True, blank=True,
        verbose_name="VG Leader or Leadership Group Leader"
    )
    victory_group = ForeignKey("VictoryGroup", null=True, blank=True,
        verbose_name="Under whose victory group?"
    )
    one2one = NullBooleanField("Finished One2One?")
    victory_weekend = NullBooleanField("Finished Victory Weekend?")
    church_community = NullBooleanField("Finished Church Community?")
    purple_book = NullBooleanField("Finished Purple Book?")
    making_disciples = NullBooleanField("Finished Making Disciples?")
    empowering_leaders = NullBooleanField("Finished Empowering Leaders?")
    leadership113 = NullBooleanField("Finished Leadership 113?")
    doing_one2one = NullBooleanField("Doing One2One?") #FIXME: account for season
    is_vg_leader = NullBooleanField("Leader of a victory group?")
    is_active = BooleanField(default=True)

    class Meta:
        ordering = ('last_name', 'first_name')
        unique_together = (('last_name', 'first_name', 'gender', 'birthdate'),)

    def __str__(self):
        return "%s, %s" % (self.last_name, self.first_name)
        # return self.full_name

    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def get_age(self):
        if self.birthdate is not None:
            today = date.today()
            return today.year - self.birthdate.year - (
                (today.month, today.day) < (self.birthdate.month, self.birthdate.day)
            )
        return None

    def clean(self):
        if Member.objects.filter(
                last_name=self.last_name,
                first_name=self.first_name,
                gender=self.gender,
                birthdate=self.birthdate,
                ).exclude(id=self.id).exists():
            raise ValidationError("Member entry already exists for %s" % self.full_name)

    def save(self, *args, **kwargs):
        if self.get_age() is not None:
            self.age = self.get_age()

        super(Member, self).save(*args, **kwargs)

# FIXME: unique fields: leader, day, time, venue?
class VictoryGroup(CoreModel):
    leader = ForeignKey(Member, related_name="leader")
    co_leader = ForeignKey(Member, null=True, blank=True,
        related_name="co_leader"
    )
    vg_intern = ForeignKey(Member, verbose_name="Intern", null=True, blank=True,
        related_name="intern"
    )
    demographic = CharField(max_length=20, choices=DEMOGRAPHICS)
    group_type = CharField(max_length=10, choices=GROUP_TYPES)
    group_age = CharField(max_length=20, null=True, blank=True)
    month_started = CharField(max_length=3, null=True, blank=True, choices=MONTHS)
    year_started = PositiveIntegerField(null=True, blank=True)
    day = CharField(max_length=3, choices=VG_DAYS)
    time = CharField(max_length=10, choices=VG_TIMES)
    venue = ForeignKey(Venue)
    member_count = PositiveIntegerField(null=True)
    is_active = BooleanField(default=True)

    class Meta:
        ordering = ('leader',)

    def __str__(self):
        return "%s - %s %s at %s" % (
            self.leader.full_name,
            self.day,
            self.time,
            self.venue
        )

    # @property
    def get_members(self):
        members = self.member_set.exclude(id=self.leader.id)
        if self.co_leader is not None:
            members = members.exclude(id=self.co_leader.id)
        if members.count() > 0:
            return members
        return None

    # @property
    def get_member_count(self):
        if self.get_members() is not None:
            return self.get_members().count()
        return 0

    def get_youngest_age(self):
        if self.get_member_count() > 0:
            members = self.get_members()
            return members.aggregate(Min('age'))["age__min"]
        return None

    def get_oldest_age(self):
        if self.get_member_count() > 0:
            members = self.get_members()
            return members.aggregate(Max('age'))["age__max"]
        return None

    def clean(self):
        if VictoryGroup.objects.filter(
                leader=self.leader,
                demographic=self.demographic,
                group_type=self.group_type,
                day=self.day,
                time=self.time,
                venue=self.venue,
                ).exclude(id=self.id).exists():
            raise ValidationError("Victory group entry already exists for %s" % self)

    def save(self, *args, **kwargs):
        self.member_count = self.get_member_count()
        youngest_age = None
        oldest_age = None
        if self.get_youngest_age() is not None:
            youngest_age = self.get_youngest_age()
        if self.get_oldest_age() is not None:
            oldest_age = self.get_oldest_age()
        if youngest_age is not None and oldest_age is not None:
            self.group_age = "%s to %s" % (youngest_age, oldest_age)
        elif youngest_age is None and oldest_age is not None:
            self.group_age = "Up to %s" % oldest_age
        elif youngest_age is not None and oldest_age is None:
            self.group_age = "%s up" % youngest_age
        super(VictoryGroup, self).save(*args, **kwargs)
