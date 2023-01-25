from django.forms import ModelForm, HiddenInput, DateInput, Textarea
from .models import Commentary, Clientnote, FullClientnote


class CommentaryForm(ModelForm):
    """Форма для комментария для клиента от эксперта"""
    class Meta:
        model = Commentary
        fields = [
            'date',
            'client',
            'general',
            'measurements',
            'nutrition',
            'workout',
            ]
        widgets = {
            'date': DateInput(attrs={
                'class': 'form-control text-center p-1 transition_common',
                'type': 'date',
                'id': "id_date_comment",
                'readonly': False,
            }),
            'client': HiddenInput(),
            'general': Textarea(attrs={
                'class': 'form-control hidden_element mb-2',
                'id': "id_general_comment",
            }),
            'measurements': Textarea(attrs={
                'class': 'form-control hidden_element mb-2',
                'id': "id_measurements_comment",
            }),
            'nutrition': Textarea(attrs={
                'class': 'form-control hidden_element mb-2',
                'id': "id_nutrition_comment",
            }),
            'workout': Textarea(attrs={
                'class': 'form-control hidden_element mb-2',
                'id': "id_workout_comment",
            }),
        }


class ClientnoteForm(ModelForm):
    """Форма для заметки о клиенте от эксперта по месяцам"""
    class Meta:
        model = Clientnote
        fields = [
            'date',
            'client',
            'general',
            'measurements',
            'nutrition',
            'workout',
            ]
        widgets = {
            'date': DateInput(attrs={
                'class': 'form-control text-center p-1 transition_common',
                'type': 'month',
                'id': "id_date_note",
                'readonly': False,
            }),
            'client': HiddenInput(),
            'general': Textarea(attrs={
                'class': 'form-control hidden_element mb-2',
                'id': "id_general_note",
            }),
            'measurements': Textarea(attrs={
                'class': 'form-control hidden_element mb-2',
                'id': "id_measurements_note",
            }),
            'nutrition': Textarea(attrs={
                'class': 'form-control hidden_element mb-2',
                'id': "id_nutrition_note",
            }),
            'workout': Textarea(attrs={
                'class': 'form-control hidden_element mb-2',
                'id': "id_workout_note",
            }),
        }


class FullClientnoteForm(ModelForm):
    """Форма для заметки о клиенте от эксперта совокупная"""
    class Meta:
        model = FullClientnote
        fields =  [
            'client',
            'note',
            ]
        widgets = {
            'client': HiddenInput(),
            'note': Textarea(attrs={
                'class': 'form-control mb-2',
                'id': "id_full_note",
                'rows': "15",
            }),
        }
      