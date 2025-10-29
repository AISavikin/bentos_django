from django.db import models

# Create your models here.
from django.db import models

class Position(models.Model):
    # В Django обязательно указывать max_length для CharField
    full = models.CharField(max_length=255)
    short = models.CharField(max_length=255)

    def __str__(self):
        return self.full

    class Meta:
        # Django автоматически создаст имя таблицы в формате "appname_position"
        # При необходимости можно переопределить через db_table
        pass


class Department(models.Model):
    title = models.CharField(max_length=255)
    genitive = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Employee(models.Model):
    name = models.CharField(max_length=255)
    name_genitive = models.CharField(max_length=255)
    # В Django ForeignKey объявляется иначе:
    # 1. Указывается related_name для обратной связи (вместо backref)
    # 2. on_delete обязателен
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        related_name='employees'  # лучше использовать мн.число для related_name
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='employees'
    )
    objective = models.CharField(max_length=255)
    profession = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}, {self.objective}'

    @property
    def short_name(self):
        # Осторожно: если в имени не 3 части, будет ошибка
        parts = self.name.split()
        if len(parts) == 3:
            last_name, first_name, second_name = parts
            return f'{last_name} {first_name[0]}.{second_name[0]}.'
        return self.name  # fallback для неправильного формата

    class Meta:
        # При необходимости можно указать порядок сортировки
        # ordering = ['name']
        pass