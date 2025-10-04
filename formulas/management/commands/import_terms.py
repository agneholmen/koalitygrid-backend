from django.core.management.base import BaseCommand
import csv
from formulas.models import Term

class Command(BaseCommand):
    help = 'Import terms from a CSV file into the Term model'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        file_path = options['path']
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                if len(row) == 2:
                    Term.objects.get_or_create(
                        name=row[0],
                        defaults={'description': row[1]}
                    )
        self.stdout.write(self.style.SUCCESS('Successfully imported terms from CSV'))