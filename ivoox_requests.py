from ivoox_models import *
from requests_html import HTMLSession

class IvooxRequests:

    BASE_URL = 'https://www.ivoox.com'
    PODCAST_URL_NAME = 'podcast-1up-radio-team_sq_f112100_1.html'
    COMMENTS_POST_URL = 'ajx-coments_v9_getComments_1.html'
    URL_SEPARATOR = '/'

    def __init__(self):
        self.session = HTMLSession()

    def request_podcast_episodes(self):
        response = self.session.get(self.BASE_URL + self.URL_SEPARATOR + self.PODCAST_URL_NAME)
        episodes_html = response.html.find('div.modulo-type-episodio div.content')
        episodes = []
        for e in episodes_html:
            title = e.find('p.title-wrapper a')[0]
            date = e.find('ul.action li.date')[0]
            episodes.append(IvooxEpisode().create_episode(title.attrs['href'], title.attrs['title'], date.attrs['title']))
        return episodes

    def print_episodes_as_json(self):
        for e in self.episodes:
            print(e.as_json())

    def request_episode_comments(self, episode):
        response = self.session.get(episode.link)

        comments_html = response.html.find('#comments div.comment-row')
        comments = []
        for c in comments_html:
            comment = c.find('div.content div.comment p')
            if len(comment) == 1:
                comment = comment[0]
                username = c.find('div.content div.comment ul.user-info li.name a')
                if len(username) == 1:
                    username = username[0]
                    date = c.find('div.content div.comment ul.user-info li.date')[0]
                    comments.append(IvooxComment().create_comment(comment.text, username.attrs['title'], date.text,
                                                              episode.full_number))

        footer = response.html.find('div.footer-link a')[0]
        if hasattr(footer, 'data-objectid'):
            data = dict()
            data['parentId'] = '0'
            data['objectId'] = footer.attrs['data-objectid']
            data['objectType'] = footer.attrs['data-objecttype']
            data['from'] = footer.attrs['data-from']

            response = self.session.post(self.BASE_URL + self.URL_SEPARATOR + self.COMMENTS_POST_URL, data)
            if response.content != b'    ':
                comments_html = response.html.find('div.comment-row')
                for c in comments_html:
                    comment = c.find('div.content div.comment p')
                    if len(comment) == 1:
                        comment = comment[0]
                        username = c.find('div.content div.comment ul.user-info li.name a')[0]
                        date = c.find('div.content div.comment ul.user-info li.date')[0]
                        comments.append(IvooxComment().create_comment(comment.text, username.attrs['title'], date.text, episode.full_number))
        return comments
