import load_django
from decimal import Decimal

from savingsApp.models import *





# Create a savings record
def Create_savings(user_id, username, name, description, balance, currency):
    savings = Savings()
    user, is_exist = Bot_user.objects.get_or_create(
        user_id=user_id, username=username)
    savings.bot_user = user
    savings.name = name.strip()
    savings.description = description.strip()
    savings.balance = balance.strip()
    savings.currency = currency.strip()
    savings.save()


# Retrieve savings records for a user
def Get_saving(user_id):
    savings = Savings.objects.filter(bot_user_id__user_id=user_id)
    return savings


# Change the balance of a savings record
def Change_saving(saving_id, value):
    saving = Savings.objects.get(id=saving_id)
    saving.balance += Decimal(value)
    saving.save()


# Delete a savings record
def Delete_saving(saving_id):
    saving = Savings.objects.get(id=saving_id)
    saving.delete()



# Retrieve operation history for a savings record
def get_saving_history(saving_id):
    operations = Operations.objects.filter(
        savings_id=saving_id).order_by('date')
    return operations
