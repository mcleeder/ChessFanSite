from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.forms import ModelForm
from .helpers import get_users_from_db, get_groups_from_db
from .models import ChessGameGroup

MONTH_CHOICES = [
    ('01', 'January'),
    ('02', 'February'),
    ('03', 'March'),
    ('04', 'April'),
    ('05', 'May'),
    ('06', 'June'),
    ('07', 'July'),
    ('08', 'August'),
    ('09', 'September'),
    ('10', 'October'),
    ('11', 'November'),
    ('12', 'December'),
]


# TODO: generate this list from datetime

YEAR_CHOICES = [
    (2010, 2010),
    (2011, 2011),
    (2012, 2012),
    (2013, 2013),
    (2014, 2014),
    (2015, 2015),
    (2016, 2016),
    (2017, 2017),
    (2018, 2018),
    (2019, 2019),
    (2020, 2020)
]

USERS_IN_DB = get_users_from_db

GROUPS_IN_DB = get_groups_from_db


class CreateGroup(ModelForm):
    player1 = forms.ChoiceField(choices=USERS_IN_DB)
    player2 = forms.ChoiceField(choices=USERS_IN_DB)

    class Meta:
        model = ChessGameGroup
        fields = ['title', 'player1', 'player2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_action = 'create_group'
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))


class GroupStats(ModelForm):
    title = forms.ChoiceField(choices=GROUPS_IN_DB)

    class Meta:
        model = ChessGameGroup
        fields = ['title']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_action = 'group_stats'
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))


class GetGamesByPlayer(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=120,
        required=True,
    )
    month = forms.ChoiceField(
        choices=MONTH_CHOICES,
    )
    year = forms.ChoiceField(
        choices=YEAR_CHOICES,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-getgames'
        self.helper.form_method = 'POST'
        self.helper.form_action = 'load_data'
        self.helper.add_input(Submit('submit', 'Load Games'))


class GetGameDetails(forms.Form):
    game_id = forms.CharField(
        max_length=20,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-getgamedetails'
        self.helper.form_method = 'POST'
        self.helper.form_action = 'game_details'
        self.helper.add_input(Submit('submit', 'Details'))

