from django.core.management.base import BaseCommand
from web.models import BookModel


class Command(BaseCommand):
    help = 'Populate database with sample books'

    def handle(self, *args, **kwargs):
        # Check if books already exist
        if BookModel.objects.exists():
            self.stdout.write(self.style.WARNING('Books already exist. Skipping...'))
            return

        books_data = [
            {
                'title': 'Python Crash Course',
                'author': 'Eric Matthes',
                'price': 39.99,
                'stock': 50
            },
            {
                'title': 'Clean Code',
                'author': 'Robert C. Martin',
                'price': 45.50,
                'stock': 30
            },
            {
                'title': 'The Pragmatic Programmer',
                'author': 'Andrew Hunt, David Thomas',
                'price': 42.00,
                'stock': 25
            },
            {
                'title': 'Design Patterns',
                'author': 'Gang of Four',
                'price': 54.99,
                'stock': 20
            },
            {
                'title': 'Introduction to Algorithms',
                'author': 'Thomas H. Cormen',
                'price': 89.99,
                'stock': 15
            },
            {
                'title': 'JavaScript: The Good Parts',
                'author': 'Douglas Crockford',
                'price': 29.99,
                'stock': 40
            },
            {
                'title': 'You Don\'t Know JS',
                'author': 'Kyle Simpson',
                'price': 35.00,
                'stock': 35
            },
            {
                'title': 'Eloquent JavaScript',
                'author': 'Marijn Haverbeke',
                'price': 32.50,
                'stock': 45
            },
            {
                'title': 'The Mythical Man-Month',
                'author': 'Frederick Brooks',
                'price': 37.99,
                'stock': 22
            },
            {
                'title': 'Code Complete',
                'author': 'Steve McConnell',
                'price': 49.99,
                'stock': 28
            },
            {
                'title': 'Refactoring',
                'author': 'Martin Fowler',
                'price': 44.99,
                'stock': 33
            },
            {
                'title': 'Head First Design Patterns',
                'author': 'Eric Freeman, Elisabeth Robson',
                'price': 41.50,
                'stock': 38
            }
        ]

        for book_data in books_data:
            BookModel.objects.create(**book_data)
            self.stdout.write(self.style.SUCCESS(f'Created book: {book_data["title"]}'))

        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully created {len(books_data)} books!'))
