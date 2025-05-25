from django.core.validators import ValidationError

def validate_file_size(file):
    file_size = file.size
    limit_mb = 5

    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError(f"Your file should be less than {limit_mb}MB")