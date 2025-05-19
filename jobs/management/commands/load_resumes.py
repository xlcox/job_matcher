import os
import csv
from django.core.management.base import BaseCommand
from jobs.models import Resume


class Command(BaseCommand):
    help = "Загрузка резюме из CSV файла"

    def add_arguments(self, parser):
        parser.add_argument(
            '--file', type=str, required=False,
            help='Путь к CSV файлу с резюме'
        )

    def handle(self, *args, **options):
        file_path = options.get('file')
        if not file_path:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_dir, 'resumes.csv')

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                salary = row.get('Желаемая зарплата') or None
                if salary:
                    salary = salary.replace(',', '').replace(' ', '')
                    try:
                        salary = float(salary)
                    except ValueError:
                        salary = None

                Resume.objects.update_or_create(
                    full_name=row['ФИО'],
                    defaults={
                        'phone_number': row['Телефон'],
                        'mail': row['Email'],
                        'salary': salary,
                        'text': row['Текст резюме'],
                    }
                )
        self.stdout.write(self.style.SUCCESS(f"Резюме загружены из {file_path}"))
