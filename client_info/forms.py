from .models import HealthQuestionary, ClientContact
from django.forms import ModelForm, TextInput, Select, SelectDateWidget, CheckboxInput


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
            }),
            'whatsapp': TextInput(attrs={
                'class': 'form-control',
            }),
            'discord': TextInput(attrs={
                'class': 'form-control',
            }),
            'skype': TextInput(attrs={
                'class': 'form-control',
            }),
            'vkontakte': TextInput(attrs={
                'class': 'form-control',
            }),
            'facebook': TextInput(attrs={
                'class': 'form-control mb-4',
            }),
            'preferred_contact': Select(attrs={
                'class': 'form-control',
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
