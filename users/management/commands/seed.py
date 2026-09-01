from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
from django.apps import apps
import os


class Command(BaseCommand):
    help = 'Carga datos seed (usuarios, productos, posts, mensajes) desde el fixture JSON. Idempotente.'

    def handle(self, *args, **options):
        fixture_path = os.path.join(settings.BASE_DIR, '_fixture_seed.json')
        Product = apps.get_model('marketplace', 'Product')
        if Product.objects.exists():
            self.stdout.write(self.style.WARNING('Ya existen productos, se omite seed para evitar duplicados.'))
            return
        if not os.path.exists(fixture_path):
            self.stdout.write(self.style.WARNING('No se encontró _fixture_seed.json, se omite seed.'))
            return

        self.stdout.write(self.style.MIGRATE_HEADING('Cargando datos seed...'))
        try:
            call_command('loaddata', fixture_path, verbosity=0)
            self.stdout.write(self.style.SUCCESS('Datos seed cargados correctamente.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error cargando seed: {e}'))