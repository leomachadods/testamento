import re
from re import search
# basicamente 
def sample_responses(input_text):
    user_message = str(input_text).lower()

    if user_message in ('oi', 'ola', 'olá'):
        return "Olá, prazer te conhecer!"
    elif 'canal' in user_message:
        return "Estamos criando essa funcionalidade ainda..."
        
    return 'Não entendi'

def get_email(texto):
    try:
        if texto:
            return str(search(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', texto)[0])
    except:
        return None
    

def validar_email(email):
    if email:
        return str(search(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', email)[0]) != ''
    return False