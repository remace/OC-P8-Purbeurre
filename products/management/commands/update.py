import requests
from django.core.management.base import BaseCommand
from products.models import Product, Category


class Command(BaseCommand):
    ''' populates the database with x products from y categories'''

    help = ("populates the database with products and categories from Open Food Facts API\n "
            "syntax: ./manage.py populate products categories \n")


    def add_arguments(self, parser):
        pass

    def handle(self, *args, **kwargs):
        pass