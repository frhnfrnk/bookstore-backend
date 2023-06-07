from django.http import JsonResponse
from django.db import connection

from rest_framework.decorators import api_view
from rest_framework import status


@api_view(['GET'])
def category_list(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM Category')
        rows = cursor.fetchall()
    
    categories = []
    for row in rows:
        category = {
            'category_id': row[0],
            'category_name': row[1]
        }
        categories.append(category)

    return JsonResponse(categories, safe=False)

@api_view(['GET'])
def book_category_list(request, pk):
    # Filter books by category
    with connection.cursor() as cursor:
        cursor.execute('SELECT book_id FROM book_category WHERE category_id = %s', [pk])
        rows = cursor.fetchall()

    books = []
    for row in rows:
        with connection.cursor() as cursor:
            cursor.execute('SELECT title FROM Book WHERE book_id = %s', [row[0]])
            book_row = cursor.fetchone()
        
        book = {
            'book_id': row[0],
            'title': book_row[0]
        }
        books.append(book)
        
    return JsonResponse(books, safe=False)

@api_view(['GET'])
def publisher_list(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM Publisher')
        rows = cursor.fetchall()

    publishers = []
    for row in rows:
        with connection.cursor() as cursor:
            cursor.execute('SELECT book_id, title FROM Book WHERE publisher_id = %s', [row[0]])
            book_rows = cursor.fetchall()
        
        books = []
        for book_row in book_rows:
            book = {
                'book_id': book_row[0],
                'title': book_row[1]
            }
            books.append(book)

        publisher = {
            'publisher_id': row[0],
            'publisher_name': row[1],
            'books': books
        }
        publishers.append(publisher)

    return JsonResponse(publishers, safe=False)

@api_view(['GET'])
def book_publisher_list(request, pk):
    with connection.cursor() as cursor:
        cursor.execute('SELECT book_id, title FROM Book WHERE publisher_id = %s', [pk])
        rows = cursor.fetchall()

    books = []
    for row in rows:
        book = {
            'book_id': row[0],
            'title': row[1]
        }
        books.append(book)

    return JsonResponse(books, safe=False)

@api_view(['GET'])
def language_list(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM Language')
        rows = cursor.fetchall()

    languages = []
    for row in rows:
        with connection.cursor() as cursor:
            cursor.execute('SELECT COUNT(*) FROM Book WHERE language_id = %s', [row[0]])
            num_books_row = cursor.fetchone()
            
        language = {
            'language_id': row[0],
            'language_name': row[1],
            'num_books': num_books_row[0]
        }
        languages.append(language)

    return JsonResponse(languages, safe=False)

@api_view(['GET'])
def book_language_list(request, pk):
    with connection.cursor() as cursor:
        cursor.execute('SELECT book_id, title FROM Book WHERE language_id = %s', [pk])
        rows = cursor.fetchall()

    books = []
    for row in rows:
        book = {
            'book_id': row[0],
            'title': row[1]
        }
        books.append(book)

    return JsonResponse(books, safe=False)

@api_view(['GET', 'POST'])
def author_list(request):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM Author')
            rows = cursor.fetchall()
        
        authors = []
        for row in rows:
            with connection.cursor() as cursor:
                cursor.execute('SELECT book_id, title FROM Book WHERE book_id IN (SELECT book_id FROM book_author WHERE author_id = %s)', [row[0]])
                book_rows = cursor.fetchall()
            
            books = []
            for book_row in book_rows:
                book = {
                    'book_id': book_row[0],
                    'title': book_row[1]
                }
                books.append(book)
            
            author = {
                'author_id': row[0],
                'author_name': row[1],
                'books': books
            }
            authors.append(author)

        return JsonResponse(authors, safe=False)
    
    elif request.method == 'POST':
        author_data = {
            'author_name': request.data.get('author_name')
        }

        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO Author (author_name) VALUES (%s)', [author_data['author_name']])

        return JsonResponse({'message': 'Author created successfully!'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def book_author_list(request, pk):
    with connection.cursor() as cursor:
        cursor.execute('SELECT book_id, title FROM Book WHERE book_id IN (SELECT book_id FROM book_author WHERE author_id = %s)', [pk])
        rows = cursor.fetchall()

    books = []
    for row in rows:
        book = {
            'book_id': row[0],
            'title': row[1]
        }
        books.append(book)

    return JsonResponse(books, safe=False)


    
