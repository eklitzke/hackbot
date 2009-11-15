from twisted.internet import ssl
from twisted.application.internet import SSLClient
from twisted.application import service

from hackbot import HackbotFactory 
from hackbot.config import config

application = service.Application('hackbot irc robot')

hb_factory = HackbotFactory()
ctx_factory = ssl.ClientContextFactory()
bot_service = SSLClient(config['server'], config['port'], hb_factory, ctx_factory)
bot_service.setServiceParent(application)
