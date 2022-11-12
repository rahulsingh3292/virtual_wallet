
from  .models import Transaction

PAYMENT_SEND_PREMIUM_USER_CHARGES = 3 
PAYMENT_SEND_NON_PREMIUM_USER_CHARGES = 5
PAYMENT_RECEIVE_PREMIUM_USER_CHARGES = 1
PAYMENT_RECEIVE_NON_PREMIUM_USER_CHARGES = 3

def get_charges(user,is_received=False):
  if user.is_superuser: return 0
  
  elif user.is_premium_user and not is_received:
    return PAYMENT_SEND_PREMIUM_USER_CHARGES  
  elif not user.is_premium_user and not is_received:
    return PAYMENT_SEND_NON_PREMIUM_USER_CHARGES  
  
  elif user.is_premium_user: 
    return PAYMENT_RECEIVE_PREMIUM_USER_CHARGES 
  else: 
    return PAYMENT_RECEIVE_NON_PREMIUM_USER_CHARGES
    

def create_transaction(user,amount,balance,remark,is_received=False):
  transaction = Transaction(user=user,amount=amount,balance=balance,remark=remark)
    
  if is_received:
    transaction.is_added = False 
   
  transaction.charges = get_charges(user,is_received)
  transaction.save()

