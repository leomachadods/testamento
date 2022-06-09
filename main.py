from datetime import datetime, timedelta

import logging
from re import U
from typing import Callable
import requests
from telegram import ChatInviteLink, TelegramObject, Update, Dice 
import telegram
from configurations import CHAT_ID, TOKEN_BOT
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackContext,
    Filters,
    Updater
)

import responses

VERIFY_EMAIL, SEND_LINK, CONVERSATION, INVALID_EMAIL, BUTTON = range(5)

class TelegramBot:
    def __init__(self) -> None:
        self.updater = Updater(TOKEN_BOT)

# função start simplesmente cria o comando start
# Sempre recebe dois argumentos
# Primeiro argumento: objeto do tipo update, que permite você lidar com as mensagens
# Segundo argumento: tem muitas informações sobre o bot, inclusive o estado atual do bo   
        
    def get_informacoes_user(self):
        create_url = f'https://api.telegram.org/bot{TOKEN_BOT}/getUpdates'
        resp = requests.get(create_url)
        dados = resp.json()
        

    
    def start(self, update: Update, context: CallbackContext):
        self.get_informacoes_user()
        update.message.reply_text(
            f'''Olá {update.effective_user.first_name} 😁 Digite abaixo seu e-mail exatamente como você colocou quando foi realizada a sua inscrição do nosso produto!

Dúvidas: @alisson_dourado
            ''')
        return VERIFY_EMAIL
    
    def help_command(self, update: Update, context: CallbackContext) -> None:
        dice = Dice(6, 'DiceEmoji.DICE' )
        update.message.reply_text(dice)
        # logging.info(invite)

    def message_handler(self, update: Update, context: CallbackContext) -> None:
        txt = str(update.message.text).lower()
        option = responses.sample_responses(txt)
        update.message.reply_text(option)

    def criar_convite(self):
        atual = datetime.now() + timedelta(minutes=60)
        timestamp = int(datetime.timestamp(atual))
        create_url = f'https://api.telegram.org/bot{TOKEN_BOT}/createChatInviteLink?chat_id=-100{CHAT_ID}&member_limit=1&expire_date={timestamp}'
        resp = requests.get(create_url)
        dados = resp.json()
        link_telegram = str(dados['result']['invite_link'])
        return link_telegram

    def enviar_link_grupo(self, update: Update, context: CallbackContext, link) -> Callable:
        update.message.reply_text(f'Link do grupo: {link}')
    
    def email_invalido(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_text('Por favor digite um email válido')
        
        return VERIFY_EMAIL
        
    def validar_licenca(self, email):
        lista = ['email@gmail.com', 'teste@gmail.com', 'ola@hotmail.com']
        return email in lista
    
    def email_handler(self, update: Update, context: CallbackContext) -> Callable:
        txt = str(update.message.text)
        email = responses.get_email(txt)
        email_eh_valido = responses.validar_email(email)
        if email_eh_valido:
            eh_valida = self.validar_licenca(email)
            if eh_valida:
                link = self.criar_convite()
                self.enviar_link_grupo(update, context, link)
            else:
                update.message.reply_text(f'''Não encontrei o email {email} na minha base de dados. Verifique como foi digitado e tente novamente.
                                          
Caso o erro persista entre em contato com o nosso suporte 
@SuporteRoulleteMegaBot''')
        else:
            self.email_invalido(update, context)
        
    def end(self, update: Update, context: CallbackContext) -> None:
        user = update.message.from_user
        update.message.reply_text("Tchau, nos vemos na próxima ")
        return ConversationHandler.END

    def echo(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_text(update.message.text)
    
    def run_bot(self) -> None:
        dispatcher = self.updater.dispatcher
        # Usar o bot atraves do token, e ver as atualizações
        # mensageiro, expedidor, enviar mensagens
        main_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start)],
            states = {
                VERIFY_EMAIL: [MessageHandler(Filters.text, self.email_handler),],
                CONVERSATION: [MessageHandler(Filters.text, self.message_handler)]
            },
            fallbacks=[CommandHandler('sair', self.end)]
        )

        dispatcher.add_handler(main_handler)
        
        self.updater.start_polling()
        self.updater.idle()

def main():
    bot = TelegramBot()
    bot.get_informacoes_user()
    bot.run_bot()

if __name__ == '__main__':
    print('Pressione CTRL + C para parar')
    main()
