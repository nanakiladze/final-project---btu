from django.core.management.base import BaseCommand
from faker import Faker
from books.models import Book, Author, Genre
import random


class Command(BaseCommand):
    help = 'Populate the database with random book data'

    def handle(self, *args, **options):
        fake = Faker()

        # Create authors
        authors = [Author.objects.create(first_name=fake.first_name(), last_name=fake.last_name()) for _ in range(50)]

        # Create genres
        genres = [Genre.objects.create(name=fake.word()) for _ in range(20)]

        # Create books
        for _ in range(1000):
            author = random.choice(authors)
            genre = random.choice(genres)
            title = fake.catch_phrase()
            publication_date = fake.date_between(start_date='-10y', end_date='today')
            stock_quantity = random.randint(1, 100)

            Book.objects.create(
                title=title,
                author=author,
                genre=genre,
                publication_date=publication_date,
                stock_quantity=stock_quantity
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with random book data'))
