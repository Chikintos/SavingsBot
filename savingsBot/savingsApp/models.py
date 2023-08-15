from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

# Bot User model
class Bot_user(models.Model):
    user_id = models.IntegerField()
    username = models.TextField()


# Savings model
class Savings(models.Model):
    bot_user = models.ForeignKey(Bot_user, on_delete=models.CASCADE)
    name = models.TextField(max_length=30)
    description = models.TextField(max_length=150)
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.TextField(max_length=10)


# Operations model
class Operations(models.Model):
    savings = models.ForeignKey(Savings, on_delete=models.CASCADE)
    action = models.TextField(max_length=50)
    date = models.DateTimeField(auto_now_add=True, editable=False)


# Signal to create operations on savings change
@receiver(post_save, sender=Savings)
def create_operations_on_savings_change(sender, instance, **kwargs):
    if kwargs.get('created', False):
        action_description = f"Створено збереження '{instance.name}'"
        operation = Operations(savings=instance, action=action_description)
        operation.save()
    else:
        action_description = f"Зміна балансу. Актуальний баланс {instance.balance}"
        operation = Operations(savings=instance, action=action_description)
        operation.save()
