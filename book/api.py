from django.http import JsonResponse
from django.db import connection

from rest_framework.decorators import api_view
from rest_framework import status


@api_view(['GET', 'POST'])
def book_list_create(request):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM Book')
            rows = cursor.fetchall()
        
        books = []
        for row in rows:
            with connection.cursor() as cursor:
                cursor.execute('SELECT category_id FROM book_category WHERE book_id = %s', [row[0]])
                category_rows = cursor.fetchall()
            
            categories = []
            for category_row in category_rows:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT category_name FROM Category WHERE category_id = %s', [category_row[0]])
                    category_name = cursor.fetchone()[0]
                
                categories.append(category_name)

            with connection.cursor() as cursor:
                cursor.execute('SELECT author_id FROM book_author WHERE book_id = %s', [row[0]])
                author_rows = cursor.fetchall()

            authors = []
            for author_row in author_rows:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT author_name FROM Author WHERE author_id = %s', [author_row[0]])
                    author_name = cursor.fetchone()[0]

                authors.append(author_name)
            
            with connection.cursor() as cursor:
                cursor.execute('SELECT language_name FROM Language WHERE language_id = %s', [row[4]])
                language = cursor.fetchone()[0]
            
            with connection.cursor() as cursor:
                cursor.execute('SELECT publisher_name FROM Publisher WHERE publisher_id = %s', [row[6]])
                publisher = cursor.fetchone()[0]

            # get stock count from Inventory models
            with connection.cursor() as cursor:
                cursor.execute('''
                SELECT COUNT(*) FROM Inventory WHERE book_id = %s AND store_id = %s
                ''', 
                [row[0], 1]
                )
                stock_store1 = cursor.fetchone()[0]
            
            with connection.cursor() as cursor:
                cursor.execute('''
                SELECT COUNT(*) FROM Inventory WHERE book_id = %s AND store_id = %s
                ''', 
                [row[0], 2]
                )
                stock_store2 = cursor.fetchone()[0]

            book = {
                'book_id': row[0],
                'title': row[1],
                'description': row[2],
                'publication_year': row[3],
                'language': language,
                'num_pages': row[5],
                'publisher': publisher,
                'price': row[7],
                'condition_value': row[8],
                'isbn13': row[9],
                'image': row[10],
                'categories': categories,
                'authors': authors,
                'stock_store1': stock_store1,
                'stock_store2': stock_store2
            }
            books.append(book)
            
        
        return JsonResponse(books, safe=False)


    elif request.method == 'POST':
        book_data = {
            'title': request.data.get('title'),
            'description': request.data.get('description'),
            'publication_year': request.data.get('publication_year'),
            'num_pages': request.data.get('num_pages'),
            'price': request.data.get('price'),
            'condition_value': request.data.get('condition_value'),
            'isbn13': request.data.get('isbn13'),
            'image': request.data.get('image'),
            'language': request.data.get('language'),
            'publisher': request.data.get('publisher')
        }

        author = request.data.get('author')
        category = request.data.get('category')

        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO Book (title, description, publication_year, num_pages, price, condition_value, isbn13, image, language_id, publisher_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING book_id
                """,
                (
                    book_data['title'],
                    book_data['description'],
                    book_data['publication_year'],
                    book_data['num_pages'],
                    book_data['price'],
                    book_data['condition_value'],
                    book_data['isbn13'],
                    book_data['image'],
                    book_data['language'],
                    book_data['publisher'],
                ),
            )
            book_id = cursor.fetchone()[0]

        with connection.cursor() as cursor:
            cursor.execute("SELECT author_id FROM Author WHERE author_name = %s", [author])
            author_id = cursor.fetchone()[0]

        if author_id is None:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO Author (author_name)
                    VALUES (%s)
                    RETURNING author_id
                    """,
                    (
                        author,
                    ),
                )
                author_id = cursor.fetchone()[0]

        else:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO book_author (book_id, author_id)
                    VALUES (%s, %s)
                    """,
                    (
                        book_id,
                        author_id,
                    ),
                )
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT category_id FROM Category WHERE category_name = %s", [category])
            category_id = cursor.fetchone()[0]

        if category_id is None:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO Category (category_name)
                    VALUES (%s)
                    RETURNING category_id
                    """,
                    (
                        category,
                    ),
                )
                category_id = cursor.fetchone()[0]
            
        else:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO book_category (book_id, category_id)
                    VALUES (%s, %s)
                    """,
                    (
                        book_id,
                        category_id,
                    ),
                )

        response_data = {
            'book_id': book_id,
            'message': 'Book created successfully.',
        }
        return JsonResponse(response_data, safe=False, status=201)

@api_view(['GET', 'PUT', 'DELETE'])
def book_detail_update_delete(request, pk):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM Book WHERE book_id = %s', [pk])
            row = cursor.fetchone()

        if row is None:
            return JsonResponse({'error': 'Book not found'}, status=404)

        book = {
            'book_id': row[0],
            'title': row[1],
            'description': row[2],
            'publication_year': row[3],
            'language': row[4],
            'num_pages': row[5],
            'publisher': row[6],
            'price': row[7],
            'condition_value': row[8],
            'isbn13': row[9],
            'image': row[10],
        }

        publisher_id = row[6]
        with connection.cursor() as cursor:
            cursor.execute('SELECT publisher_name FROM Publisher WHERE publisher_id = %s', [publisher_id])
            publisher_row = cursor.fetchone()

        if publisher_row is None:
            book['publisher_name'] = None
        else:
            book['publisher_name'] = publisher_row[0]

        with connection.cursor() as cursor:
            cursor.execute('SELECT author_id FROM book_author WHERE book_id = %s', [pk])
            author_rows = cursor.fetchall()

        if author_rows is None:
            book['authors'] = None
        else:
            authors = []
            for author_row in author_rows:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT author_name FROM Author WHERE author_id = %s', [author_row[0]])
                    author_name_row = cursor.fetchone()
                    authors.append(author_name_row[0])
            book['authors'] = authors

        with connection.cursor() as cursor:
            cursor.execute('SELECT category_id FROM book_category WHERE book_id = %s', [pk])
            category_rows = cursor.fetchall()
        
        if category_rows is None:
            book['categories'] = None
        else:
            categories = []
            for category_row in category_rows:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT category_name FROM Category WHERE category_id = %s', [category_row[0]])
                    category_name_row = cursor.fetchone()
                    categories.append(category_name_row[0])
            book['categories'] = categories

        with connection.cursor() as cursor:
            cursor.execute('SELECT language_name FROM Language WHERE language_id = %s', [row[4]])
            language_row = cursor.fetchone()
        
        if language_row is None:
            book['language_name'] = None
        else:
            book['language_name'] = language_row[0]

        return JsonResponse(book, safe=False)
    
    elif request.method == 'PUT':
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM Book WHERE book_id = %s', [pk])
            row = cursor.fetchone()

        if row is None:
            return JsonResponse({'error': 'Book not found'}, status=404)

        book_data = {
            'title': request.data.get('title', row[1]),
            'description': request.data.get('description', row[2]),
            'publication_year': request.data.get('publication_year', row[3]),
            'language': request.data.get('language', row[4]),
            'num_pages': request.data.get('num_pages', row[5]),
            'publisher': request.data.get('publisher', row[6]),
            'price': request.data.get('price', row[7]),
            'condition_value': request.data.get('condition_value', row[8]),
            'isbn13': request.data.get('isbn13', row[9]),
            'image': request.data.get('image', row[10])
        }


        with connection.cursor() as cursor:
            cursor.execute('BEGIN;')
            cursor.execute(
                """
                UPDATE Book
                SET title = %s, description = %s, publication_year = %s, num_pages = %s,
                price = %s, condition_value = %s, isbn13 = %s, image = %s, language_id = %s,
                publisher_id = %s
                WHERE book_id = %s
                """,
                (
                    book_data['title'],
                    book_data['description'],
                    book_data['publication_year'],
                    book_data['num_pages'],
                    book_data['price'],
                    book_data['condition_value'],
                    book_data['isbn13'],
                    book_data['image'],
                    book_data['language'],
                    book_data['publisher'],
                    pk
                ),
            )
            affected_rows = cursor.rowcount
        
            if affected_rows > 0:
                # Commit transaksi jika berhasil
                cursor.execute("COMMIT;")
                print("Update successful")
            else:
                # Rollback transaksi jika tidak ada baris yang terpengaruh
                cursor.execute("ROLLBACK;")
                return JsonResponse({'error': 'Error updating book'}, status=500)

        return JsonResponse({'message': 'Book updated successfully'})

    elif request.method == 'DELETE':
        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM book_author WHERE book_id = %s', [pk])

        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM book_category WHERE book_id = %s', [pk])

        with connection.cursor() as cursor:
            cursor.execute("BEGIN;")
            cursor.execute('DELETE FROM Book WHERE book_id = %s', [pk])
            cursor.execute("COMMIT;")
        return JsonResponse({'message': 'Book was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def book_search(request, search):

    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM Book WHERE title ILIKE %s', ['%' + search + '%'])
        rows = cursor.fetchall()

    if rows == []:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM Book WHERE description ILIKE %s', ['%' + search + '%'])
            rows = cursor.fetchall()

    books = []
    for row in rows:
        book = {
            'book_id': row[0],
            'title': row[1],
            'description': row[2],
            'publication_year': row[3],
            'language': row[4],
            'num_pages': row[5],
            'publisher': row[6],
            'price': row[7],
            'condition_value': row[8],
            'isbn13': row[9],
            'image': row[10],
        }
        books.append(book)

    return JsonResponse(books, safe=False)