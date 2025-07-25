import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    start_date = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr='lte')
    sender = django_filters.CharFilter(field_name='sender__user_id', lookup_expr='exact')
    conversation_participant = django_filters.CharFilter(method='filter_by_participant')

    class Meta:
        model = Message
        fields = ['sender', 'start_date', 'end_date']

    def filter_by_participant(self, queryset, name, value):
        return queryset.filter(conversation__participants__user_id=value)