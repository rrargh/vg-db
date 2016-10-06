from django.forms import ModelForm
from models import Member

class MemberForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)
        self.fields['coach'].queryset = Member.objects.exclude(
            id__exact=self.instance.pk)