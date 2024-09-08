from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, phone_number, full_name, display_name, password):
        if not phone_number:
            raise ValueError('user must have phone number')
        
        elif not full_name:
            raise ValueError('user must have full name')
        
        elif not password:
            raise ValueError('user must have password')

        user = self.model(phone_number=phone_number, full_name=full_name, display_name=display_name)
        user.set_password(password)
        user.save()

        return user
    
    def create_superuser(self , phone_number, full_name, display_name , password):
        user = self.create_user(phone_number=phone_number, full_name=full_name, password=password, display_name=display_name)
        user.is_admin = True
        user.save()

        return user