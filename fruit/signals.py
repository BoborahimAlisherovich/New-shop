from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment

@receiver(post_save,sender=Comment)
def update_product_rating(sender, instance, created, **kwargs):
    if created:
        product = instance.product
        comments_count = Comment.objects.filter(product=product).count()
        total_rating = sum(comment.rating for comment in Comment.objects.filter(product=product))
        product.rating = total_rating / comments_count
        product.save()
