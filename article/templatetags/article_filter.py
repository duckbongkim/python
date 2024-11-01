from django import template
import markdown 
from django import template
from django.utils.safestring import mark_safe


register = template.Library()

@register.filter ## @ 파이썬 데코레이션 
def sub(value, arg):
    return value - arg
## 템플릿 필터에 sub라는 함수를 추가함

@register.filter
def mark(value):
    extensions= ["nl2br","fenced_code"]
    return mark_safe(markdown.markdown(value,extensions=extensions))