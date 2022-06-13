from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated = models.DateTimeField(auto_now_add=True, verbose_name='Обновлено')
    deleted = models.BooleanField(default=False, verbose_name='Удалено')

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()


class News(BaseModel):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    preambule = models.CharField(max_length=2255, verbose_name='Превью')
    body = models.TextField(verbose_name='Новость')
    body_as_markdown = models.BooleanField(default=False, verbose_name='Маркдаун')

    def __str__(self):
        return f'{self.title} {self.created}'

    class Meta:
        ordering = ['-created', 'title']
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class Courses(BaseModel):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    description_as_markdown = models.BooleanField(default=True, verbose_name='Маркдаун')
    cost = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена')
    cover = models.CharField(max_length=124, verbose_name='Изображение', default='No image')

    def __str__(self):
        return f'{self.name} {self.created}'

    class Meta:
        ordering = ['-cost', 'name']
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(BaseModel):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, blank=True, null=True)
    num = models.PositiveIntegerField(verbose_name='Номер урока')
    title = models.CharField(max_length=50, verbose_name='Название урока')
    description = models.CharField(max_length=255, verbose_name='Описание урока')
    description_as_markdown = models.BooleanField(default=False, verbose_name='Маркдаун')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        ordering = ['course', 'num']
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class CourseTeachers(models.Model):
    name_first = models.CharField(max_length=100, verbose_name='Имя')
    name_second = models.CharField(max_length=100, verbose_name='Фамилия')
    day_birth = models.DateField(verbose_name='День рождения')
    course = models.ManyToManyField(Courses)
    deleted = models.BooleanField(default=False, verbose_name='Удалено')

    def __str__(self):
        return f'{self.name_first} {self.name_second}'

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()

    class Meta:
        verbose_name = 'Препоаватель'
        verbose_name_plural = 'Преподаватели'


class CourseFeedback(BaseModel):
    RAITING_FIVE = 5
    RAITING_FOUR = 4
    RAITING_THREE = 3
    RAITING_TWO = 2
    RAITING_ONE = 1

    RATINGS = (
        (RAITING_FIVE, '⭐⭐⭐⭐⭐'),
        (RAITING_FOUR, '⭐⭐⭐⭐'),
        (RAITING_THREE, '⭐⭐⭐'),
        (RAITING_TWO, '⭐⭐'),
        (RAITING_ONE, '⭐'),
    )

    course = models.ForeignKey(Courses, on_delete=models.CASCADE, verbose_name='Курс')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Пользователь')
    feedback = models.TextField(verbose_name='Отзыв', default='Без отзыва')
    rating = models.PositiveSmallIntegerField(choices=RATINGS, default=RAITING_FIVE, verbose_name='Рейтинг')

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'

    def __str__(self):
        return f'Отзыв от {self.user} на курс {self.course}'


