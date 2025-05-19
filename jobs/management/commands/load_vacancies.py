import os
import csv
from django.core.management.base import BaseCommand
from jobs.models import Vacancy


class Command(BaseCommand):
    help = "Загрузка вакансий из CSV файла"

    def add_arguments(self, parser):
        parser.add_argument(
            '--file', type=str, required=False,
            help='Путь к CSV файлу с вакансиями'
        )

    def handle(self, *args, **options):
        file_path = options.get('file')
        if not file_path:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_dir, 'vacancies.csv')

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                salary = row.get('salary') or None
                if salary:
                    salary = salary.replace(',', '').replace(' ', '')
                    try:
                        salary = float(salary)
                    except ValueError:
                        salary = None

                Vacancy.objects.update_or_create(
                    name=row['name'],
                    defaults={
                        'description': row['text'],
                        'salary': salary,
                    }
                )
        self.stdout.write(self.style.SUCCESS(f"Вакансии загружены из {file_path}"))
