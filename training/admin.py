from django.contrib import admin

from training.models import Area, Exercise, ExerciseRecord, Tool, Training


class ExerciseRecordInline(admin.TabularInline):
    model = ExerciseRecord


class TrainingAdmin(admin.ModelAdmin):
    inlines = [ExerciseRecordInline]


admin.site.register(Exercise)
admin.site.register(Tool)
admin.site.register(Training, TrainingAdmin)
admin.site.register(ExerciseRecord)
admin.site.register(Area)
