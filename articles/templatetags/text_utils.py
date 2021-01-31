from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.simple_tag
@stringfilter
def truncate_in_middle(value, max_length):
    """
    Truncate text in the middle by words.
    If the text is longer than the max_length,
    remove middle word until the text is less than or
    equal to max_length.
    """
    if len(value) <= max_length:
        return value

    words = value.split()

    while True:
        # Base case
        if len(words) == 1:
            return words[0][:max_length-3] + '...'

        # Keep removing middle word
        mid = len(words) // 2
        value = ' '.join(words[0:mid]) + '...' + ' '.join(words[mid+1:])
        del words[mid]

        # Check length with the ellipsis
        if len(value) <= 70:
            break

    return value
