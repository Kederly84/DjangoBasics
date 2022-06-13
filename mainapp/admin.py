from functools import reduce
from operator import or_

from django.contrib import admin
from django.db.models import Q
from django.utils.html import format_html

from mainapp.models import News, Courses, Lesson, CourseTeachers


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'slug', 'preambule', 'created', 'updated', 'deleted')
    list_per_page = 10
    list_filter = ('created', 'updated', 'deleted')
    search_fields = ('title', 'preambule')
    date_hierarchy = 'created'
    show_full_result_count = False

    def slug(self, obj):
        return format_html(
            '<a href="http://127.0.0.1:8000/admin/mainapp/news/{}/change/">{}</a>',
            obj.pk,
            obj.title
        )

    slug.short_description = 'Заголовок'

    # def get_search_results(self, request, queryset, search_term):
    #     """Я очень сильно не уверен что это вообще работает"""
    #     queryset, may_have_duplicates = super().get_search_results(
    #         request, queryset, search_term,
    #     )
    #     queryset |= self.model.objects.filter(title__icontains=search_term)
    #     return queryset, may_have_duplicates

    def get_search_results(self, request, queryset, search_term):
        """Это работает, но все еще почему то регистрозависимая"""
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        q_objects = [
            Q(**{field + '__icontains': search_term})
            for field in self.search_fields
        ]
        queryset = queryset.filter(reduce(or_, q_objects))
        return queryset, use_distinct


@admin.register(Courses)
class CoursesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'slug', 'created', 'updated', 'deleted', 'cost')
    list_per_page = 10
    list_filter = ('created', 'updated', 'deleted')
    search_fields = ('name', 'description')
    show_full_result_count = False

    def slug(self, obj):
        return format_html(
            '<a href="http://127.0.0.1:8000/admin/mainapp/courses/{}/change/">{}</a>',
            obj.pk,
            obj.name
        )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'num', 'created', 'updated', 'deleted')
    list_per_page = 10
    list_filter = ('created', 'updated', 'deleted')
    search_fields = ('title', 'description')
    show_full_result_count = False


@admin.register(CourseTeachers)
class CourseTeachersAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'day_birth', 'deleted')
    list_per_page = 10
    list_filter = ('name_first', 'name_second')
    search_fields = ('name_first', 'name_second')
    show_full_result_count = False
