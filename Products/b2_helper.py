import os
from io import BytesIO
from django.conf import settings
from django.http import HttpResponse, Http404
from .models import Product
from b2sdk.v2 import InMemoryAccountInfo, B2Api, DoNothingProgressListener

# Initialize B2 once
info = InMemoryAccountInfo()
b2_api = B2Api(info)
b2_api.authorize_account(
    "production",
    settings.B2_APPLICATION_KEY_ID,
    settings.B2_APPLICATION_KEY
)
bucket = b2_api.get_bucket_by_name(settings.B2_BUCKET_NAME)






def product_image(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise Http404("Product not found")

    CACHE_DIR = os.path.join(settings.MEDIA_ROOT, "cache")
    os.makedirs(CACHE_DIR, exist_ok=True)

    local_filename = os.path.join(CACHE_DIR, os.path.basename(product.image_path))

    # Serving from cache
    if os.path.exists(local_filename):
        with open(local_filename, "rb") as f:
            # print("✅Loading from cache...")      # DEBUGGING LINE
            content = f.read()
    else:
        try:
            # Downloading file from B2 bucket
            progress_listener = DoNothingProgressListener()
            downloaded_file = bucket.download_file_by_name(product.image_path, progress_listener)
            downloaded_file.save_to(local_filename)  # save full file to cache

            with open(local_filename, "rb") as f:
                content = f.read()
        except Exception as e:
            print("Error downloading from B2:", e)
            raise Http404("Image not found in B2 bucket")

    # Determine MIME type
    ext = os.path.splitext(product.image_path)[1].lower()
    if ext in [".jpg", ".jpeg"]:
        content_type = "image/jpeg"
    elif ext == ".png":
        content_type = "image/png"
    else:
        content_type = "application/octet-stream"

    return HttpResponse(content, content_type=content_type)