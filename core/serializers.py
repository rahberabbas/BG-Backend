from rest_framework import serializers
from .models import *

class BackgroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = BG_Remove
        fields = '__all__'

class BackgroundImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BG_Add_Remove
        fields = '__all__'
        
class BackgroundColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BG_Add_color
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageGallery
        fields = '__all__'


class CategorySerializer22(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
       
class BlogListSerializer(serializers.ModelSerializer):
    image = ImageSerializer()
    category = CategorySerializer22()
    class Meta:
        model = Blog
        fields = '__all__'
        
    def to_representation(self, instance):
        # print("It Runs")
        representation = super().to_representation(instance)
        # Assuming your content field is named 'content'
        content = representation.get('description', '')

        soup = BeautifulSoup(content, 'html.parser')
        # Add 'img-fluid' class to all img tags
        # print(soup)
        for img_tag in soup.find_all('img'):
            # print(img_tag)
            src = img_tag.get('src')
            if src and not src.startswith("https://"):
            # Modify the src attribute based on the condition
                img_tag['src'] = "http://127.0.0.1:8000" + src
            img_tag['class'] = img_tag.get('class', []) + ['img-fluid-new']
            print("New Tag", img_tag)

        representation['description'] = str(soup)
        # print(representation)
        return representation
        
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class AnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyticsScript
        fields = '__all__'



class BlogSerializer(serializers.ModelSerializer):
    image = ImageSerializer()
    category = CategorySerializer22()

    class Meta:
        model = Blog
        fields = '__all__'
        
class CategorySerializer(serializers.ModelSerializer):
    blog_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'blog_count']

    def get_blog_count(self, category):
        return category.blog_set.count()