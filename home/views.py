from django.shortcuts import render
from rest_framework import status
from rest_framework.exceptions import NotFound,PermissionDenied
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import *
from .serializers import *
import logging
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

# for normal token authentication
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated

# for jwt token authentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

#for manually generating JWT token for a user
from rest_framework_simplejwt.tokens import RefreshToken

#Generic Views
from rest_framework import generics






logger = logging.getLogger(__name__)

# Create your views here.

###################################################################################################################################################

#generic view method for crud
        
###################################################################################################################################################


class StudentGeneric(generics.ListAPIView,generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class =StudentSerializer

class StudentGeneric1(generics.UpdateAPIView,generics.DestroyAPIView):
    queryset = Student.objects.all()
    serializer_class =StudentSerializer
    lookup_field = 'id'
     






















###################################################################################################################################################

#APIVIEW method for crud
        
###################################################################################################################################################



class RegisterUser(APIView):

    def post(self,request):
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'status': status.HTTP_403_FORBIDDEN, 'message': 'Something went wrong','error':serializer.errors})

        serializer.save()
        user = User.objects.get(username=serializer.data['username'])

        #As soon as user registers user will get a token 


        # manually getting a normal token for user 
        # token_obj, _ = Token.objects.get_or_create(user=user)

        # manually getting a JWT token for user 
        # if u want to generate token manually for a user then u may call this method 
        refresh = RefreshToken.for_user(user)

        # manually getting a normal token for user 
        # return Response({'status': status.HTTP_200_OK, 'payload': serializer.data, 'token':str(token_obj), 'message': 'Your data has been saved '})

        # manually getting a JWT token for user 
        return Response({'status': status.HTTP_200_OK, 'payload': serializer.data, 'refresh': str(refresh),
        'access': str(refresh.access_token), 'message': 'Your data has been saved '})



# APIVIEW Reduces Routing overhead ; one route for all student apis 
class StudentAPI(APIView):
      
      authentication_classes = [JWTAuthentication]
      permission_classes = [IsAuthenticated] # only authenticated users can access this api
      def get(self,request):
        print(f"User accessing GET STUDENTS API: '{request.user}'")
        paginator = PageNumberPagination()
        student_objs = Student.objects.all().order_by('id')
        page = paginator.paginate_queryset(student_objs, request)
    
        if page is not None:
            serializer = StudentSerializer(page, many=True)
            response_data = paginator.get_paginated_response(serializer.data)
            response_data.data['status'] = status.HTTP_200_OK  
            return response_data
        else:
            serializer = StudentSerializer(student_objs, many=True)
            return Response({'status': status.HTTP_200_OK, 'payload': serializer.data})
      
      def post(self,request):
        print(f"User accessing POST STUDENTS API: '{request.user}'")
        data = request.data
        print(data)
        serializer = StudentSerializer(data=data)
        if serializer.is_valid():
                        serializer.save()
        else:
            logging.info('error reason: ' + str(serializer.error_messages))
            print()
            print(f"Errors are: '{serializer.error_messages}'")
            return Response({'status': status.HTTP_403_FORBIDDEN,'errors':serializer.errors, 'message':"Something went wrong"})
            
        logging.info('Successfully added student information')
        return Response({'status': status.HTTP_200_OK, 'payload': serializer.data,'message':'Student added'})
      
      def put(self, request):
        print(f"User accessing PUT STUDENTS API: '{request.user}'")
        try:
            student_id = request.data.get('id')  # Extract 'id' from request data
            student_obj = Student.objects.get(id=student_id)

            serializer = StudentSerializer(student_obj, data=request.data)

            if not serializer.is_valid():
                logging.info('error reason: ' + str(serializer.errors))
                print(f"Errors are: '{serializer.error_messages}'")
                return Response({'status': status.HTTP_403_FORBIDDEN, 'errors': serializer.errors, 'message': "Something went wrong"})
            serializer.save()
            logging.info('Successfully updated student information')
            return Response({'status': status.HTTP_200_OK, 'payload': serializer.data, 'message': 'Student updated'})

        except Student.DoesNotExist:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'message': 'Student not found'})
        except Exception as e:
            return Response({'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': str(e)})

      def patch(self, request):
        print(f"User accessing PATCH STUDENTS API: '{request.user}'")
        try:
            student_id = request.data.get('id')  # Extract 'id' from request data
            student_obj = Student.objects.get(id=student_id)

            serializer = StudentSerializer(student_obj, data=request.data, partial=True)

            if not serializer.is_valid():
                logging.info('error reason: ' + str(serializer.errors))
                print(f"Errors are: '{serializer.error_messages}'")
                return Response({'status': status.HTTP_403_FORBIDDEN, 'errors': serializer.errors, 'message': "Something went wrong"})

            serializer.save()
            logging.info('Successfully updated student information')
            return Response({'status': status.HTTP_200_OK, 'payload': serializer.data, 'message': 'Student updated'})

        except Student.DoesNotExist:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'message': 'Student not found'})
        except Exception as e:
            return Response({'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': str(e)})

      
      def delete(self,request):
        print(f"User accessing DELETE STUDENTS API: '{request.user}'")
        # alternate delete also works if you provide id in url as query param  instead of request.data.get('id') use id = request.GET.get('id')
        try:
            student_id = request.data.get('id')  # Extract 'id' from request data
            student_obj = Student.objects.get(id=student_id)            
            student_obj.delete()
            return Response({'status': status.HTTP_200_OK, 'message':'Student Data Deleted Successfully'})
        except Exception as e:
            print(f"Exception Caught: '{e}'")
            return Response({'status': status.HTTP_403_FORBIDDEN, 'message':'Invalid id'})



###################################################################################################################################################

#@api_view decorator method for crud
        
###################################################################################################################################################

# @api_view(['GET'])
# def get_book(request):
#     book_objs = Book.objects.all()
#     serializer = BookSerializer(book_objs, many=True)
#     if not serializer.data:
#             return Response({'status': status.HTTP_200_OK, 'message': 'No Books Present in database'})

#     return Response({'status': status.HTTP_200_OK, 'payload': serializer.data})

# @api_view(['POST'])
# def add_book(request):
#     data = request.data
#     category_name = data.get('category', {}).get('category_name')

#     try:
#         category = Category.objects.filter(category_name=category_name).first()
#         if not category:
#             return Response({'status': status.HTTP_403_FORBIDDEN, 'message': 'Category does not exist. Please create the category first.'})

#         book_data = {'category': category.id, 'book_title': data.get('book_title')}
#         book_serializer = BookSerializer(data=book_data)
#         if book_serializer.is_valid():
#             book_serializer.save(category=category)  # Assign category object directly
#             return Response({'status': status.HTTP_200_OK, 'payload': book_serializer.data, 'message': 'Book added'})
#         else:
#             return Response({'status': status.HTTP_403_FORBIDDEN, 'errors': book_serializer.errors, 'message': 'Invalid book data'})

#     except Exception as e:
#         return Response({'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': str(e)})




# @api_view(['POST'])
# def add_category(request):
#     data = request.data
#     category_serializer = CategorySerializer(data=data)
#     if category_serializer.is_valid():
#         category_serializer.save()
#         return Response({'status': status.HTTP_200_OK, 'payload': category_serializer.data, 'message': 'Category added'})
#     else:
#         return Response({'status': status.HTTP_403_FORBIDDEN, 'errors': category_serializer.errors, 'message': 'Invalid category data'})
    
# # @api_view(['GET'])
# # def home(request):
# #     paginator = PageNumberPagination()
# #     # student_objs = Student.objects.all()
# #     # serializer = StudentSerializer(student_objs, many=True)
# #     # return Response({'status': 200, 'payload': serializer.data})
# #     try:
       
# #        student_objs = Student.objects.all()
# #        if not student_objs.exists():
# #            raise NotFound("No students found")
# #        serializer = StudentSerializer(student_objs, many=True)
# #        logging.info('Successfully Retreived student information')
# #       #  return Response (serializer.data)
# #        return Response({'status': status.HTTP_200_OK, 'payload': serializer.data})
# #     except PermissionDenied:
# #        logging.info('error reason: ' + Response.get('payload'))
# #        return Response({'status': status.HTTP_403_FORBIDDEN, 'payload': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
# #     except NotFound:
# #        logging.info('error reason: ' + Response.get('payload'))
# #        return Response({'status': status.HTTP_404_NOT_FOUND, 'payload': 'Student list Empty'}, status=status.HTTP_404_NOT_FOUND)
# #     except Exception as e:
# #        logging.info('error reason: ' + str(serializer.error_messages))
# #        return Response({'status': status.HTTP_400_BAD_REQUEST, 'payload': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# def home(request):
#     paginator = PageNumberPagination()
#     student_objs = Student.objects.all()
#     page = paginator.paginate_queryset(student_objs, request)
    
#     if page is not None:
#         serializer = StudentSerializer(page, many=True)
#         response_data = paginator.get_paginated_response(serializer.data)
#         response_data.data['status'] = status.HTTP_200_OK  
#         return response_data
#     else:
#         serializer = StudentSerializer(student_objs, many=True)
#         return Response({'status': status.HTTP_200_OK, 'payload': serializer.data})

     



# @api_view(['POST'])
# def post_student(request):
#    data = request.data
#    print(data)
#    serializer = StudentSerializer(data=data)
#    if serializer.is_valid():
#       serializer.save()
#    else:
#       logging.info('error reason: ' + str(serializer.error_messages))
#       print(serializer.error_messages)
#       return Response({'status': status.HTTP_403_FORBIDDEN,'errors':serializer.errors, 'message':"Something went wrong"})
       
#    logging.info('Successfully added student information')
#    return Response({'status': status.HTTP_200_OK, 'payload': serializer.data,'message':'Student added'})

# @api_view(['PUT', 'PATCH'])
# def update_student(request, id):
#     try:
#         student_obj = Student.objects.get(id=id)

#         if request.method == 'PUT':
#             serializer = StudentSerializer(student_obj, data=request.data)
#         elif request.method == 'PATCH':
#             serializer = StudentSerializer(student_obj, data=request.data, partial=True)

#         if not serializer.is_valid():
#             logging.info('error reason: ' + str(serializer.errors))
#             print(serializer.errors)
#             return Response({'status': status.HTTP_403_FORBIDDEN, 'errors': serializer.errors, 'message': "Something went wrong"})

#         serializer.save()
#         logging.info('Successfully updated student information')
#         return Response({'status': status.HTTP_200_OK, 'payload': serializer.data, 'message': 'Student updated'})

#     except Student.DoesNotExist:
#         return Response({'status': status.HTTP_404_NOT_FOUND, 'message': 'Student not found'})
#     except Exception as e:
#         return Response({'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': 'Server error'})



# @api_view(['GET'])
# def get_student(request, id):
#     try:
#         logging.info(f"Fetching student with ID: {id}")
#         student_obj = Student.objects.get(id=id)
#         logging.info(f"Retrieved student: {student_obj}")
#         serializer = StudentSerializer(student_obj, many=False)
#         return Response({'status': status.HTTP_200_OK, 'payload': serializer.data})
#     except Student.DoesNotExist:
#         print("Student not found")
#         logging.info("Student not found")
#         return Response({'status': status.HTTP_404_NOT_FOUND, 'message': 'Student not found'})
#     except Exception as e:
#         logging.info(f"Exception occurred: {e}")
#         return Response({'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': 'Server error'})


# @api_view(['DELETE'])
# def delete_student(request,id):
#    try:
#       student_obj = Student.objects.get(id=id)
#       student_obj.delete()
#       return Response({'status': status.HTTP_200_OK, 'message':'Student Data Deleted Successfully'})
#    except Exception as e:
#       print(e)
#       return Response({'status': status.HTTP_403_FORBIDDEN, 'message':'Invalid id'})
   

# # alternate delete where u can pass id as query string in request 
# @api_view(['DELETE'])
# def delete_student_alternate(request):
#    try:
#       id = request.GET.get('id')
#       student_obj = Student.objects.get(id=id)
#       student_obj.delete()
#       return Response({'status': status.HTTP_200_OK, 'message':'Student Data Deleted Successfully'})
#    except Exception as e:
#       print(e)
#       return Response({'status': status.HTTP_403_FORBIDDEN, 'message':'Invalid id'})
