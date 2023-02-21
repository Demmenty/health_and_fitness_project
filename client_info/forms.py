from .models import (
    HealthQuestionary,
    MeetQuestionary,
    ClientContact,
    ClientMemo,
    )
from django.forms import (
    ModelForm,
    TextInput,
    Textarea,
    Select,
    SelectDateWidget,
    CheckboxInput,
    NumberInput,
    HiddenInput,
    )


class ClientContactForm(ModelForm):
    class Meta:
        model = ClientContact
        fields = [
            'telegram',
            'whatsapp',
            'discord',
            'skype',
            'vkontakte',
            'facebook',
            'preferred_contact',
        ]
        widgets = {
            'telegram': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 't.me/myname'
            }),
            'whatsapp': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://wa.me/myphone'
            }),
            'discord': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Myusername'
            }),
            'skype': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'join.skype.com/invite/mycode'
            }),
            'vkontakte': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://vk.com/myid'
            }),
            'facebook': TextInput(attrs={
                'class': 'form-control mb-4',
                'placeholder': 'www.facebook.com/myname&id'
            }),
            'preferred_contact': Select(attrs={
                'class': 'form-control mb-2',
            }),
        }


class ClientMemoForm(ModelForm):
    class Meta:
        model = ClientMemo
        fields = [
            'client',
            'general',
            'measurements',
            'nutrition',
            'workout',
        ]
        widgets = {
            'client': HiddenInput(),
            'general': Textarea(attrs={
                'class': 'form-control hidden_element mb-2',
                'id': "memo_general_textarea",
            }),
            'measurements': Textarea(attrs={
                'class': 'form-control hidden_element mb-2',
                'id': "memo_measurements_textarea",
            }),
            'nutrition': Textarea(attrs={
                'class': 'form-control hidden_element mb-2',
                'id': "memo_nutrition_textarea",
            }),
            'workout': Textarea(attrs={
                'class': 'form-control hidden_element mb-2',
                'id': "memo_workout_textarea",
            }),
        }


class HealthQuestionaryForm(ModelForm):
    class Meta:
        model = HealthQuestionary
        fields = [
            'fullname',
            'birth_date',
            'parameter11',
            'parameter12',
            'parameter13',
            'parameter14',
            'parameter15',
            'parameter16',
            'parameter17',
            'parameter20',
            'parameter31',
            'parameter32',
            'parameter33',
            'parameter34',
            'parameter35',
            'parameter36',
            'norm_pressure',
            'parameter42',
            'parameter43',
            'parameter44',
            'parameter45',
            'parameter46',
            'parameter47',
            'parameter48',
            'parameter49',
            'parameter410',
            'parameter411',
            'parameter412',
            'parameter413',
            'parameter414',
            'parameter415',
            'parameter416',
            'parameter416_exp',
            'parameter417',
            'parameter418',
            'parameter419',
            'confirm'
            ]
        widgets = {
            'fullname': TextInput(attrs={
                'class': 'form-control fs-5 text-center',
            }),
            'birth_date': SelectDateWidget(
                years=range(1920, 2020),
                attrs={'class': 'form-control',
            }),
            'parameter11': TextInput(attrs={
                'class': 'hidden_element',
            }),
            'parameter12': TextInput(attrs={
                'class': 'hidden_element',
            }),
            'parameter13': TextInput(attrs={
                'class': 'hidden_element',
            }),
            'parameter14': TextInput(attrs={
                'class': 'hidden_element',
            }),
            'parameter15': TextInput(attrs={
                'class': 'hidden_element',
            }),
            'parameter16': TextInput(attrs={
                'class': 'hidden_element',
            }),
            'parameter17': TextInput(attrs={
                'class': 'hidden_element',
            }),
            'parameter20': TextInput(attrs={
                'class': 'hidden_element',
            }),
            'parameter31': TextInput(attrs={
                'class': 'hidden_element',
            }),
            'parameter32': TextInput(attrs={
                'class': 'hidden_element',
            }),
            'parameter33': TextInput(attrs={
                'class': 'hidden_element',
            }),
            'parameter34': TextInput(attrs={
                'class': 'hidden_element',
            }),
            'parameter35': TextInput(attrs={
                'class': 'hidden_element',
            }),
            'parameter36': TextInput(attrs={
                'class': 'hidden_element',
            }),
            'norm_pressure': TextInput(attrs={
                'class': 'form-control hidden_element',
                'placeholder': 'Укажите его',
            }),
            'parameter42': TextInput(attrs={
                'class': 'form-control hidden_element',
                'placeholder': 'Укажите свой уровень',
            }),
            'parameter43': TextInput(attrs={
                'class': 'form-control hidden_element',
                'placeholder': 'Перечислите их',
            }),
            'parameter44': TextInput(attrs={
                'class': 'form-control hidden_element',
                'placeholder': 'Перечислите их',
            }),
            'parameter45': TextInput(attrs={
                'class': 'form-control hidden_element',
                'placeholder': 'Перечислите их',
            }),
            'parameter46': TextInput(attrs={
                'class': 'form-control hidden_element',
                'placeholder': 'Перечислите их',
            }),
            'parameter47': TextInput(attrs={
                'class': 'form-control hidden_element',
                'placeholder': 'Перечислите их',
            }),
            'parameter48': TextInput(attrs={
                'class': 'form-control hidden_element',
                'placeholder': 'Перечислите какие и когда',
            }),
            'parameter49': TextInput(attrs={
                'class': 'form-control hidden_element',
                'placeholder': 'Перечислите их',
            }),
            'parameter410': TextInput(attrs={
                'class': 'form-control hidden_element',
                'placeholder': 'Перечислите их',
            }),
            'parameter411': TextInput(attrs={
                'class': 'form-control hidden_element',
                'placeholder': 'Укажите срок беременности',
            }),
            'parameter412': TextInput(attrs={
                'class': 'form-control hidden_element',
                'placeholder': 'Укажите, были ли осложнения до, во время и после родов и какие',
            }),
            'parameter413': TextInput(attrs={
                'class': 'form-control hidden_element',
                'placeholder': 'Перечислите их',
            }),
            'parameter414': TextInput(attrs={
                'class': 'form-control hidden_element',
                'placeholder': 'Укажите, какую',
            }),
            'parameter415': TextInput(attrs={
                'class': 'form-control hidden_element',
                'placeholder': 'Перечислите какие и когда',
            }),
            'parameter416': TextInput(attrs={
                'class': 'form-control hidden_element',
            }),
            'parameter416_exp': TextInput(attrs={
                'class': 'form-control hidden_element',
                'placeholder': 'Укажите стаж занятий',
            }),
            'parameter417': TextInput(attrs={
                'class': 'form-control hidden_element',
                'placeholder': 'Перечислите их',
            }),
            'parameter418': TextInput(attrs={
                'class': 'form-control hidden_element',
                'placeholder': 'Укажите их',
            }),
            'parameter419': TextInput(attrs={
                'class': 'form-control hidden_element',
                'placeholder': 'Перечислите их',
            }),
            'confirm': CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }


class MeetQuestionaryForm(ModelForm):
    class Meta:
        model = MeetQuestionary
        fields = [
            'sex',
            'sex_comment',
            'height',
            'weight',
            'weight_min',
            'weight_max',
            'weight_avg',
            'daily_steps',
            'sleep_time',
            'wakeup_time',
            'sleep_problems',
            'daily_meals_amount',
            'daily_snacks_amount',
            'common_meal',
            'weekly_meal',
            'yearly_meal',
            'favorite_meal',
            'goal',
            'goal_mark',
            'goal_attempts',
            'goal_obstacle',
            'goal_importance',
            'goal_maxtime',
            'readiness_to_change',
        ]
        widgets = {
            'sex': Select(attrs={
                'class': 'form-control text-center',
            }),
            'sex_comment': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'прокомментируйте свой ответ',
                'rows': "2",
            }),
            'height': NumberInput(attrs={
                'class': 'form-control d-inline text-center',
                'min': '0',
            }),
            'weight': NumberInput(attrs={
                'class': 'form-control d-inline text-center',
                'min': '0',
            }),
            'weight_min': NumberInput(attrs={
                'class': 'form-control d-inline text-center',
                'min': '0',
            }),
            'weight_max': NumberInput(attrs={
                'class': 'form-control d-inline text-center',
                'min': '0',
            }),
            'weight_avg': NumberInput(attrs={
                'class': 'form-control d-inline text-center',
                'min': '0',
            }),
            'daily_steps': TextInput(attrs={
                'class': 'form-control text-center',
            }),
            'sleep_time': TextInput(attrs={
                'class': 'form-control text-center',
            }),
            'wakeup_time': TextInput(attrs={
                'class': 'form-control text-center',
            }),
            'sleep_problems': Textarea(attrs={
                'class': 'form-control',
                'rows': "6",
            }),
            'daily_meals_amount': TextInput(attrs={
                'class': 'form-control text-center',
            }),
            'daily_snacks_amount': TextInput(attrs={
                'class': 'form-control text-center',
            }),
            'common_meal': Textarea(attrs={
                'class': 'form-control',
                'rows': "6",
            }),
            'weekly_meal': Textarea(attrs={
                'class': 'form-control',
                'rows': "6",
            }),
            'yearly_meal': Textarea(attrs={
                'class': 'form-control',
                'rows': "6",
            }),
            'favorite_meal': Textarea(attrs={
                'class': 'form-control',
                'rows': "6",
            }),
            'goal': Textarea(attrs={
                'class': 'form-control',
                'rows': "6",
            }),
            'goal_mark': Textarea(attrs={
                'class': 'form-control',
                'rows': "6",
            }),
            'goal_attempts': Textarea(attrs={
                'class': 'form-control',
                'rows': "6",
            }),
            'goal_obstacle': Textarea(attrs={
                'class': 'form-control',
                'rows': "6",
            }),
            'goal_importance': NumberInput(attrs={
                'class': 'form-range',
                'type': 'range',
                'max': '10',
                'oninput': "goalvalue.value=value",
            }),
            'goal_maxtime': Textarea(attrs={
                'class': 'form-control',
                'rows': "6",
            }),
            'readiness_to_change': NumberInput(attrs={
                'class': 'form-range',
                'type': 'range',
                'min': '1',
                'max': '6',
                'oninput': "readinessvalue.value=value",
            })
        }
