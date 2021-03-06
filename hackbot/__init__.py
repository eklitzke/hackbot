from twisted.words.protocols import irc
from twisted.internet import reactor, protocol

from hackbot.config import config

def make_nick(user):
	if '!' in user:
		nick, _ = user.split('!', 1)
		return nick
	return user

def make_channel(channel):
	return channel.lstrip('#')

def checkuser(func):
	def inner(self, user, *args, **kwargs):
		nick = make_nick(user)
		if nick != config['owner']:
			return
		return func(self, user, *args, **kwargs)
	return inner

class Hackbot(irc.IRCClient):

	nickname = config['nickname']
	password = config['password']

	def signedOn(self):
		for channel in config['channels']:
			self.join(channel)

	def joined(self, channel):
		# ensure the IRC channel hasn't automatically joined us to a channel not
		# in the config
		channel = make_channel(channel)
		if channel not in config['channels']:
			self.leave(channel, reason='This is no place for bots!')
	
	@checkuser
	def userJoined(self, user, channel):
		if channel in config['channels']:
			self.say(channel, 'Greetings, comrade! Honor work!')
	
	@checkuser
	def privmsg(self, user, channel, message):
		if channel != self.nickname:
			# this isn't really a privmsg
			return

		cmd, message = message.split(' ', 1)
		if cmd == 'say':
			chan, msg = message.split(' ', 1)
			self.say(make_channel(chan), msg)
		elif cmd == 'join':
			self.join(make_channel(message))
		elif cmd in ('part', 'leave'):
			self.leave(make_channel(message))
		elif cmd in ('me', 'emote'):
			chan, msg = message.split(' ', 1)
			self.me(make_channel(chan), msg)

class HackbotFactory(protocol.ClientFactory):

	protocol = Hackbot

	def clientConnectionLost(self, connector, reason):
		"""Just reconnect"""
		connector.connect()
	
	def clientConnectionFailed(self, connector, reason):
		reactor.stop()
