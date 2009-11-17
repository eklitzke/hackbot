# -*- python -*-
# hackbot.tac
# run like:  twistd -y hackbot.tac

from twisted.internet import ssl
from twisted.application.internet import SSLClient, TCPClient
from twisted.application import service

from hackbot import HackbotFactory 
from hackbot.config import config

def make_service():
	serv = service.MultiService()

	hb_factory = HackbotFactory()
	if config.get('ssl', False):
		ctx_factory = ssl.ClientContextFactory()
		bot_service = SSLClient(config['server'], config['port'], hb_factory, ctx_factory)
	else:
		bot_service = TCPClient(config['server'], config['port'], hb_factory)
	bot_service.setServiceParent(serv)

	return serv

application = service.Application('hackbot irc robot')
s = make_service()
s.setServiceParent(service.IServiceCollection(application))
