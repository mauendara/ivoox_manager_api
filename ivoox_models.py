import dateparser
import re
import json

class IvooxEntity:

    def __init__(self, **entries):
        self.__dict__.update(entries)

    def to_dict(self):
        return self.__dict__

    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, json_str):
        json_dict = json.loads(json_str)
        return cls(**json_dict)


class IvooxEpisode(IvooxEntity):

    def create_episode(self, link, title, date):
        self.link = link
        self.title = title
        self.date = '{0:%Y-%m-%d %H:%M:%S}'.format(dateparser.parse(date))
        self.full_number = re.findall('\d{1}x{1}\d{2}', title)[0]
        self.season_number = self.full_number.split('x')[0]
        self.episode_number = self.full_number.split('x')[1]
        return self


class IvooxComment(IvooxEntity):

    def create_comment(self, text, username, date, episode_full_number):
        self.text = text
        self.username = username
        self.date = '{0:%Y-%m-%d %H:%M:%S}'.format(dateparser.parse(date))
        self.episode_full_number = episode_full_number
        return self