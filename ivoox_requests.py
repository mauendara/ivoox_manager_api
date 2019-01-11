from requests_html import HTMLSession
import re
import json
import dateparser

class IvooxRequests:

    BASE_URL = 'https://www.ivoox.com'
    PODCAST_URL_NAME = 'podcast-1up-radio-team_sq_f112100_1.html'
    URL_SEPARATOR = '/'

    def __init__(self):
        self.session = HTMLSession()
        self.episodes = []

    def request_podcast_episodes(self):
        response = self.session.get(self.BASE_URL + self.URL_SEPARATOR + self.PODCAST_URL_NAME)
        episodes_html = response.html.find('div.modulo-type-episodio div.content')
        for e in episodes_html:
            title = e.find('p.title-wrapper a')[0]
            date = e.find('ul.action li.date')[0]
            self.episodes.append(IvooxEpisode(title.attrs['href'], title.attrs['title'], date.attrs['title']))

    def print_episodes_as_json(self):
        for e in self.episodes:
            print(e.as_json())


class IvooxEpisode:

    def __init__(self, link, title, date):
        self.link = link
        self.title = title
        self.date = '{0:%Y-%m-%d %H:%M:%S}'.format(dateparser.parse(date))
        self.full_number = re.findall('\d{1}x{1}\d{2}', title)[0]
        self.season_number = self.full_number.split('x')[0]
        self.episode_number = self.full_number.split('x')[1]

    def as_json(self):
        return json.dumps(self.__dict__)

    def as_dict(self):
        return self.__dict__


if __name__ == "__main__":
    ir = IvooxRequests()
    ir.request_podcast_episodes()
    episodes = ir.episodes
    for e in episodes:
        print(e.date)