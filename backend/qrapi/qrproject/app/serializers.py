from rest_framework import serializers
from .models import Department, Subject, Student, Admin, Invigilator, Payment


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'  # or specify fields as a list, e.g., ['id', 'name']

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'  # or specify fields as a list, e.g., ['id', 'name', 'semester', 'department']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'  # or specify fields as a list, e.g., ['id', 'name', 'register_number', 'department', ...]

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'  # or specify fields as a list, e.g., ['id', 'name', 'admin_number']

class InvigilatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invigilator
        fields = '__all__'  # or specify fields as a list, e.g., ['id', 'name', 'invigilator_number']

class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'  # Exclude student and department, as they can be set in the view
