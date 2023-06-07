from rest_framework import serializers

# from .models import Book, Author, Publisher, Category, BookCategory, Language, BookAuthor

# class BookSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Book
#         fields = '__all__'

# class PublisherSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Publisher
#         fields = '__all__'

# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = '__all__'

# class LanguageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Language
#         fields = '__all__'

# class AuthorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Author
#         fields = '__all__'

# class BookAuthorSerializer(serializers.ModelSerializer):
#     author = AuthorSerializer()

#     class Meta:
#         model = BookAuthor
#         fields = '__all__'

# class BookDetailSerializer(serializers.ModelSerializer):
#     publisher = PublisherSerializer() 
#     language = LanguageSerializer()

#     class Meta:
#         model = Book
#         fields = '__all__'
