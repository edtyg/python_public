import slack_sdk
import datetime as dt
from local_credentials.api_key_others import SLACK_ED_PERSONAL


class slack:
    # https://slack.dev/python-slack-sdk/web/index.html#messaging

    def __init__(self, token):
        self.token = token
        self.client = slack_sdk.WebClient(token=self.token)  # reading my stored token

    def post_message(self, channel, text, blocks=None):
        post_message = self.client.chat_postMessage(
            channel=channel, text=text, blocks=blocks
        )
        # use .data to grab the data of the message - like channel, ts etc..
        return post_message

    def post_scheduled_message(self, channel, text, post_at):
        schedule_message = self.client.chat_scheduleMessage(
            channel=channel, text=text, post_at=post_at
        )

        return schedule_message

    def check_scheduled_messages(self):
        checking_scheduled_messages = self.client.chat_scheduledMessages_list()
        return checking_scheduled_messages


if __name__ == "__main__":
    slack_client = slack(SLACK_ED_PERSONAL)  # personal token
    msg1 = slack_client.post_message(channel="#general", text="hi")
