from django.db import models
from PIL import Image
from rembg import remove, new_session
import os
from io import BytesIO
from django.core.files.base import ContentFile
import numpy as np
import requests
import uuid
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from bs4 import BeautifulSoup
import uuid
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import InMemoryUploadedFile


# Specify the parameters
discard_threshold = 1e-05
shift = 1e-06

# Create a configuration dictionary
config = {
    "discard_threshold": discard_threshold,
    "shift": shift
}

# Create your models here.
class BG_Remove(models.Model):
    image = models.ImageField(blank=True, upload_to='images')
    bg_image = models.ImageField(blank=True, upload_to='bg_images/')
    webp_image_url = models.URLField(blank=True, null=True)
    webp_bg_image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return str(self.id)
    
    def save(self, *args, **kwargs):
        pil_image = Image.open(self.image)
        width, height = pil_image.size
        TARGET_WIDTH = 2000
        coefficient = width / 2000
        new_height = height / coefficient
        pil_image = pil_image.resize((int(TARGET_WIDTH),int(new_height)),Image.ANTIALIAS)
        session = new_session("isnet-general-use")
        rmbg = remove(pil_image, alpha_matting=10, session=session, config=config)
        img = np.array(rmbg)
        buffer = BytesIO()
        output_img = Image.fromarray(img)
        output_img = output_img.resize(size=(width, height))
        output_img.save(buffer, format="png")
        val = buffer.getvalue()
        filename = os.path.basename(self.image.name)
        name, _ = filename.split(".")
        self.bg_image.save(f"bgrm_{name}.png", ContentFile(val), save=False)
        super().save(*args, **kwargs)
        if self.image and not self.webp_image_url:
            webp_image = self.convert_to_webp(self.image)
            self.webp_image_url = self.save_webp_image(webp_image)
            super().save(update_fields=['webp_image_url'])
        if self.bg_image and  not self.webp_bg_image_url:
            print("Im here", self.bg_image)
            webp_image = self.convert_to_bg_webp(self.bg_image)
            self.webp_bg_image_url = self.save_webp_bg_image(webp_image)
            super().save(update_fields=['webp_bg_image_url'])
        
    def convert_to_webp(self, image):
        img = Image.open(image)
        webp_image = BytesIO()
        img.save(webp_image, 'WEBP')
        return webp_image

    def save_webp_image(self, webp_image):
        webp_file = InMemoryUploadedFile(
            webp_image,  # file
            None,  # field_name
            f'{self.image.name.split(".")[0]}{uuid.uuid4()}_webp.webp',  # file name
            'image/webp',  # content_type
            webp_image.tell(),  # size
            None  # content_type_extra
        )

        # Save the webp_file to the storage backend
        webp_path = default_storage.save(webp_file.name, webp_file)

        # Set the webp_image_url to the URL of the saved webp_file
        self.webp_image_url = default_storage.url(webp_path)
        return self.webp_image_url
    
    def convert_to_bg_webp(self, image):
        img = Image.open(image)
        webp_image = BytesIO()
        img.save(webp_image, 'WEBP')
        return webp_image

    def save_webp_bg_image(self, webp_image):
        webp_file = InMemoryUploadedFile(
            webp_image,  # file
            None,  # field_name
            f'{self.image.name.split(".")[0]}_bg_webp.webp',  # file name
            'image/webp',  # content_type
            webp_image.tell(),  # size
            None  # content_type_extra
        )

        # Save the webp_file to the storage backend
        webp_path = default_storage.save(webp_file.name, webp_file)

        # Set the webp_image_url to the URL of the saved webp_file
        self.webp_image_url = default_storage.url(webp_path)
        return self.webp_image_url


class BG_Add_Remove(models.Model):
    image = models.URLField(null=True, blank=True)
    bgimage = models.URLField(null=True, blank=True)
    back_image = models.ImageField(blank=True, upload_to='background_images')
    bg_image = models.ImageField(blank=True, upload_to='bg_images/')
    webp_bg_image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return str(self.id)
    
    def save(self, *args, **kwargs):
        # pil_image = Image.open(self.image)
        # width, height = pil_image.size
        # TARGET_WIDTH = 2000
        # coefficient = width / 2000
        # new_height = height / coefficient
        # pil_image = pil_image.resize((int(TARGET_WIDTH),int(new_height)),Image.ANTIALIAS)
        # session = new_session("isnet-general-use")
        # rmbg = remove(pil_image, alpha_matting=10, session=session)
        response = requests.get(self.image)
        rmbg = Image.open(BytesIO(response.content))
        print("Bg Resp,", rmbg)
        
        try:
            bgresponse = requests.get(self.bgimage)
            background = Image.open(BytesIO(bgresponse.content))
            background = background.resize(rmbg.size)
            background.paste(rmbg, mask=rmbg.split()[3])
            img = np.array(background)
            buffer = BytesIO()
            output_img = Image.fromarray(img)
            output_img.save(buffer, format="png")
            val = buffer.getvalue()
            filename = os.path.basename("Newimage.png")
            name, _ = filename.split(".")
            self.bg_image.save(f"bgrm_{name}.png", ContentFile(val), save=False)
            super().save(*args, **kwargs)       
            # if not self.webp_bg_image_url:
            #     print("Im here", self.bg_image)
            #     webp_image = self.convert_to_webp(self.bg_image)
            #     self.webp_bg_image_url = self.save_webp_image(webp_image)
            #     super().save(update_fields=['webp_bg_image_url']) 
            
        except:
            background = Image.open(self.back_image)
            background = background.resize(rmbg.size)
            background.paste(rmbg, mask=rmbg.split()[3])
            img = np.array(background)
            buffer = BytesIO()
            output_img = Image.fromarray(img)
            output_img.save(buffer, format="png")
            val = buffer.getvalue()
            filename = os.path.basename("Newimage.png")
            name, _ = filename.split(".")
            self.bg_image.save(f"bgrm_{name}.png", ContentFile(val), save=False)
            super().save(*args, **kwargs)   
        
        if self.bg_image and  not self.webp_bg_image_url:
            print("Im here", self.bg_image)
            webp_image = self.convert_to_webp(self.bg_image)
            self.webp_bg_image_url = self.save_webp_image(webp_image)
            super().save(update_fields=['webp_bg_image_url'])
        
    def convert_to_webp(self, image):
        img = Image.open(image)
        webp_image = BytesIO()
        img.save(webp_image, 'WEBP')
        return webp_image

    def save_webp_image(self, webp_image):
        webp_file = InMemoryUploadedFile(
            webp_image,  # file
            None,  # field_name
            f'{uuid.uuid4()}_webp.webp',  # file name
            'image/webp',  # content_type
            webp_image.tell(),  # size
            None  # content_type_extra
        )

        # Save the webp_file to the storage backend
        webp_path = default_storage.save(webp_file.name, webp_file)

        # Set the webp_image_url to the URL of the saved webp_file
        self.webp_image_url = default_storage.url(webp_path)
        return self.webp_image_url     
        

class BG_Add_color(models.Model):
    image = models.URLField(null=True, blank=True)
    hex_color = models.CharField(max_length=256, null=True, blank=True)
    bg_image = models.ImageField(blank=True, upload_to='bg_images/')
    webp_bg_image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return str(self.id)
    
    def save(self, *args, **kwargs):
        # pil_image = Image.open(self.image)
        # width, height = pil_image.size
        # TARGET_WIDTH = 2000
        # coefficient = width / 2000
        # new_height = height / coefficient
        # pil_image = pil_image.resize((int(TARGET_WIDTH),int(new_height)),Image.ANTIALIAS)
        # session = new_session("isnet-general-use")
        # rmbg = remove(pil_image, alpha_matting=10, session=session)
        response = requests.get(self.image)
        rmbg = Image.open(BytesIO(response.content))
        bg_color = self.hex_color# Red color
        bg_image = Image.new('RGBA', rmbg.size, bg_color)
        background = Image.alpha_composite(bg_image, rmbg)
        img = np.array(background)
        buffer = BytesIO()
        output_img = Image.fromarray(img)
        output_img.save(buffer, format="png")
        val = buffer.getvalue()
        filename = os.path.basename("Newimage.png")
        name, _ = filename.split(".")
        self.bg_image.save(f"bgrm_{name}.png", ContentFile(val), save=False)
        super().save(*args, **kwargs)
        if self.bg_image and not self.webp_bg_image_url:
            print("Im here", self.bg_image)
            webp_image = self.convert_to_webp(self.bg_image)
            self.webp_bg_image_url = self.save_webp_image(webp_image)
            super().save(update_fields=['webp_bg_image_url'])
        
    def convert_to_webp(self, image):
        img = Image.open(image)
        webp_image = BytesIO()
        img.save(webp_image, 'WEBP')
        return webp_image

    def save_webp_image(self, webp_image):
        webp_file = InMemoryUploadedFile(
            webp_image,  # file
            None,  # field_name
            f'{uuid.uuid4()}_webp.webp',  # file name
            'image/webp',  # content_type
            webp_image.tell(),  # size
            None  # content_type_extra
        )

        # Save the webp_file to the storage backend
        webp_path = default_storage.save(webp_file.name, webp_file)

        # Set the webp_image_url to the URL of the saved webp_file
        self.webp_image_url = default_storage.url(webp_path)
        return self.webp_image_url 
    
class ImageGallery(models.Model):
    title = models.CharField(max_length=256, null=True, blank=True)
    image = models.ImageField(blank=True, upload_to='blogs/')
    alt_text = models.CharField(max_length=256, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.title    
        
class Category(models.Model):
    title = models.CharField(max_length=256, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    meta_title = models.CharField(max_length=256, null=True, blank=True)
    meta_description = models.CharField(max_length=256, null=True, blank=True)
    image = models.ForeignKey(ImageGallery, on_delete=models.CASCADE, limit_choices_to={'image__isnull': False})
    
    def save(self, *args, **kwargs):
        
        if not self.slug:
            self.slug = slugify(self.title)

        # Replace spaces with hyphens in the slug
        self.slug = self.slug.replace(' ', '-')

        # Check if the slug is unique, if not, append a counter
        counter = 1
        original_slug = self.slug
        while Category.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            self.slug = f"{original_slug}-{counter}"
            counter += 1
        
        # If a custom slug is not provided, generate one from the title
        # if not self.slug:
        #     base_slug = slugify(self.title)
        #     self.slug = base_slug

        #     # Check if a blog with the same slug already exists
        #     counter = 1
        #     while Category.objects.filter(slug=self.slug).exists():
        #         print("Exists")
        #         self.slug = f"{base_slug}-{counter}"
        #         counter += 1
        
        # # Add hyphens between words in the custom slug
        # self.slug = self.slug.replace(" ", "-")

        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title


    
class Blog(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=256, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    meta_title = models.CharField(max_length=256, null=True, blank=True)
    meta_description = models.CharField(max_length=256, null=True, blank=True)
    image = models.ForeignKey(ImageGallery, on_delete=models.CASCADE, limit_choices_to={'image__isnull': False})
    description = RichTextUploadingField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    
    
    
    def save(self, *args, **kwargs):
        
        
        if not self.slug:
            self.slug = slugify(self.title)

        # Replace spaces with hyphens in the slug
        self.slug = self.slug.replace(' ', '-')

        # Check if the slug is unique, if not, append a counter
        counter = 1
        original_slug = self.slug
        while Blog.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            self.slug = f"{original_slug}-{counter}"
            counter += 1
        
        # # If a custom slug is not provided, generate one from the title
        # if not self.slug:
        #     self.slug = slugify(self.title)
        #     base_slug = slugify(self.title)
        #     self.slug = base_slug

        #     # Check if a blog with the same slug already exists
        #     # counter = 1
        #     # while Blog.objects.filter(slug=self.slug).exists():
        #     #     print("Exists")
        #     #     self.slug = f"{base_slug}-{counter}"
        #     #     counter += 1
        
        # # Add hyphens between words in the custom slug
        # self.slug = self.slug.replace(" ", "-")

        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
class Contact(models.Model):
    name = models.CharField(max_length=256, null=True, blank=True)
    email = models.CharField(max_length=256, null=True, blank=True)
    subject = models.CharField(max_length=256, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    error = models.ImageField(blank=True, upload_to='error/')
    
    def __str__(self):
        return self.name
    

class AnalyticsScript(models.Model):
    script = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.script
    
class Webmaster(models.Model):
    script = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.script