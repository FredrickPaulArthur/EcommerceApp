from django.core.management.base import BaseCommand



class Command(BaseCommand):
    help = "Just saying Welcome to the E-Commerce App users."

    def handle(self, *args, **kwargs):
        self.stdout.write("Welcome to Django Commands.")