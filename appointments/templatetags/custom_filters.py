from django import template

register = template.Library()


@register.filter
def status_badge(status):
    badges = {
        'scheduled': 'badge-scheduled',
        'confirmed': 'badge-confirmed',
        'completed': 'badge-completed',
        'cancelled': 'badge-cancelled',
    }
    return badges.get(status, 'badge-completed')
