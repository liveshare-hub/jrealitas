from django.db import models
from django.contrib.auth.models import User
from django.db.models.aggregates import Max
# from django.contrib.auth import get_user_model
# from django.db.models import Q

# User = get_user_model()

# class ThreadManager(models.Manager):
#     def by_user(self, **kwargs):
#         user = kwargs.get('user')
#         lookup = Q(first_person=user) | Q(second_person=user)
#         qs = self.get_queryset().filter(lookup).distinct()
#         return qs

# class Thread(models.Model):
#     first_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='thread_first_person')
#     second_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='thread_second_person')
#     updated = models.DateTimeField(auto_now=True)
#     timestamp = models.DateTimeField(auto_now_add=True)
    
#     objects = ThreadManager()
#     class Meta:
#         unique_together = ['first_person','second_person']

# class ChatMessage(models.Model):
#     thread = models.ForeignKey(Thread, on_delete=models.CASCADE, blank=True, null=True, related_name='chatmessage_thread')
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     message = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    recipent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    body = models.TextField(max_length=1000, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def send_message(from_user, to_user, body):
        sender_message = Message(
            user=from_user,
            sender=from_user,
            recipent=to_user,
            body=body,
            is_read=True
        )
        sender_message.save()

        recipent_message = Message(
            user=to_user,
            sender=from_user,
            body=body,
            recipent=from_user,
        )
        recipent_message.save()

        return sender_message

    def get_messages(user):
        users = []
        messages = Message.objects.filter(user=user).values('recipent').annotate(last=Max('date')).order_by('-last')
        for message in messages:
            users.append({
                'user': User.objects.get(pk=message['recipent']),
                'last': message['last'],
                'unread': Message.objects.filter(user=user, recipent__pk=message['recipent'], is_read=False)
            })

        return users

class ThreadChat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='th_from_user')
    recipent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='th_to_user')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.pk} - {self.sender}'