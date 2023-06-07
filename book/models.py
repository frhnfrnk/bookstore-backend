from django.db import models


# class Language(models.Model):
#     language_id = models.AutoField(primary_key=True)
#     language_name = models.CharField(max_length=255)

#     class Meta:
#         managed = False
#         db_table = 'language'
        
# class Book(models.Model):
#     book_id = models.AutoField(primary_key=True)
#     title = models.CharField(max_length=255)
#     description = models.TextField(blank=True, null=True)
#     publication_year = models.IntegerField()
#     language = models.ForeignKey(Language, models.DO_NOTHING)
#     num_pages = models.IntegerField()
#     publisher = models.ForeignKey('Publisher', models.DO_NOTHING)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     condition_value = models.TextField()  # This field type is a guess.
#     isbn13 = models.CharField(max_length=255)
#     image = models.CharField(max_length=255, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'book'

# class Author(models.Model):
#     author_id = models.AutoField(primary_key=True)
#     author_name = models.CharField(max_length=255)

#     class Meta:
#         managed = False
#         db_table = 'author'

# class BookAuthor(models.Model):
#     author = models.OneToOneField(Author, models.DO_NOTHING, primary_key=True)  # The composite primary key (author_id, book_id) found, that is not supported. The first column is selected.
#     book = models.ForeignKey(Book, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'book_author'
#         unique_together = (('author', 'book'),)



# class BookCategory(models.Model):
#     book = models.OneToOneField(Book, models.DO_NOTHING, primary_key=True)  # The composite primary key (book_id, category_id) found, that is not supported. The first column is selected.
#     category = models.ForeignKey('Category', models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'book_category'
#         unique_together = (('book', 'category'),)


# class Category(models.Model):
#     category_id = models.AutoField(primary_key=True)
#     category_name = models.CharField(max_length=255)

#     class Meta:
#         managed = False
#         db_table = 'category'




# class Publisher(models.Model):
#     publisher_id = models.AutoField(primary_key=True)
#     publisher_name = models.CharField(max_length=255)

#     class Meta:
#         managed = False
#         db_table = 'publisher'




