import re

from django.core.exceptions import ValidationError


def validate_youtube_only(value):
    """
    Валидатор для проверки, что ссылка ведёт только на YouTube.
    """
    youtube_patterns = [
        r"^https?://(www\.)?youtube\.com/",
        r"^https?://youtu\.be/",
        r"^https?://(www\.)?m\.youtube\.com/",
        r"^https?://(www\.)?youtube-nocookie\.com/",
    ]

    for pattern in youtube_patterns:
        if re.match(pattern, value, re.IGNORECASE):
            return value

    raise ValidationError(
        "Разрешены только ссылки на YouTube. "
        "Ссылки на сторонние платформы запрещены."
    )
