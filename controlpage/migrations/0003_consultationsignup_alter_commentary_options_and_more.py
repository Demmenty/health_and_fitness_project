# Generated by Django 4.1 on 2022-12-03 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controlpage', '0002_commentary_general_read_commentary_measurements_read_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consultationsignup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True, verbose_name='Дата заполнения заявки')),
                ('name', models.CharField(help_text='Как к вам обращаться?', max_length=100, verbose_name='Имя')),
                ('age', models.CharField(blank=True, help_text='Сколько вам лет?', max_length=100, verbose_name='Возраст')),
                ('location', models.CharField(blank=True, help_text='Расскажите, откуда вы?', max_length=100, verbose_name='Место жительства')),
                ('email', models.EmailField(blank=True, help_text='Обещаем не использовать в коварных целях!', max_length=100, verbose_name='Почта')),
                ('contacts', models.CharField(help_text='Оставьте ссылку на предпочитаемый способ связи', max_length=255, verbose_name='Контакты')),
                ('is_read', models.BooleanField(default=False, verbose_name='Заявка прочитана')),
                ('expert_comment', models.TextField(blank=True, null=True, verbose_name='Комментарий')),
            ],
        ),
        migrations.AlterModelOptions(
            name='commentary',
            options={'ordering': ['-date']},
        ),
        migrations.AlterField(
            model_name='commentary',
            name='general_read',
            field=models.BooleanField(default=True, verbose_name='Общее - прочитано'),
        ),
        migrations.AlterField(
            model_name='commentary',
            name='measurements_read',
            field=models.BooleanField(default=True, verbose_name='Измерения - прочитано'),
        ),
        migrations.AlterField(
            model_name='commentary',
            name='nutrition_read',
            field=models.BooleanField(default=True, verbose_name='Питание - прочитано'),
        ),
        migrations.AlterField(
            model_name='commentary',
            name='workout_read',
            field=models.BooleanField(default=True, verbose_name='Тренировки - прочитано'),
        ),
    ]
