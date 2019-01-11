from tinydb import TinyDB, Query

class IvooxDataManager:

    EPISODES_TABLE = 'episodes'

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
                self.insert_episode(e.as_dict())


    def get_episodes(self):
        episodes = self.db.table(self.EPISODES_TABLE)
        return episodes.all()