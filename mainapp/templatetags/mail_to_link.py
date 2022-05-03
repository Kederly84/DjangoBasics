from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def email_to_link(email: str):
    return mark_safe(f"<a href='mailto:{email}'>{email}</a>")


