# valida la cantidad máxima permitida para cada archivo multimedia.
from django.core.exceptions import ValidationError


MAX_MEDIA_SIZE = 20 * 1024 * 1024


def validate_media_size(uploaded_file):
    if uploaded_file.size > MAX_MEDIA_SIZE:
        raise ValidationError("El archivo no puede superar los 20 MB.")
