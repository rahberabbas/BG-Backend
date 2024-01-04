from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe

from ckeditor.widgets import CKEditorWidget

class CustomCKEditorWidget(CKEditorWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize CKEditor settings
        self.config['filebrowserImageBrowseUrl'] = '/admin/image_gallery/imagegallery/'
        self.config['filebrowserImageUploadUrl'] = '/admin/image_gallery/imagegallery/add/'

# admin.site.register(BG_Remove)
# admin.site.register(BG_Add_Remove)
# admin.site.register(BG_Add_color)

admin.site.register(Contact)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'display_image')
    search_fields = ['title', 'slug']
    def display_image(self, obj):
        return mark_safe(f'<img src="{obj.image.image.url}" width="100" />')
    display_image.short_description = 'Image'

    readonly_fields = ('view_image',)

    def view_image(self, obj):
        return mark_safe(f'<img src="{obj.image.image.url}" width="200" />')

    view_image.short_description = 'Image Preview'
    
admin.site.register(Category, CategoryAdmin)

class ImageGalleryAdmin(admin.ModelAdmin):
    list_display = ('display_image', 'title', 'alt_text')
    search_fields = ['title']
    def display_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="100" />')

    display_image.short_description = 'Image'

    readonly_fields = ('view_image',)

    def view_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="200" />')

    view_image.short_description = 'Image Preview'

admin.site.register(ImageGallery, ImageGalleryAdmin)

from django.utils.html import format_html

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'display_image_gallery', 'date')
    search_fields = ['title', 'slug']
    date_hierarchy = 'date'
    def display_image_gallery(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.image.url}" width="100"/>')
        return 'No Image Gallery'

    display_image_gallery.short_description = 'Image Gallery'

    raw_id_fields = ('image',)
    
    def image_preview(self, obj):
        # Assuming ImageGallery has an 'image' field of type ImageField
        return format_html('<img src="{}" width="200" height="200" />', obj.image.image.url)

    image_preview.short_description = 'Image Preview'
    
    
    
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['image_preview'] = self.get_image_preview(object_id)
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def get_image_preview(self, object_id):
        blog = Blog.objects.get(pk=object_id)
        if blog.image:
            return mark_safe(f'<img src="{blog.image.image.url}" width="200" />')
        return 'No Image Gallery'
    
    readonly_fields = ('view_image',)
    
    def view_image(self, obj):
        # if obj.image:
        #     print("Object", obj.image)
        print(obj.image.image.url)
        return mark_safe(f'<img src="{obj.image.image.url}" width="200" />')
        # return 'No Image Gallery'

    view_image.short_description = 'Image Preview'

    # readonly_fields = ('image',)

admin.site.register(Blog, BlogAdmin)
admin.site.register(BG_Remove)
admin.site.register(BG_Add_Remove)
admin.site.register(BG_Add_color)