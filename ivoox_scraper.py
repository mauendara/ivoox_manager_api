from ivoox_data_manager import *
from ivoox_requests import *
from ivoox_models import *

SEASON = '9'

if __name__ == "__main__":
    requests = IvooxRequests()
    data_manager = IvooxDataManager()

    episodes = requests.request_podcast_episodes()
    data_manager.update_episodes(episodes)

    episodes = data_manager.get_episodes_by_season(SEASON)
    i = 0
    for e in episodes:
        comments = requests.request_episode_comments(e)
        data_manager.update_comments(comments)
        i = i + 1
        if i > 2:
            break

    data_manager.find_poles_in_episodes(episodes)
