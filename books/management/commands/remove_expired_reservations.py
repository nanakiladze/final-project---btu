from django.core.management.base import BaseCommand
from django.utils import timezone
from books.models import BookCheckout, Book


class Command(BaseCommand):
    help = 'Removes expired book reservations'

    def handle(self, *args, **options):
        # Get all book checkouts where the return_date is null (not returned yet)
        unreturned_checkouts = BookCheckout.objects.filter(is_taken=False)

        # Loop through each unreturned checkout
        for checkout in unreturned_checkouts:
            # Checked if the checkout date is more than 1 day ago
            if checkout.checkout_date < timezone.now() - timezone.timedelta(hours=24):
                checkout.is_late = True
                self.stdout.write(
                    self.style.SUCCESS(f'Removed reservation for {checkout.book.title} by {checkout.user.username}'))
