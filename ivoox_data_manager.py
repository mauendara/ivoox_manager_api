from ivoox_models import *
from tinydb import TinyDB, Query

class IvooxDataManager:

    EPISODES_TABLE = 'episodes'
    COMMENTS_TABLE = 'comments'

    def __init__(self):
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

    def insert_comment(self, comment):
        comments_table = self.db.table(self.COMMENTS_TABLE)
        comments_table.insert(comment)

    def get_comments(self):
        comments_table = self.db.table(self.COMMENTS_TABLE)
        comments_documents = comments_table.all();
        comments = []
        for c in comments_documents:
            comments.append(IvooxComment(**c))
        return comments

    def delete_comments(self):
        comments_table = self.db.table(self.COMMENTS_TABLE)
        comments_table.purge();