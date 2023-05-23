import datetime
from telegram.ext import Updater, CommandHandler


TOKEN = '5691067018:AAEiR5PKBcLJn92g3FM2u0yhSpG1EYEBSso'


evenements = {}


def start(update, context):
    """Gestionnaire de la commande /start."""
    context.bot.send_message(chat_id=update.effective_chat.id, text="Salut ! Je suis un bot pour gérer les événements.")


def create_event(update, context):
    """Gestionnaire de la commande /create_event."""
    chat_id = update.effective_chat.id
    text = update.message.text.split(' ', 1)[1]

    donnees_evenement = text.split(',')
    if len(donnees_evenement) < 4:
        context.bot.send_message(chat_id=chat_id, text="Données insuffisantes pour créer un événement.")
        return

    date = donnees_evenement[0].strip()
    lieu = donnees_evenement[1].strip()
    heure = donnees_evenement[2].strip()
    pieces_jointes = donnees_evenement[3].strip()

   
    try:
        datetime_evenement = datetime.datetime.strptime(date + ' ' + heure, '%Y-%m-%d %H:%M')
    except ValueError:
        context.bot.send_message(chat_id=chat_id, text="Format de date ou d'heure incorrect.")
        return

   
    evenements[datetime_evenement] = {
        'lieu': lieu,
        'pieces_jointes': pieces_jointes
    }

    context.bot.send_message(chat_id=chat_id, text="Événement créé.")


def view_schedule(update, context):
    """Gestionnaire de la commande /view_schedule."""
    chat_id = update.effective_chat.id

    aujourd_hui = datetime.date.today()
    evenements_aujourd_hui = []

    for datetime_evenement, donnees_evenement in evenements.items():
        if datetime_evenement.date() == aujourd_hui:
            evenements_aujourd_hui.append((datetime_evenement, donnees_evenement))

    if not evenements_aujourd_hui:
        context.bot.send_message(chat_id=chat_id, text="Il n'y a pas d'événements prévus pour aujourd'hui.")
        return

    message = "Événements pour aujourd'hui :\n\n"
    for datetime_evenement, donnees_evenement in evenements_aujourd_hui:
        message += f"Date/heure : {datetime_evenement.strftime('%Y-%m-%d %H:%M')}\n"
        message += f"Lieu : {donnees_evenement['lieu']}\n"
        message += f"Pièces jointes : {donnees_evenement['pieces_jointes']}\n\n"

    context.bot.send_message(chat_id=chat_id, text=message)
