from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Comment, Cart, CartItem, Contact


admin.site.register((Category, Cart, CartItem))

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title","price","image_tag"]
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ["title"]
    readonly_fields = ['image_tag','rating'] #change
    def image_tag(self, obj):
        return format_html('<img width="100" height="100" src="{}" />'.format(obj.image.url))

    image_tag.short_description = 'Image'

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["first_name", "email"]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["full_name", "rating","product"]
    
