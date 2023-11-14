from django import forms

from client.models import Contacts, Health, MainData
from client.utils import create_change_log_entry, create_log_entry
from users.models import User


class UserNamesForm(forms.ModelForm):
    """Form for the user names."""

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name")
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }

    def save(self, *args, **kwargs):
        """Save the instance and create a Log entry about the changes."""

        create_change_log_entry(form=self, client=self.instance)

        super().save(*args, **kwargs)


class UserEmailForm(forms.ModelForm):
    """Form for the user email."""

    class Meta:
        model = User
        fields = ("email",)
        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }

    def save(self, *args, **kwargs):
        """Save the instance and create a Log entry about the changes."""

        create_change_log_entry(form=self, client=self.instance)

        super().save(*args, **kwargs)


class MainDataForm(forms.ModelForm):
    """Form for the main information about the client."""

    header = "Основная информация"

    class Meta:
        model = MainData
        fields = (
            "sex",
            "birthday",
            "height",
        )
        widgets = {
            "sex": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "birthday": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "class": "form-control",
                    "type": "date",
                },
            ),
            "height": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "max": "300",
                },
            ),
        }

    def save(self, *args, **kwargs):
        """Save the instance and create a Log entry about the changes."""

        create_change_log_entry(form=self, client=self.instance.client)

        super().save(*args, **kwargs)


class HealthFormPage0(forms.ModelForm):
    """Form for starting the health questionnaire."""

    header = "Анкета здоровья"
    preamble = (
        "Настоящая анкета предназначена для сбора информации о здоровье "
        "и физической форме клиента в целях определения средств и методов наиболее "
        "успешного и безопасного оказания данному клиенту физкультурно-оздоровительных "
        "услуг исполнителем соответствующих услуг.\n "
        "Одновременно сведения, указанные клиентом в настоящей анкете, служат для "
        "определения возможности оказания физкультурно-оздоровительных услуг данному "
        "клиенту, а также для определения необходимости предварительного получения "
        "клиентом медицинского заключения о допуске к занятиям физической культурой."
    )

    class Meta:
        model = Health
        fields = ("confirmation",)
        widgets = {
            "confirmation": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

    def is_valid(self) -> bool:
        """Return True if the form is valid and confirmation received."""

        if self.data.get("confirmation") is None:
            self.add_error(
                "confirmation",
                "Дальше вы не пройдете, пока не подпишите бумаги.",
            )

        return self.is_bound and not self.errors

    def save(self, *args, **kwargs):
        """Save the instance and create a Log entry."""

        create_log_entry(
            form=self,
            change_message="Начато заполнение анкеты здоровья",
            client=self.instance.client,
        )

        super().save(*args, **kwargs)


class HealthFormPage1(forms.ModelForm):
    """
    Form for section 1 of the health questionnaire:
    The presence of potentially dangerous subjective feelings.
    """

    header = "1. Наличие потенциально опасных субъективных ощущений"
    preamble = "Отметьте галочкой ощущения, которые имеются в настоящее время."

    class Meta:
        model = Health
        fields = (
            "palpitation",
            "dyspnea",
            "fainting",
            "chest_pain",
            "ankles_swelling",
            "leg_cramps",
            "restriction_reasons",
        )
        widgets = {
            "palpitation": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "dyspnea": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "fainting": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "chest_pain": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "chest_pain": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "ankles_swelling": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "leg_cramps": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "restriction_reasons": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

    def save(self, *args, **kwargs):
        """Save the instance and create a Log entry about the changes."""

        create_change_log_entry(form=self, client=self.instance.client)

        super().save(*args, **kwargs)


class HealthFormPage2(forms.ModelForm):
    """
    Form for section 2 of the health questionnaire:
    The presence of diagnosed health conditions.
    """

    header = "2. Наличие диагностированных заболеваний"
    preamble = "Были в прошлом или есть в настоящее время:"

    class Meta:
        model = Health
        fields = (
            "heart_attack",
            "cardiac_surgery",
            "pacemaker",
            "arrhythmia",
            "heart_defect",
            "diabetes",
            "kidney_disease",
        )
        widgets = {
            "heart_attack": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "cardiac_surgery": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "pacemaker": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "arrhythmia": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "heart_defect": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "diabetes": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "kidney_disease": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

    def save(self, *args, **kwargs):
        """Save the instance and create a Log entry about the changes."""

        create_change_log_entry(form=self, client=self.instance.client)

        super().save(*args, **kwargs)


class HealthFormPage3(forms.ModelForm):
    """
    Form for section 3 of the health questionnaire:
    Additional health information.
    """

    header = "3. Дополнительная информация о состоянии здоровья"

    class Meta:
        model = Health
        fields = (
            "known_blood_pressure",
            "blood_pressure",
            "has_glucose_changes",
            "glucose_level",
            "has_urinary_diseases",
            "urinary_diseases",
            "has_respiratory_diseases",
            "respiratory_diseases",
            "has_digestive_diseases",
            "digestive_diseases",
            "has_oncological_diseases",
            "oncological_diseases",
            "has_vascular_diseases",
            "vascular_diseases",
            "has_trauma_or_surgeries",
            "trauma_or_surgeries",
            "has_osteoporosis_and_joint_problems",
            "osteoporosis_and_joint_problems",
            "has_other_diseases",
            "other_diseases",
            "use_medications",
            "medications",
            "follow_diet",
            "current_diet",
            "is_pregnant",
            "pregnancy_stage",
            "had_birth_in_last_six_months",
            "birth_complications",
        )
        widgets = {
            "known_blood_pressure": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "blood_pressure": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "has_glucose_changes": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "glucose_level": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "has_urinary_diseases": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "urinary_diseases": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "has_respiratory_diseases": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "respiratory_diseases": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "has_digestive_diseases": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "digestive_diseases": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "has_oncological_diseases": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "oncological_diseases": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "has_vascular_diseases": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "vascular_diseases": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "has_trauma_or_surgeries": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "trauma_or_surgeries": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "has_osteoporosis_and_joint_problems": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "osteoporosis_and_joint_problems": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "has_other_diseases": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "other_diseases": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
            "use_medications": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "medications": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
            "follow_diet": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "current_diet": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "is_pregnant": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "pregnancy_stage": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "had_birth_in_last_six_months": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "birth_complications": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
        }

    def save(self, *args, **kwargs):
        """Save the instance and create a Log entry about the changes."""

        create_change_log_entry(form=self, client=self.instance.client)

        super().save(*args, **kwargs)


class HealthFormPage4(forms.ModelForm):
    """
    Form for section 4 of the health questionnaire:
    Physical activity.
    """

    header = "4. Физическая активность"

    class Meta:
        model = Health
        fields = (
            "has_regular_training",
            "had_physical_activity",
            "previous_physical_activity",
            "current_physical_activity",
            "current_physical_activity_period",
            "has_signs_of_underrecovery_or_overtraining",
            "signs_of_underrecovery_or_overtraining",
        )
        widgets = {
            "has_regular_training": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "had_physical_activity": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "previous_physical_activity": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
            "current_physical_activity": forms.RadioSelect(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "current_physical_activity_period": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "has_signs_of_underrecovery_or_overtraining": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "signs_of_underrecovery_or_overtraining": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
        }

    def save(self, *args, **kwargs):
        """Save the instance and create a Log entry about the changes."""

        create_change_log_entry(form=self, client=self.instance.client)

        super().save(*args, **kwargs)


class HealthFormPage5(forms.ModelForm):
    """
    Form for section 5 of the health questionnaire:
    Other issues and individual requirements.
    """

    header = "5. Индивидуальные требования"

    class Meta:
        model = Health
        fields = (
            "has_work_rest_schedule_issues",
            "work_rest_schedule_issues",
            "has_other_issues",
            "other_issues",
        )
        widgets = {
            "has_work_rest_schedule_issues": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "work_rest_schedule_issues": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
            "has_other_issues": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "other_issues": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
        }

    def save(self, *args, **kwargs):
        """Save the instance and create a Log entry about the changes."""

        client = self.instance.client

        create_change_log_entry(form=self, client=client)
        create_log_entry(
            form=self,
            change_message="Клиент завершил заполнение анкеты.",
            client=client,
        )

        super().save(*args, **kwargs)


class HealthFormResult(forms.ModelForm):
    """
    Form for the result of the health questionnaire for expert:
    Readiness for physical activity.
    """

    class Meta:
        model = Health
        fields = (
            "workout_readiness",
            "client",
        )
        widgets = {
            "client": forms.HiddenInput(),
            "workout_readiness": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }


FIRST_HEALTH_FORM_PAGE = 0
LAST_HEALTH_FORM_PAGE = 5
HEALTH_FORMS = {
    0: HealthFormPage0,
    1: HealthFormPage1,
    2: HealthFormPage2,
    3: HealthFormPage3,
    4: HealthFormPage4,
    5: HealthFormPage5,
}


class ContactsForm(forms.ModelForm):
    """Form for contacts of client."""

    header = "Контакты"

    class Meta:
        model = Contacts
        fields = (
            "telegram",
            "whatsapp",
            "discord",
            "skype",
            "vkontakte",
            "facebook",
            "preferred_contact",
        )
        widgets = {
            "telegram": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://t.me/your_telegram_username",
                }
            ),
            "whatsapp": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://wa.me/your_whatsapp_number",
                }
            ),
            "discord": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "discord.gg/your_discord_server or username",
                }
            ),
            "skype": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://join.skype.com/my_code",
                }
            ),
            "vkontakte": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://vk.com/your_vk_username_or_id",
                }
            ),
            "facebook": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://www.facebook.com/your_facebook_username.id",
                }
            ),
            "preferred_contact": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }

    def save(self, *args, **kwargs):
        """Save the instance and create a Log entry about the changes."""

        create_change_log_entry(form=self, client=self.instance.client)

        super().save(*args, **kwargs)