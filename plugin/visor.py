from disco.bot import Plugin
from util import query_faq, get_vod_status, overquote
#classify quotes
#format quotes for expression


class VisorPlugin(Plugin):

    @Plugin.command('status', '<user:snowflake>', group='vod')
    def command_vod_status(self, user):
        """
        Calls
        :param user: User for which to retrieve void status
        :return status msg
        """
        msg = overquote(get_vod_status(user))
        event.msg.reply(msg)

    @Plugin.command('query', '<str:query...>', group='faq')
    def command_faq_queryr(self, query):
        """
        Calls
        :param query: FAQ Query
        :return answer: Answer to query
        """
        msg = overquote(query_faq(query))
        event.msg.reply(msg)