from django.contrib.auth.models import User
from rest_framework import serializers
from .models import PerfilUsuario
from django.utils import timezone


class UsuarioSerializer(serializers.ModelSerializer):
    rol = serializers.CharField(source='perfil.rol', read_only=True)
    rol_display = serializers.CharField(source='perfil.get_rol_display', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'email', 'rol', 'rol_display']


class UsuarioCreateSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=150)
    correo = serializers.EmailField()
    rol = serializers.ChoiceField(choices=PerfilUsuario.ROL_CHOICES)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        nombre = validated_data['nombre']
        correo = validated_data['correo']
        rol = validated_data['rol']
        password = validated_data['password']

        user = User.objects.create_user(
            username=correo,
            email=correo,
            first_name=nombre,
            password=password
        )
        PerfilUsuario.objects.create(user=user, rol=rol)
        return user


class UsuarioUpdateSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=150)
    correo = serializers.EmailField()
    rol = serializers.ChoiceField(choices=PerfilUsuario.ROL_CHOICES)

    def update(self, instance, validated_data):
        instance.first_name = validated_data['nombre']
        instance.email = validated_data['correo']
        instance.username = validated_data['correo']
        instance.save()

        perfil, _ = PerfilUsuario.objects.get_or_create(user=instance)
        perfil.rol = validated_data['rol']
        perfil.ultima_modificacion = timezone.now()
        perfil.save()

        return instance


class PerfilActualSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nombre = serializers.CharField()
    correo = serializers.EmailField()
    rol = serializers.CharField()
    rol_display = serializers.CharField()
    usa_contrasena_temporal = serializers.BooleanField()
    ultima_sesion = serializers.DateTimeField()
    ultima_modificacion = serializers.DateTimeField()
