from django.db import connection
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view
from .models import Staff


@api_view(['GET'])
def staff_list(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM Staff')
        rows = cursor.fetchall()

    staffs = []
    for row in rows:
        with connection.cursor() as cursor:
            cursor.execute('SELECT store_id, store_name FROM Store WHERE store_id = %s', [row[6]])
            store = cursor.fetchone()
        
        with connection.cursor() as cursor:
            cursor.execute('SELECT address_id, address, city  FROM Address WHERE address_id = %s', [row[7]])
            address = cursor.fetchone()
        
        staff = {
            'staff_id': row[0],
            'first_name': row[1],
            'last_name': row[2],
            'email': row[3],
            'username': row[4],
            'password': row[5],
            'store': {
                'store_id': store[0],
                'store_name': store[1],
            },
            'address': {
                'address_id': address[0],
                'address': address[1],
                'city': address[2],
            },
            'is_manager': row[8],
        }
        staffs.append(staff)

    return Response(staffs)

@api_view(['POST'])
def signup(request):
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    email = request.data.get('email')
    username = request.data.get('username')
    password = request.data.get('password')
    store_id = request.data.get('store_id')
    address = request.data.get('address')
    is_manager = request.data.get('is_manager')

    #Apakah username ada?
    with connection.cursor() as cursor:
        cursor.execute('SELECT username FROM Staff WHERE username = %s', [username])
        row = cursor.fetchone()
    if row:
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    #Apakah email ada?
    with connection.cursor() as cursor:
        cursor.execute('SELECT email FROM Staff WHERE email = %s', [email])
        row = cursor.fetchone()
    if row:
        return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    
    # Enkripsi password
    hashed_password = make_password(password)

    # Insert user ke database
    with connection.cursor() as cursor:
        cursor.execute('''
            INSERT INTO Address (address, city, phone, postal_code) 
            VALUES (%s, %s, %s, %s)
            RETURNING address_id
            ''', 
            [address['address'], address['city'], address['phone'], address['postal_code']])
        address_id = cursor.fetchone()[0]
        cursor.execute(
            '''
                INSERT INTO Staff (first_name, last_name, email, username, password, store_id, address_id, is_manager) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING staff_id, first_name, last_name, email, username, password, store_id, address_id, is_manager
                ''',
                [first_name, last_name, email, username, hashed_password, store_id, address_id, is_manager])

    # Ambil user yang baru saja dibuat
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM Staff WHERE username = %s', [username])
        rows = cursor.fetchone()
    
    if rows:
        user = Staff()
        user.id = rows[0]
        user.first_name = rows[1]
        user.last_name = rows[2]
        user.email = rows[3]
        user.username = rows[4]
        user.password = rows[5]
        user.store_id = rows[6]
        user.address_id = rows[7]
        user.is_manager = rows[8]

        user.save()


        # Generate token
        refresh = RefreshToken.for_user(user)

        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return Response({
            'tokens': tokens,
            'staff_id': user.id,
            'isManager': user.is_manager,
            'message': 'User created successfully',
        }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # Ambil user dari database
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM Staff WHERE username = %s', [username])
        row = cursor.fetchone()


    if row:

        user = Staff()
        user.id = row[0]
        user.first_name = row[1]
        user.last_name = row[2]
        user.email = row[3]
        user.username = row[4]
        user.password = row[5]
        user.store_id = row[6]
        user.address_id = row[7]
        user.is_manager = row[8]

        # Cocokkan password
        if check_password(password, user.password):
            # Generate token
            refresh = RefreshToken.for_user(user)

            tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

            return Response({
                'tokens': tokens,
                'staff_id': user.id,
                'isManager': user.is_manager,
                'message': 'Login successful',
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Wrong password'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def logout(request):
    return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_staff(request, staff_id):
    with connection.cursor() as cursor:
        cursor.execute('DELETE FROM Staff WHERE staff_id = %s', [staff_id])
    return Response({'message': 'Staff deleted successfully'}, status=status.HTTP_200_OK)
