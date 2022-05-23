import json

from django.core.management import BaseCommand

from mainapp.models import News


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open('mainapp/some_data.json', 'r') as file:
            news_list = json.load(file)
        for item in news_list:
            News.objects.create(
                title=item['title'],
                preambule=item['preambule'],
                body=item['body']
            )


