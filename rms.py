from errbot import BotPlugin, re_botcmd
import datetime
import random
import re

CONFIG_TEMPLATE = {
    'TIMEOUT': 600
}

class RMS(BotPlugin):
    """
    Corrects people when they say Linux but mean GNU/Linux
    """

    responses = (
        "I believe what you are referring to is actually GNU/Linux.",
        "Are you sure you don't mean GNU/Linux?",
        "I think you mean GNU/Linux--or, as I've taken to calling it, GNU plus Linux.",
        "_clears throat_ I believe you mean GNU/Linux.",
    )

    @re_botcmd(pattern=r"(^| )linux( |$)", prefixed=False, flags=re.IGNORECASE)
    def linux(self, msg, args):
        """
        You mentined linux. Are you sure you didn't mean GNU/Linux?
        """

        if not self.be_sassy():
            self.log.debug('Limiting sassiness')
            return

        if 'gnu' in msg.body.lower():
            self.log.debug('Skipping message containing GNU')
            return

        self['LAST_RUN'] = datetime.datetime.now()

        return random.choice(self.responses)

    def get_configuration_template(self):
        return CONFIG_TEMPLATE

    def be_sassy(self):
        if 'LAST_RUN' not in self.keys():
            return True

        if self.config is None or self.config['TIMEOUT'] is None:
            self.config = CONFIG_TEMPLATE

        return datetime.datetime.now() >= self['LAST_RUN'] + datetime.timedelta(seconds=self.config['TIMEOUT'])
