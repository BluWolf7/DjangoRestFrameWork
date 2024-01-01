from django.shortcuts import render
from rest_framework import status
from rest_framework.exceptions import NotFound,PermissionDenied
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import *
from .serializers import *
import logging


logger = logging.getLogger(__name__)

# Create your views here.

# @api_view(['GET'])
# def home(request):
#     paginator = PageNumberPagination()
#     # student_objs = Student.objects.all()
#     # serializer = StudentSerializer(student_objs, many=True)
#     # return Response({'status': 200, 'payload': serializer.data})
#     try:
       
#        student_objs = Student.objects.all()
#        if not student_objs.exists():
#            raise NotFound("No students found")
#        serializer = StudentSerializer(student_objs, many=True)
#        logging.info('Successfully Retreived student information')
#       #  return Response (serializer.data)
#        return Response({'status': status.HTTP_200_OK, 'payload': serializer.data})
#     except PermissionDenied:
#        logging.info('error reason: ' + Response.get('payload'))
#        return Response({'status': status.HTTP_403_FORBIDDEN, 'payload': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
#     except NotFound:
#        logging.info('error reason: ' + Response.get('payload'))
#        return Response({'status': status.HTTP_404_NOT_FOUND, 'payload': 'Student list Empty'}, status=status.HTTP_404_NOT_FOUND)
#     except Exception as e:
#        logging.info('error reason: ' + str(serializer.error_messages))
#        return Response({'status': status.HTTP_400_BAD_REQUEST, 'payload': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def home(request):
    paginator = PageNumberPagination()
    student_objs = Student.objects.all()
    page = paginator.paginate_queryset(student_objs, request)
    
    if page is not None:
        serializer = StudentSerializer(page, many=True)
        response_data = paginator.get_paginated_response(serializer.data)
        response_data.data['status'] = status.HTTP_200_OK  
        return response_data
    else:
        serializer = StudentSerializer(student_objs, many=True)
        return Response({'status': status.HTTP_200_OK, 'payload': serializer.data})

     



@api_view(['POST'])
def post_student(request):
   data = request.data
   print(data)
   serializer = StudentSerializer(data=data)
   if serializer.is_valid():
      serializer.save()
   else:
      logging.info('error reason: ' + str(serializer.error_messages))
      print(serializer.error_messages)
      return Response({'status': status.HTTP_403_FORBIDDEN,'errors':serializer.errors, 'message':"Something went wrong"})
       
   logging.info('Successfully added student information')
   return Response({'status': status.HTTP_200_OK, 'payload': serializer.data,'message':'Student added'})

@api_view(['PUT', 'PATCH'])
def update_student(request, id):
    try:
        student_obj = Student.objects.get(id=id)

        if request.method == 'PUT':
            serializer = StudentSerializer(student_obj, data=request.data)
        elif request.method == 'PATCH':
            serializer = StudentSerializer(student_obj, data=request.data, partial=True)

        if not serializer.is_valid():
            logging.info('error reason: ' + str(serializer.errors))
            print(serializer.errors)
            return Response({'status': status.HTTP_403_FORBIDDEN, 'errors': serializer.errors, 'message': "Something went wrong"})

        serializer.save()
        logging.info('Successfully updated student information')
        return Response({'status': status.HTTP_200_OK, 'payload': serializer.data, 'message': 'Student updated'})

    except Student.DoesNotExist:
        return Response({'status': status.HTTP_404_NOT_FOUND, 'message': 'Student not found'})
    except Exception as e:
        return Response({'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': 'Server error'})



@api_view(['GET'])
def get_student(request, id):
    try:
        logging.info(f"Fetching student with ID: {id}")
        student_obj = Student.objects.get(id=id)
        logging.info(f"Retrieved student: {student_obj}")
        serializer = StudentSerializer(student_obj, many=False)
        return Response({'status': status.HTTP_200_OK, 'payload': serializer.data})
    except Student.DoesNotExist:
        print("Student not found")
        logging.info("Student not found")
        return Response({'status': status.HTTP_404_NOT_FOUND, 'message': 'Student not found'})
    except Exception as e:
        logging.info(f"Exception occurred: {e}")
        return Response({'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': 'Server error'})


@api_view(['DELETE'])
def delete_student(request,id):
   try:
      student_obj = Student.objects.get(id=id)
      student_obj.delete()
      return Response({'status': status.HTTP_200_OK, 'message':'Student Data Deleted Successfully'})
   except Exception as e:
      print(e)
      return Response({'status': status.HTTP_403_FORBIDDEN, 'message':'Invalid id'})
   

# alternate delete where u can pass id as query string in request 
@api_view(['DELETE'])
def delete_student_alternate(request):
   try:
      id = request.GET.get('id')
      student_obj = Student.objects.get(id=id)
      student_obj.delete()
      return Response({'status': status.HTTP_200_OK, 'message':'Student Data Deleted Successfully'})
   except Exception as e:
      print(e)
      return Response({'status': status.HTTP_403_FORBIDDEN, 'message':'Invalid id'})
