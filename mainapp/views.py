from django.views.generic import TemplateView
import json


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


class CoursesView(TemplateView):
    template_name = 'mainapp/courses_list.html'


class DocSiteView(TemplateView):
    template_name = 'mainapp/doc_site.html'


class IndexView(TemplateView):
    template_name = 'mainapp/index.html'


class LoginView(TemplateView):
    template_name = 'mainapp/login.html'


class NewsView(TemplateView):
    template_name = 'mainapp/news.html'


    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        with open('mainapp/some_data.json', 'r') as read_file:
            data = json.load(read_file)
        arr = []
        for key in data:
            arr.append(data[key])
        context_data['object_list'] = arr

        # context_data['object_list'] = [
        #     {
        #         'title': 'Новость',
        #         'preview': 'Превью к новости',
        #         'date': datetime.now()
        #     }, {
        #         'title': 'Новость',
        #         'preview': 'Превью к новости',
        #         'date': datetime.now()
        #     }, {
        #         'title': 'Новость',
        #         'preview': 'Превью к новости',
        #         'date': datetime.now()
        #     }, {
        #         'title': 'Новость',
        #         'preview': 'Превью к новости',
        #         'date': datetime.now()
        #     }, {
        #         'title': 'Новость',
        #         'preview': 'Превью к новости',
        #         'date': datetime.now()
        #     }
        # ]
        return context_data


class NewsWithPagination(NewsView):

    def get_context_data(self, page, **kwargs):
        context = super().get_context_data(page=page, **kwargs)
        context["page_num"] = page
        return context