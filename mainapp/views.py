from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse, FileResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.core.cache import cache
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _

from mainapp import tasks
from mainapp import tasks as mainapp_tasks
from django.contrib import messages
from django.http.response import HttpResponseRedirect

from mainapp.forms import CourseFeedbackForm
from mainapp.models import News, Courses, Lesson, CourseTeachers, CourseFeedback

import logging


logger = logging.getLogger(__name__)


class ContactsView(TemplateView):
    template_name = 'mainapp/contacts.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['contacts'] = [
            {
                'map': 'https://yandex.ru/map-widget/v1/-/CCUAZHcrhA',
                'city': 'Санкт‑Петербург',
                'phone': '+7-999-11-11111',
                'email': 'geeklab@spb.ru',
                'adress': 'территория Петропавловская крепость, 3Ж'
            }, {
                'map': 'https://yandex.ru/map-widget/v1/-/CCUAZHX3xB',
                'city': 'Казань',
                'phone': '+7-999-22-22222',
                'email': 'geeklab@kz.ru',
                'adress': 'территория Кремль, 11, Казань, Республика Татарстан, Россия'
            }, {
                'map': 'https://yandex.ru/map-widget/v1/-/CCUAZHh9kD',
                'city': 'Москва',
                'phone': '+7-999-33-33333',
                'email': 'geeklab@msk.ru',
                'adress': 'Красная площадь, 7, Москва, Россия'
            }
        ]
        return context_data

    def post(self, *args, **kwargs):
        message_body = self.request.POST.get('message_body')
        message_from = self.request.user.pk if self.request.user.is_authenticated else None
        tasks.send_feedback_mail.delay(message_body, message_from)
        return HttpResponseRedirect(reverse_lazy("mainapp:contacts"))


class CoursesView(TemplateView):
    template_name = 'mainapp/courses_list.html'


class DocSiteView(TemplateView):
    template_name = 'mainapp/doc_site.html'


class IndexView(TemplateView):
    template_name = 'mainapp/index.html'


# class NewsView(TemplateView):
#     template_name = 'mainapp/news.html'
#
#     def get_context_data(self, **kwargs):
#         context_data = super().get_context_data(**kwargs)
#         context_data['object_list'] = News.objects.filter(deleted=False)
#         return context_data
#
#
# class NewsWithPagination(NewsView):
#
#     def get_context_data(self, page, **kwargs):
#         context = super().get_context_data(page=page, **kwargs)
#         context["page_num"] = page
#         return context

class NewsView(ListView):
    model = News
    paginate_by = 5

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class NewsDetailView(DetailView):
    model = News

    def get_object(self, queryset=None):
        return get_object_or_404(News, pk=self.kwargs.get('pk'), deleted=False)


class NewsCreateView(PermissionRequiredMixin, CreateView):
    model = News
    fields = '__all__'
    success_url = reverse_lazy('mainapp:news')
    permission_required = ('mainapp.add_news',)


class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    model = News
    fields = '__all__'
    success_url = reverse_lazy('mainapp:news')
    permission_required = ('mainapp.change_news',)


class NewsDeleteView(PermissionRequiredMixin, DeleteView):
    model = News
    success_url = reverse_lazy('mainapp:news')
    permission_required = ('mainapp.delete_news',)


class CourseDetailView(TemplateView):
    template_name = "mainapp/courses_detail.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['course_object'] = get_object_or_404(Courses, pk=self.kwargs.get('pk'))
        context_data['lessons'] = Lesson.objects.filter(course=context_data['course_object'])
        context_data['teachers'] = CourseTeachers.objects.filter(course=context_data['course_object'])
        feedback_list_key = f"course_feedback{context_data['course_object'].pk}"
        cached_feedback_list = cache.get(feedback_list_key)
        if cached_feedback_list is None:
            context_data['feedback_list'] = CourseFeedback.objects.filter(course=context_data['course_object'])
            cache.set(feedback_list_key, context_data['feedback_list'], timeout=600)
        else:
            context_data['feedback_list'] = cached_feedback_list

        if not self.request.user.is_anonymous:
            if not CourseFeedback.objects.filter(
                    course=context_data["course_object"],
                    user=self.request.user).count():
                context_data['feedback_form'] = CourseFeedbackForm(
                    course=context_data['course_object'],
                    user=self.request.user
                )
        return context_data


class CoursesListView(TemplateView):
    template_name = "mainapp/courses_list.html"

    def get_context_data(self, **kwargs):
        context = super(CoursesListView, self).get_context_data(**kwargs)
        context["objects"] = Courses.objects.all()
        return context


class CourseFeedbackFormView(CreateView):
    model = CourseFeedback
    form_class = CourseFeedbackForm

    def form_valid(self, form):
        self.object = form.save()
        rendered_card = render_to_string('mainapp/includes/feedback_card.html', context={'item': self.object})
        return JsonResponse({'card': rendered_card})


class LogView(TemplateView):
    template_name = "mainapp/log_view.html"

    def get_context_data(self, **kwargs):
        """Переписал как и требовалось в 2b(**).
        Вывод только последнего кол-ва заданных строк указанных в lines_count"""
        context = super(LogView, self).get_context_data(**kwargs)
        log_slice = []
        lines_count = 10
        last_line = sum(1 for line in open(settings.LOG_FILE))
        with open(settings.LOG_FILE, "r") as log_file:
            for i, line in enumerate(log_file):
                if i < (last_line - lines_count):
                    continue
                log_slice.insert(0, f'{i} {line}')
            context["log"] = "".join(log_slice)
        return context


class LogDownloadView(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, *args, **kwargs):
        return FileResponse(open(settings.LOG_FILE, "rb"))



