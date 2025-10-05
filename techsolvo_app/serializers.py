from datetime import datetime
from rest_framework import serializers
from .models import CompanyData

class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyData
        fields = '__all__'
        
    def validate_incorporate(self, value):
        if isinstance(value, str):
            try:
                date_object = datetime.strptime(value, "%d %B %Y").date()
                return date_object
            except ValueError:
                raise serializers.ValidationError("Invalid date format. Please use 'dd Month YYYY' format.")
        return value

    def to_internal_value(self, data):
        # Create a copy of the data to modify it
        mutable_data = data.copy()
        
        # Convert the 'incorporate' field to a datetime.date object
        if 'incorporate' in mutable_data:
            mutable_data['incorporate'] = self.validate_incorporate(mutable_data['incorporate'])
        
        return super().to_internal_value(mutable_data)

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)  
