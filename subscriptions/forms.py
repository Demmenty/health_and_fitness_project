from django.forms import DateInput, ModelForm, NumberInput, Select, Textarea, TextInput

from subscriptions.models import Plan, Subscription


class PlanForm(ModelForm):
    """Form for subscription plan"""

    class Meta:
        model = Plan
        fields = ("name", "access", "default_price", "description")
        widgets = {
            "name": TextInput(attrs={"class": "form-control"}),
            "access": Select(
                attrs={"class": "form-control"}, choices=Plan.Access.choices
            ),
            "default_price": NumberInput(attrs={"class": "form-control"}),
            "description": Textarea(
                attrs={"rows": 11, "cols": 10, "class": "form-control"}
            ),
        }


class SubscriptionForm(ModelForm):
    """Form for subscription details for specific client"""

    class Meta:
        model = Subscription
        fields = ("plan", "price", "start_date", "end_date", "comment")
        widgets = {
            "plan": Select(
                attrs={
                    "class": "form-control",
                },
            ),
            "price": NumberInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "start_date": DateInput(
                format="%Y-%m-%d",
                attrs={
                    "class": "form-control",
                    "type": "date",
                },
            ),
            "end_date": DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "comment": Textarea(attrs={"rows": 6, "class": "form-control"}),
        }
