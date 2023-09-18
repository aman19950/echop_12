
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
from .models import Signup

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signup
        fields = '__all__'
