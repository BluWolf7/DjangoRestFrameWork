from rest_framework import serializers
from .models import *

class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model=Student
        # fields = ['name','age']
        # exclude = ['id']
        fields = '__all__'

    def validate(self, data):
        if 'age' in data and data['age'] < 18:
            raise serializers.ValidationError({'error': 'age cannot be less than 18'})

        if 'name' in data and any(char.isdigit() for char in data['name']):
            raise serializers.ValidationError({'error': 'name cannot contain numeric characters'})

        if 'father_name' in data and any(char.isdigit() for char in data['father_name']):
            raise serializers.ValidationError({'error': 'father name cannot contain numeric characters'})

        return data
    

    
