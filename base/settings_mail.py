from .config_mail_perso import *

# EMAIL SETTINGS 

EMAIL_USE_TLS = True
EMAIL_HOST_USER = MY_EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = MY_EMAIL_HOST_PASSWORD
EMAIL_HOST = MY_EMAIL_HOST
EMAIL_PORT = MY_EMAIL_PORT
URL_COMPLETE = MY_URL_COMPLETE

# Autorisation des pages de création de compte/récupération du mot de passe
AUTORISE_CREATION = False
AUTORISE_RECUPERATION = True

# possibilité de ne pas envoyer le mail et d'afficher le texte en console
ENVOIE_MAIL = MY_ENVOIE_MAIL