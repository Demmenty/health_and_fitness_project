from django.forms import (
    CheckboxInput,
    ClearableFileInput,
    DateInput,
    EmailInput,
    HiddenInput,
    ModelForm,
    NumberInput,
    RadioSelect,
    Select,
    Textarea,
    TextInput,
)
from django.urls import reverse

from client.models import Contacts, Food, Goal, Health, Note, Sleep, Weight
from client.utils import create_change_log_entry, create_log_entry
from users.models import User


class NoteForm(ModelForm):
    """Form for the client's personal note."""

    class Meta:
        model = Note
        fields = ("general", "measurements", "nutrition", "workout")
        widgets = {
            "general": Textarea(
                attrs={
                    "class": "form-control border-top-0 rounded-0 rounded-bottom",
                    "rows": 19,
                }
            ),
            "measurements": Textarea(
                attrs={
                    "class": "form-control border-top-0 rounded-0 rounded-bottom",
                    "rows": 19,
                }
            ),
            "nutrition": Textarea(
                attrs={
                    "class": "form-control border-top-0 rounded-0 rounded-bottom",
                    "rows": 19,
                }
            ),
            "workout": Textarea(
                attrs={
                    "class": "form-control border-top-0 rounded-0 rounded-bottom",
                    "rows": 19,
                }
            ),
        }


class ProfileForm(ModelForm):
    """Form for the user main information."""

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "sex",
            "birthday",
            "height",
            "avatar",
        )
        widgets = {
            "username": TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "first_name": TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "last_name": TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "avatar": ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",
                }
            ),
            "sex": Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "birthday": DateInput(
                format="%Y-%m-%d",
                attrs={
                    "class": "form-control",
                    "type": "date",
                },
            ),
            "height": NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "max": "300",
                },
            ),
        }

    def save(self, *args, **kwargs):
        """Save the instance and create a Log entry about the changes."""

        client = self.instance
        link = reverse("expert:client_profile") + f"?client_id={client.id}"
        create_change_log_entry(form=self, client=client, link=link)

        super().save(*args, **kwargs)


class UserEmailForm(ModelForm):
    """Form for the user email."""

    class Meta:
        model = User
        fields = ("email",)
        widgets = {
            "email": EmailInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }

    def save(self, *args, **kwargs):
        """Save the instance and create a Log entry about the changes."""

        client = self.instance
        link = reverse("expert:client_profile") + f"?client_id={client.id}"
        create_change_log_entry(form=self, client=client, link=link)

        super().save(*args, **kwargs)


class WeightForm(ModelForm):
    """Form for the client's start weight data."""

    class Meta:
        model = Weight
        fields = (
            "weight_current",
            "weight_min",
            "weight_max",
            "weight_avg",
        )
        widgets = {
            "weight_current": NumberInput(
                attrs={
                    "class": "form-control text-center",
                }
            ),
            "weight_min": NumberInput(
                attrs={
                    "class": "form-control text-center",
                }
            ),
            "weight_max": NumberInput(
                attrs={
                    "class": "form-control text-center",
                }
            ),
            "weight_avg": NumberInput(
                attrs={
                    "class": "form-control text-center",
                }
            ),
        }

    def save(self, *args, **kwargs):
        """Save the instance and create a Log entry about the changes."""

        client = self.instance.client
        link = reverse("expert:client_weight") + f"?client_id={client.id}"

        if self.instance.id:
            create_change_log_entry(form=self, client=client, link=link)
        else:
            create_log_entry(
                modelname=self.Meta.model._meta.verbose_name,
                description="Клиент заполнил анкету",
                client=client,
                link=link,
            )

        super().save(*args, **kwargs)


class SleepForm(ModelForm):
    """Form for the client's sleep data."""

    class Meta:
        model = Sleep
        fields = (
            "time_asleep",
            "time_wakeup",
            "problems",
        )
        widgets = {
            "time_asleep": TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "time_wakeup": TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "problems": Textarea(
                attrs={
                    "class": "form-control",
                }
            ),
        }

    def save(self, *args, **kwargs):
        """Save the instance and create a Log entry about the changes."""

        client = self.instance.client
        link = reverse("expert:client_sleep") + f"?client_id={client.id}"

        if self.instance.id:
            create_change_log_entry(form=self, client=client, link=link)
        else:
            create_log_entry(
                modelname=self.Meta.model._meta.verbose_name,
                description="Клиент заполнил анкету",
                client=client,
                link=link,
            )

        super().save(*args, **kwargs)


class FoodForm(ModelForm):
    """Form for the client's start food data."""

    class Meta:
        model = Food
        fields = (
            "daily_meal_amount",
            "daily_snack_amount",
            "common",
            "weekly",
            "yearly",
            "favorite",
        )
        widgets = {
            "daily_meal_amount": TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "daily_snack_amount": TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "common": Textarea(
                attrs={
                    "class": "form-control",
                    "rows": "8",
                }
            ),
            "weekly": Textarea(
                attrs={
                    "class": "form-control",
                    "rows": "8",
                }
            ),
            "yearly": Textarea(
                attrs={
                    "class": "form-control",
                    "rows": "8",
                }
            ),
            "favorite": Textarea(
                attrs={
                    "class": "form-control",
                    "rows": "8",
                }
            ),
        }

    def save(self, *args, **kwargs):
        """Save the instance and create a Log entry about the changes."""

        client = self.instance.client
        link = reverse("expert:client_food") + f"?client_id={client.id}"

        if self.instance.id:
            create_change_log_entry(form=self, client=client, link=link)
        else:
            create_log_entry(
                modelname=self.Meta.model._meta.verbose_name,
                description="Клиент заполнил анкету",
                client=client,
                link=link,
            )

        super().save(*args, **kwargs)


class GoalForm(ModelForm):
    """Form for the client's goal."""

    class Meta:
        model = Goal
        fields = (
            "description",
            "measure",
            "attempts",
            "obstacles",
            "importance",
            "maxtime",
            "readiness",
        )
        widgets = {
            "description": Textarea(
                attrs={
                    "class": "form-control",
                }
            ),
            "measure": Textarea(
                attrs={
                    "class": "form-control",
                }
            ),
            "attempts": Textarea(
                attrs={
                    "class": "form-control",
                }
            ),
            "obstacles": Textarea(
                attrs={
                    "class": "form-control",
                }
            ),
            "importance": NumberInput(
                attrs={
                    "class": "form-range",
                    "type": "range",
                    "min": "0",
                    "max": "10",
                    "oninput": "importanceoutput.value=value",
                }
            ),
            "maxtime": Textarea(
                attrs={
                    "class": "form-control",
                }
            ),
            "readiness": NumberInput(
                attrs={
                    "class": "form-range",
                    "type": "range",
                    "min": "1",
                    "max": "6",
                    "oninput": "readinessoutput.value=value",
                }
            ),
        }

    def save(self, *args, **kwargs):
        """Save the instance and create a Log entry about the changes."""

        client = self.instance.client
        link = reverse("expert:client_goal") + f"?client_id={client.id}"

        if self.instance.id:
            create_change_log_entry(form=self, client=client, link=link)
        else:
            create_log_entry(
                modelname=self.Meta.model._meta.verbose_name,
                description="Клиент заполнил анкету",
                client=client,
                link=link,
            )

        super().save(*args, **kwargs)


class HealthFormPage0(ModelForm):
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
            "confirmation": CheckboxInput(
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


class HealthFormPage1(ModelForm):
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
            "palpitation": CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "dyspnea": CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "fainting": CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "chest_pain": CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "chest_pain": CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "ankles_swelling": CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "leg_cramps": CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "restriction_reasons": CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

    def save(self, *args, **kwargs):
        """Save the instance and create a Log entry about the changes."""

        if self.instance.is_filled:
            client = self.instance.client
            link = reverse("expert:client_health") + f"?client_id={client.id}"
            create_change_log_entry(form=self, client=client, link=link)

        super().save(*args, **kwargs)


class HealthFormPage2(ModelForm):
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
            "heart_attack": CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "cardiac_surgery": CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "pacemaker": CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "arrhythmia": CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "heart_defect": CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "diabetes": CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "kidney_disease": CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

    def save(self, *args, **kwargs):
        """Save the instance and create a Log entry about the changes."""

        if self.instance.is_filled:
            client = self.instance.client
            link = reverse("expert:client_health") + f"?client_id={client.id}"
            create_change_log_entry(form=self, client=client, link=link)

        super().save(*args, **kwargs)


class HealthFormPage3(ModelForm):
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
            "known_blood_pressure": CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "blood_pressure": TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "has_glucose_changes": CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "glucose_level": TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "has_urinary_diseases": CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "urinary_diseases": TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "has_respiratory_diseases": CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "respiratory_diseases": TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "has_digestive_diseases": CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "digestive_diseases": TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "has_oncological_diseases": CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "oncological_diseases": TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "has_vascular_diseases": CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "vascular_diseases": TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "has_trauma_or_surgeries": CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "trauma_or_surgeries": TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "has_osteoporosis_and_joint_problems": CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "osteoporosis_and_joint_problems": TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "has_other_diseases": CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "other_diseases": Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
            "use_medications": CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "medications": Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
            "follow_diet": CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "current_diet": TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "is_pregnant": CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "pregnancy_stage": TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "had_birth_in_last_six_months": CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "birth_complications": Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
        }

    def save(self, *args, **kwargs):
        """Save the instance and create a Log entry about the changes."""

        if self.instance.is_filled:
            client = self.instance.client
            link = reverse("expert:client_health") + f"?client_id={client.id}"
            create_change_log_entry(form=self, client=client, link=link)

        super().save(*args, **kwargs)


class HealthFormPage4(ModelForm):
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
            "daily_steps",
            "has_signs_of_underrecovery_or_overtraining",
            "signs_of_underrecovery_or_overtraining",
        )
        widgets = {
            "has_regular_training": CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "had_physical_activity": CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "previous_physical_activity": Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
            "current_physical_activity": RadioSelect(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "current_physical_activity_period": TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "daily_steps": TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "has_signs_of_underrecovery_or_overtraining": CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "signs_of_underrecovery_or_overtraining": Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
        }

    def save(self, *args, **kwargs):
        """Save the instance and create a Log entry about the changes."""

        if self.instance.is_filled:
            client = self.instance.client
            link = reverse("expert:client_health") + f"?client_id={client.id}"
            create_change_log_entry(form=self, client=client, link=link)

        super().save(*args, **kwargs)


class HealthFormPage5(ModelForm):
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
            "has_work_rest_schedule_issues": CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "work_rest_schedule_issues": Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
            "has_other_issues": CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "other_issues": Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
        }

    def save(self, *args, **kwargs):
        """Save the instance and create a Log entry about the changes."""

        client = self.instance.client
        link = reverse("expert:client_health") + f"?client_id={client.id}"

        if self.instance.is_filled:
            create_change_log_entry(form=self, client=client, link=link)
        else:
            self.instance.is_filled = True
            create_log_entry(
                modelname=self.Meta.model._meta.verbose_name,
                description="Клиент заполнил анкету",
                client=client,
                link=link,
            )

        super().save(*args, **kwargs)


class HealthFormResult(ModelForm):
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
            "client": HiddenInput(),
            "workout_readiness": Select(
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


class ContactsForm(ModelForm):
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
            "telegram": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://t.me/your_telegram_username",
                }
            ),
            "whatsapp": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://wa.me/your_whatsapp_number",
                }
            ),
            "discord": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "discord.gg/your_discord_server or username",
                }
            ),
            "skype": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://join.skype.com/my_code",
                }
            ),
            "vkontakte": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://vk.com/your_vk_username_or_id",
                }
            ),
            "facebook": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://www.facebook.com/your_facebook_username.id",
                }
            ),
            "preferred_contact": Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }

    def save(self, *args, **kwargs):
        """Save the instance and create a Log entry about the changes."""

        client = self.instance.client
        link = reverse("expert:client_contacts") + f"?client_id={client.id}"
        create_change_log_entry(form=self, client=client, link=link)

        super().save(*args, **kwargs)
