from django.core.management.base import BaseCommand
from books.models import Book

class Command(BaseCommand):
    help = 'Populate the database with sample books'

    def handle(self, *args, **kwargs):
        books_data = [
            {
                'title': 'Clean Code',
                'author': 'Robert C. Martin',
                'price': 39.99,
                'stock': 15
            },
            {
                'title': 'The Pragmatic Programmer',
                'author': 'Andrew Hunt',
                'price': 44.99,
                'stock': 10
            },
            {
                'title': 'Design Patterns',
                'author': 'Gang of Four',
                'price': 54.99,
                'stock': 8
            },
            {
                'title': 'Introduction to Algorithms',
                'author': 'Thomas H. Cormen',
                'price': 89.99,
                'stock': 5
            },
            {
                'title': 'The Clean Coder',
                'author': 'Robert C. Martin',
                'price': 34.99,
                'stock': 12
            },
            {
                'title': 'Refactoring',
                'author': 'Martin Fowler',
                'price': 49.99,
                'stock': 7
            },
            {
                'title': 'Head First Design Patterns',
                'author': 'Eric Freeman',
                'price': 44.99,
                'stock': 20
            },
            {
                'title': 'Code Complete',
                'author': 'Steve McConnell',
                'price': 59.99,
                'stock': 6
            },
            {
                'title': 'The Mythical Man-Month',
                'author': 'Frederick P. Brooks Jr.',
                'price': 29.99,
                'stock': 15
            },
            {
                'title': 'Working Effectively with Legacy Code',
                'author': 'Michael Feathers',
                'price': 49.99,
                'stock': 9
            },
            {
                'title': 'Domain-Driven Design',
                'author': 'Eric Evans',
                'price': 64.99,
                'stock': 4
            },
            {
                'title': 'Patterns of Enterprise Application Architecture',
                'author': 'Martin Fowler',
                'price': 54.99,
                'stock': 11
            },
        ]

        created_count = 0
        updated_count = 0

        for book_data in books_data:
            book, created = Book.objects.update_or_create(
                title=book_data['title'],
                author=book_data['author'],
                defaults={
                    'price': book_data['price'],
                    'stock': book_data['stock']
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created: {book.title}')
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'⟳ Updated: {book.title}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Successfully populated database!\n'
                f'Created: {created_count} books\n'
                f'Updated: {updated_count} books\n'
                f'Total: {Book.objects.count()} books in database'
            )
        )
