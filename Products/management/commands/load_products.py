import csv
from django.core.management.base import BaseCommand
from Products.models import Product, Brand, Category
from django.core.files.images import get_image_dimensions
from django.db.utils import IntegrityError
from django.utils.text import slugify



class Command(BaseCommand):
    help = "Loads products into the database from CSV."

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="Path to the CSV file")

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        self.stdout.write(self.style.WARNING(f"Loading products from {csv_file}..."))

        with open(csv_file, newline="", encoding='utf-8') as f:
            reader = csv.DictReader(f)
            field_names = [field.name for field in Product._meta.fields]

            for row in reader:
                defaults = {}
                for field in field_names:
                    if field in ["slug", "id", "created_on", "updated_on"]:
                        # Will be created along with the Product
                        continue

                    if field == "brand":
                        brand_name = row["brand"].strip()
                        brand, _ = Brand.objects.get_or_create(name=brand_name)
                        defaults["brand"] = brand
                    elif field == "category":
                        category_name = row["category"].strip()
                        slug = slugify(category_name)
                        category, _ = Category.objects.get_or_create(slug=slug, defaults={"name": category_name})
                        defaults["category"] = category
                    elif field == "image_path":
                        # Take from CSV, fallback to default
                        defaults["image_path"] = row.get("image_path", "product_images/default.jpg").strip()
                    else:
                        defaults[field] = row.get(field, "").strip()

                product, created = Product.objects.update_or_create(slug=row["slug"], defaults=defaults)
                if created:
                    self.stdout.write(self.style.SUCCESS(f"✅ Added {product.title}"))
                else:
                    self.stdout.write(self.style.NOTICE(f"🔄 Updated {product.title}"))

        self.stdout.write(self.style.SUCCESS("🎉 Done loading all products!"))
