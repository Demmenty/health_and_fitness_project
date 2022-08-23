# Generated by Django 4.0.6 on 2022-08-21 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personalpage', '0010_alter_questionary_parameter11_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionary',
            name='confirm',
            field=models.BooleanField(choices=[('1', 'да '), ('0', 'нет')], default='0', verbose_name='Подверждаю достоверность предоставленных сведений и даю согласие на обработку персональных данных'),
        ),
        migrations.AlterField(
            model_name='questionary',
            name='parameter13',
            field=models.BooleanField(choices=[('1', 'да '), ('0', 'нет')], default='0', verbose_name='Одышка при небольшой нагрузке или в покое'),
        ),
        migrations.AlterField(
            model_name='questionary',
            name='parameter14',
            field=models.BooleanField(choices=[('1', 'да '), ('0', 'нет')], default='0', verbose_name='Потемнения в глазах, головокружения, обмороки, потеря равновесия'),
        ),
        migrations.AlterField(
            model_name='questionary',
            name='parameter16',
            field=models.BooleanField(choices=[('1', 'да '), ('0', 'нет')], default='0', verbose_name='Чувство жжения, боль, судороги в нижних конечностях при ходьбе на малые дистанции'),
        ),
        migrations.AlterField(
            model_name='questionary',
            name='parameter17',
            field=models.BooleanField(choices=[('1', 'да '), ('0', 'нет')], default='0', verbose_name='Другие известные клиенту причины, по которым ему следует ограничить физическую активность'),
        ),
        migrations.AlterField(
            model_name='questionary',
            name='parameter20',
            field=models.BooleanField(choices=[('1', 'да '), ('0', 'нет')], default='0', verbose_name='В течение как минимум последних трех месяцев проводятся регулярные тренировки длительностью не менее 30 минут в день, интенсивностью не ниже умеренной, с частотой не менее трех раз в неделю'),
        ),
        migrations.AlterField(
            model_name='questionary',
            name='parameter31',
            field=models.BooleanField(choices=[('1', 'да '), ('0', 'нет')], default='0', verbose_name='Инфаркт миокарда'),
        ),
        migrations.AlterField(
            model_name='questionary',
            name='parameter32',
            field=models.BooleanField(choices=[('1', 'да '), ('0', 'нет')], default='0', verbose_name='Катетеризация сердца, коронарная ангиопластика, операции на сердце, трансплантация сердца'),
        ),
        migrations.AlterField(
            model_name='questionary',
            name='parameter33',
            field=models.BooleanField(choices=[('1', 'да '), ('0', 'нет')], default='0', verbose_name='Нарушения сердечного ритма, кардиостимулятор/имплантируемый сердечный дефибриллятор'),
        ),
        migrations.AlterField(
            model_name='questionary',
            name='parameter34',
            field=models.BooleanField(choices=[('1', 'да '), ('0', 'нет')], default='0', verbose_name='Врожденные пороки сердца, патологии сердечных клапанов, сердечная недостаточность'),
        ),
        migrations.AlterField(
            model_name='questionary',
            name='parameter35',
            field=models.BooleanField(choices=[('1', 'да '), ('0', 'нет')], default='0', verbose_name='Сахарный диабет'),
        ),
        migrations.AlterField(
            model_name='questionary',
            name='parameter36',
            field=models.BooleanField(choices=[('1', 'да '), ('0', 'нет')], default='0', verbose_name='Заболевания почек'),
        ),
    ]
