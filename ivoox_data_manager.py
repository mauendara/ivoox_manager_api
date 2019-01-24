from ivoox_models import *
from tinydb import TinyDB, Query
from operator import itemgetter as i
from functools import cmp_to_key
import dateparser


class IvooxDataManager:
    EPISODES_TABLE = 'episodes'
    COMMENTS_TABLE = 'comments'
    POLES_TABLE = 'poles'

    def __init__(self, database_env):
        self.database_env = database_env
        if self.database_env == 'dev':
            self.db = TinyDB('db.json', indent=4, separators=(',', ': '))
        elif self.database_env == 'pro':
            self.db = TinyDB('db.json')

    def insert_episode(self, episode):
        episodes_table = self.db.table(self.EPISODES_TABLE)
        episodes_table.insert(episode)

    def update_episodes(self, episodes):
        episodes_table = self.db.table(self.EPISODES_TABLE)
        Episode = Query()
        for e in episodes:
            result = episodes_table.search(Episode.full_number == e.full_number)
            if not result:
                self.insert_episode(e.to_dict())

    def get_episodes(self):
        episodes_table = self.db.table(self.EPISODES_TABLE)
        episodes_documents = episodes_table.all();
        episodes = []
        for e in episodes_documents:
            episodes.append(IvooxEpisode(**e))
        return episodes

    def get_episodes_by_season(self, season):
        episodes_table = self.db.table(self.EPISODES_TABLE)
        Episode = Query()
        episodes_documents = episodes_table.search(Episode.season_number == season)
        episodes = []
        for e in episodes_documents:
            episodes.append(IvooxEpisode(**e))
        return episodes

    def get_episodes_by_season_as_dict(self, season):
        episodes_table = self.db.table(self.EPISODES_TABLE)
        Episode = Query()
        return episodes_table.search(Episode.season_number == season)

    def get_episodes_by_season_sorted(self, season):
        episodes_dicts = self.multikeysort(self.get_episodes_by_season_as_dict(season), ['-full_number'])
        episodes = []
        for e in episodes_dicts:
            episodes.append(IvooxComment(**e))
        return episodes

    def get_episode_by_full_number(self, full_number):
        episodes_table = self.db.table(self.EPISODES_TABLE)
        Episode = Query()
        episode_document = episodes_table.search(Episode.full_number == full_number)[0]
        return IvooxEpisode(**episode_document)

    def insert_comment(self, comment):
        comments_table = self.db.table(self.COMMENTS_TABLE)
        comments_table.insert(comment)

    def update_comments(self, comments):
        comments_table = self.db.table(self.COMMENTS_TABLE)
        Comment = Query()
        for c in comments:
            comment = comments_table.search(
                (Comment.episode_full_number == c.episode_full_number) &
                (Comment.username == c.username) &
                (Comment.date == c.date))
            if not comment:
                comments_table.insert(c.to_dict())

    def get_comments_by_episode_as_dict(self, episode_full_number):
        comments_table = self.db.table(self.COMMENTS_TABLE)
        Comments = Query()
        return comments_table.search(Comments.episode_full_number == episode_full_number)

    def get_comments_by_episode_sorted(self, episode_full_fumber):
        comments_dicts = self.multikeysort(self.get_comments_by_episode_as_dict(episode_full_fumber), ['date'])
        comments = []
        for c in comments_dicts:
            comments.append(IvooxComment(**c))
        return comments

    def get_comments(self):
        comments_table = self.db.table(self.COMMENTS_TABLE)
        comments_documents = comments_table.all();
        comments = []
        for c in comments_documents:
            comments.append(IvooxComment(**c))
        return comments

    def delete_comments(self):
        comments_table = self.db.table(self.COMMENTS_TABLE)
        comments_table.purge()

    def insert_pole(self, pole):
        poles_table = self.db.table(self.POLES_TABLE)
        poles_table.insert(pole)

    def delete_poles(self):
        poles_table = self.db.table(self.POLES_TABLE)
        poles_table.purge()

    def get_poles(self):
        poles_table = self.db.table(self.POLES_TABLE)
        poles_documents = poles_table.all()
        poles = []
        for p in poles_documents:
            poles.append(IvooxPole(**p))
        return poles

    def get_poles_sorted(self):
        poles_table = self.db.table(self.POLES_TABLE)
        poles_documents = poles_table.all()
        poles_sorted = self.multikeysort(poles_documents, ['-episode_full_number'])
        poles = []
        for p in poles_sorted:
            poles.append(IvooxPole(**p))
        return poles

    def get_poles_by_season(self, season):
        poles_table = self.db.table(self.POLES_TABLE)
        Pole = Query()
        poles_documents = poles_table.search(Pole.season == season)
        poles = []
        for p in poles_documents:
            poles.append(IvooxPole(**p))
        return poles

    def get_pole_by_episode(self, episode_full_number):
        poles_table = self.db.table(self.POLES_TABLE)
        Pole = Query()
        poles_documents = poles_table.search(Pole.episode_full_number == episode_full_number)
        if len(poles_documents) > 0:
            return IvooxPole(**poles_documents[0])
        else:
            return None

    def find_and_store_pole_from_episode(self, episode_full_number):
        pole = self.get_pole_by_episode(episode_full_number)
        if pole is None:
            comments = self.get_comments_by_episode_sorted(episode_full_number)
            for c in comments:
                comment_dict = c.to_dict()
                text = comment_dict['text'].lower()
                if 'pole' in text:
                    episode = self.get_episode_by_full_number(episode_full_number).to_dict()
                    time_after = dateparser.parse(comment_dict['date']) - dateparser.parse(episode['date'])
                    self.insert_pole(IvooxPole().create_pole(episode_full_number, comment_dict['username'], comment_dict['date'], comment_dict['user_avatar'], str(time_after)).to_dict())
                    break

    def find_poles_in_episodes(self, episodes):
        for e in episodes:
            self.find_and_store_pole_from_episode(e.to_dict()['full_number'])

    def count_poles_by_season(self, season):
        poles_table = self.db.table(self.POLES_TABLE)
        Pole = Query()
        poles_documents = poles_table.search(Pole.season == season)

        poles_total = dict()
        for p in poles_documents:
            try:
                number = poles_total[p['username']]
            except:
                number = None

            if number is None:
                poles_total[p['username']] = 1
            else:
                poles_total[p['username']] = number + 1

        count_poles = []
        for username, count in poles_total.items():
            count_poles.append({'username':username, 'count':count})

        return self.multikeysort(count_poles, ['-count'])

    def multikeysort(self, items, columns):
        comparers = [
            ((i(col[1:].strip()), -1) if col.startswith('-') else (i(col.strip()), 1))
            for col in columns
        ]

        def comparer(left, right):
            comparer_iter = (
                cmp(fn(left), fn(right)) * mult
                for fn, mult in comparers
            )
            return next((result for result in comparer_iter if result), 0)

        def cmp(a, b):
            return (a > b) - (a < b)

        return sorted(items, key=cmp_to_key(comparer))
