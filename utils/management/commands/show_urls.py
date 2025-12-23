from django.core.management.base import BaseCommand
from django.urls import get_resolver

class Command(BaseCommand):
    help = "Muestra todas las URLs cargadas por Django"

    def handle(self, *args, **kwargs):
        resolver = get_resolver()
        for pattern in resolver.url_patterns:
            self.print_pattern(pattern)

    def print_pattern(self, pattern, prefix=""):
        if hasattr(pattern, "url_patterns"):
            for p in pattern.url_patterns:
                self.print_pattern(p, prefix + str(pattern.pattern))
        else:
            print(prefix + str(pattern.pattern))
