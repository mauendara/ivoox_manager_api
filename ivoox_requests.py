from ivoox_models import *
from requests_html import HTMLSession


class IvooxRequests:

    COMMENTS_POST_URL = 'ajx-coments_v9_getComments_1.html'
    URL_SEPARATOR = '/'

    def __init__(self, base_url, podcast_url):
        self.session = HTMLSession()
        self.base_url = base_url
        self.podcast_url = podcast_url

    def request_podcast_episodes(self):
        response = self.session.get(self.base_url + self.URL_SEPARATOR + self.podcast_url)
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
            user_avatar = c.find('img')[0]
            if len(comment) == 1:
                comment = comment[0]
                username = c.find('div.content div.comment ul.user-info li.name a')
                if len(username) == 1:
                    username = username[0]
                    date = c.find('div.content div.comment ul.user-info li.date')[0]
                    comments.append(IvooxComment().create_comment(comment.text, username.attrs['title'], date.text,
                                                              episode.full_number, user_avatar.attrs['src']))

        footer = response.html.find('div.footer-link a')[0]

        try:
            objectid = footer.attrs['data-objectid']
        except Exception:
            objectid = None

        if objectid is not None:
            data = dict()
            data['parentId'] = '0'
            data['objectId'] = footer.attrs['data-objectid']
            data['objectType'] = footer.attrs['data-objecttype']
            data['from'] = footer.attrs['data-from']

            response = self.session.post(self.base_url + self.URL_SEPARATOR + self.COMMENTS_POST_URL, data)
            if response.content != b'    ':
                comments_html = response.html.find('div.comment-row')
                for c in comments_html:
                    comment = c.find('div.content div.comment p')
                    user_avatar = c.find('img')[0]
                    if len(comment) == 1:
                        comment = comment[0]
                        username = c.find('div.content div.comment ul.user-info li.name a')[0]
                        date = c.find('div.content div.comment ul.user-info li.date')[0]
                        comments.append(IvooxComment().create_comment(comment.text, username.attrs['title'],
                                                                      date.text, episode.full_number, user_avatar.attrs['src']))
        return comments
