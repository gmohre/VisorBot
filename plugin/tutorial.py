from disco.bot import Plugin


class VODPlugin(Plugin):
    @Plugin.command('vod')
    def command_vod(self, event):
        event.msg.reply('Vod Status!')
