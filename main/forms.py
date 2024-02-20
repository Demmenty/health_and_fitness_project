from django.forms import ClearableFileInput


class CustomImageFileInput(ClearableFileInput):
    template_name = "widgets/custom_image_file_input.html"


class CustomFileInput(ClearableFileInput):
    template_name = "widgets/custom_file_input.html"
