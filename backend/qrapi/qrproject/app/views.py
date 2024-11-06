from datetime import timezone
import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Department, Subject, Student, Admin, Invigilator, Payment
from .serializers import DepartmentSerializer, SubjectSerializer, StudentSerializer, AdminSerializer, InvigilatorSerializer

class DepartmentAPI(APIView):
    def get(self, request, id=None):
        if id is not None:
            try:
                department = Department.objects.get(id=id)
                serializer = DepartmentSerializer(department)
                return Response(serializer.data)
            except Department.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            departments = Department.objects.all()
            serializer = DepartmentSerializer(departments, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            department = Department.objects.get(id=id)
            department.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Department.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class SubjectAPI(APIView):
    def get(self, request, id=None):
        if id is not None:
            try:
                subject = Subject.objects.get(id=id)
                serializer = SubjectSerializer(subject)
                return Response(serializer.data)
            except Subject.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            subjects = Subject.objects.all()
            serializer = SubjectSerializer(subjects, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            subject = Subject.objects.get(id=id)
            subject.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Subject.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class StudentAPI(APIView):
    def get(self, request, id=None):
        if id is not None:
            try:
                student = Student.objects.get(id=id)
                serializer = StudentSerializer(student)

                # Fetch department name
                department_name = student.department.name

                # Fetch semester numbers and subjects based on the department ID
                department_id = student.department.id
                subjects = Subject.objects.filter(department_id=department_id)

                # Prepare the subjects and their corresponding semester numbers
                subjects_with_semester = [
                    {
                        'subject_name': subject.name,
                        'semester_number': subject.semester,
                        'subject_date':subject.date
                    } for subject in subjects
                ]

                # Add subjects, semester data, and department name to the response
                response_data = {
                    **serializer.data,  # Include student data
                    'department_name': department_name,  # Add department name
                    'subjects': subjects_with_semester
                }

                return Response(response_data)

            except Student.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            students = Student.objects.all()
            serializer = StudentSerializer(students, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            student = Student.objects.get(id=id)
            student.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class AdminAPI(APIView):
    def get(self, request, id=None):
        if id is not None:
            try:
                admin = Admin.objects.get(id=id)
                serializer = AdminSerializer(admin)
                return Response(serializer.data)
            except Admin.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            admins = Admin.objects.all()
            serializer = AdminSerializer(admins, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            admin = Admin.objects.get(id=id)
            admin.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Admin.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class InvigilatorAPI(APIView):
    def get(self, request, id=None):
        if id is not None:
            try:
                invigilator = Invigilator.objects.get(id=id)
                serializer = InvigilatorSerializer(invigilator)
                return Response(serializer.data)
            except Invigilator.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            invigilators = Invigilator.objects.all()
            serializer = InvigilatorSerializer(invigilators, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = InvigilatorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            invigilator = Invigilator.objects.get(id=id)
            invigilator.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Invigilator.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class LoginAPI(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Check in the Student table
        try:
            student = Student.objects.get(register_number=username, password=password)
            # Fetch department name
            department_name = student.department.name if student.department else "N/A"

            # Fetch subjects and their semester numbers
            subjects = Subject.objects.filter(department=student.department)
            subjects_list = [{"subject_name": subject.name, "semester": subject.semester} for subject in subjects]

            return Response({
                'message': 'Login successful',
                'user_type': 'student',
                'user_id': student.id,
                'name': student.name,
                'register_number': student.register_number,
                'department_name': department_name,
                'college_name': student.college_name,
                'university_name': student.university,
                'dob': student.dob,
                'subjects': subjects_list,
            }, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            pass  # Move on to the next check if not found

        # Check in the Admin table
        try:
            admin = Admin.objects.get(admin_number=username, password=password)
            return Response({
                'message': 'Login successful',
                'user_type': 'admin',
                'user_id': admin.id,
            }, status=status.HTTP_200_OK)
        except Admin.DoesNotExist:
            pass  # Move on to the next check if not found

        # Check in the Invigilator table
        try:
            invigilator = Invigilator.objects.get(invigilator_number=username, password=password)
            return Response({
                'message': 'Login successful',
                'user_type': 'invigilator',
                'user_id': invigilator.id,
            }, status=status.HTTP_200_OK)
        except Invigilator.DoesNotExist:
            pass  # Move on to the next check if not found

        # If none found, return error
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)


class RegisterStudentView(APIView):
    def post(self, request):
        serializer = StudentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Registration successful", "student": serializer.data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


@api_view(['GET', 'POST', 'PATCH'])
def payment_handler(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if request.method == 'GET':
        # List all payments for the student
        payments = Payment.objects.filter(student=student).values()
        return JsonResponse(list(payments), safe=False, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # Create a new payment
        data = request.data
        try:
            payment = Payment(
                student=student,
                department=student.department,
                semester_number=data['semester_number'],
                subjects=data['subjects'],
                payment_successful=True  # Set payment_successful to True upon creation
            )
            payment.save()
            return JsonResponse({'message': 'Payment created successfully!', 'payment_id': payment.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        # Update payment status
        data = request.data
        payment_id = data.get('payment_id')  # Assume payment ID is provided in the request body
        payment = get_object_or_404(Payment, id=payment_id, student=student)
        payment.payment_successful = data.get('payment_successful', payment.payment_successful)
        payment.save()
        return JsonResponse({'message': 'Payment status updated successfully!'}, status=status.HTTP_200_OK)

    return JsonResponse({'error': 'Invalid method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)




@api_view(['GET', 'POST', 'PATCH'])
def cash_payment(request,student_id):
    student = get_object_or_404(Student, id=student_id)

    if request.method == 'GET':
        # List all payments for the student
        payments = Payment.objects.filter(student=student).values()
        return JsonResponse(list(payments), safe=False, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # Create a new payment
        data = request.data
        try:
            payment = Payment(
                student=student,
                department=student.department,
                semester_number=data['semester_number'],
                subjects=data['subjects'],
                payment_successful=False  # Set payment_successful to True upon creation
            )
            payment.save()
            return JsonResponse({'message': 'Payment created successfully!', 'payment_id': payment.id},
                                status=status.HTTP_201_CREATED)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        # Update payment status
        data = request.data
        payment_id = data.get('payment_id')  # Assume payment ID is provided in the request body
        payment = get_object_or_404(Payment, id=payment_id, student=student)
        payment.payment_successful = data.get('payment_successful', payment.payment_successful)
        payment.save()
        return JsonResponse({'message': 'Payment status updated successfully!'}, status=status.HTTP_200_OK)

    return JsonResponse({'error': 'Invalid method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)






@csrf_exempt  # Disable CSRF protection for this view
def student_payments_view(request, payment_id=None):
    if request.method == 'GET':
        # If a payment_id is provided, fetch that specific payment
        if payment_id is not None:
            payment = get_object_or_404(Payment, id=payment_id)
            payment_data = {
                'id': payment.id,
                'student_name': payment.student.name,
                'student_register_number': payment.student.register_number,
                'department_name': payment.department.name,
                'semester_number': payment.semester_number,
                'subjects': payment.subjects,
                'payment_successful': payment.payment_successful,
                'payment_date': payment.payment_date.isoformat(),  # Format date to ISO
            }
            return JsonResponse(payment_data)

        # If no payment_id is provided, return all payments
        payments = Payment.objects.select_related('student', 'department').values(
            'id',  # Include the ID for each payment
            'student__name',
            'student__register_number',
            'department__name',
            'semester_number',
            'subjects',
            'payment_successful',
            'payment_date'
        )

        payments_list = [
            {
                'id': payment['id'],  # Include the ID for each payment
                'student_name': payment['student__name'],
                'student_register_number': payment['student__register_number'],
                'department_name': payment['department__name'],
                'semester_number': payment['semester_number'],
                'subjects': payment['subjects'],
                'payment_successful': payment['payment_successful'],
                'payment_date': payment['payment_date'].isoformat(),  # Format date to ISO
            }
            for payment in payments
        ]
        return JsonResponse(payments_list, safe=False)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            student = get_object_or_404(Student, register_number=data['register_number'])
            department = get_object_or_404(Department, name=data['department'])

            payment = Payment.objects.create(
                student=student,
                department=department,
                semester_number=data['semester_number'],
                subjects=data['subjects'],
                payment_successful=data.get('payment_successful', False),  # Default to False if not provided
            )
            return JsonResponse({'message': 'Payment created successfully', 'payment_id': payment.id}, status=201)
        except (KeyError, ValueError) as e:
            return HttpResponseBadRequest(f'Invalid data: {e}')

    elif request.method == 'PUT':
        if payment_id is not None:
            try:
                payment = get_object_or_404(Payment, id=payment_id)
                data = json.loads(request.body)

                # Update payment details
                payment.semester_number = data.get('semester_number', payment.semester_number)
                payment.subjects = data.get('subjects', payment.subjects)
                payment.payment_successful = data.get('payment_successful', payment.payment_successful)
                payment.save()

                return JsonResponse({'message': 'Payment updated successfully'})
            except (KeyError, ValueError) as e:
                return HttpResponseBadRequest(f'Invalid data: {e}')
        else:
            return JsonResponse({'error': 'Payment ID is required'}, status=400)

    elif request.method == 'DELETE':
        if payment_id is not None:
            try:
                payment = get_object_or_404(Payment, id=payment_id)
                payment.delete()
                return JsonResponse({'message': 'Payment deleted successfully'})
            except Exception as e:
                return HttpResponseBadRequest(f'Invalid request: {e}')
        else:
            return JsonResponse({'error': 'Payment ID is required'}, status=400)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
