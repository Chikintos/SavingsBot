import load_django
from decimal import Decimal
from savingsApp.models import *
from django.core.exceptions import ObjectDoesNotExist

# Create a savings record
def Create_savings(user_id, username, name, description, balance, currency):
    try:
        savings = Savings()
        user, is_exist = Bot_user.objects.get_or_create(
            user_id=user_id, username=username)
        savings.bot_user = user
        savings.name = name.strip()
        savings.description = description.strip()
        savings.balance = balance.strip()  # This should be a number, be careful!
        savings.currency = currency.strip()
        savings.save()
    except Exception as e:
        print(f"Error while creating savings: {e}")

# Retrieve savings records for a user
def Get_saving(user_id):
    try:
        savings = Savings.objects.filter(bot_user_id__user_id=user_id)
        return savings
    except Exception as e:
        print(f"Error while retrieving savings: {e}")
    
        return []

# Change the balance of a savings record
def Change_saving(saving_id, value):
    try:
        saving = Savings.objects.get(id=saving_id)
        saving.balance += Decimal(value)
        saving.save()
    except ObjectDoesNotExist:
        print(f"Savings with ID {saving_id} does not exist.")
    except Exception as e:
        print(f"Error while updating savings: {e}")

# Delete a savings record
def Delete_saving(saving_id):
    try:
        saving = Savings.objects.get(id=saving_id)
        saving.delete()
    except ObjectDoesNotExist:
        print(f"Savings with ID {saving_id} does not exist.")
    except Exception as e:
        print(f"Error while deleting savings: {e}")

# Retrieve operation history for a savings record
def get_saving_history(saving_id):
    try:
        operations = Operations.objects.filter(
            savings_id=saving_id).order_by('date')
        return operations
    except Exception as e:
        print(f"Error while retrieving operation history: {e}")
        return []
