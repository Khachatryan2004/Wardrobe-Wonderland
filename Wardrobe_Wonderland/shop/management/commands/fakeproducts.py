from django.core.management.base import BaseCommand
from faker import Faker
from shop.models import Category, Item

fake = Faker()

class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker()
        default_image_path = 'item_img/cloth_3.jpg'  # Adjust this to your actual default image path
        for _ in range(30):
            product_name = fake.company()
            product_description = fake.paragraph(nb_sentences=2)
            product_price = fake.pydecimal(
                left_digits=3, right_digits=2, min_value=1, max_value=999.99)
            product = Item(
                category=Category.objects.first(),
                name=product_name,
                description=product_description,
                slug=fake.slug(),
                price=product_price,
                status=True,
                created_at=fake.date_time(),
                updated_at=fake.date_time(),
                discount=fake.pyint(min_value=0, max_value=20),
                image=default_image_path  # Assign the default image path
            )
            product.save()
        self.stdout.write(f'Products in DB: {Item.objects.count()}')

