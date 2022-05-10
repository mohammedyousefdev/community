from django.forms import ModelForm
from django.contrib.auth.models import User

from users.models import Profile

class profileForm(ModelForm):
    class Meta:
        model=Profile
        exclude=['user','rating']
        labels={
            'first_name':'Ism',
            'last_name':'Familiya',
            'picture':'Rasm',
        }
        
    def __init__(self, *args, **kwargs):
        super(profileForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control mb-3'