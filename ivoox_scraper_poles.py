from ivoox_data_manager import *
from ivoox_requests import *
from ivoox_models import *

SEASON = '9'

if __name__ == "__main__":
    requests = IvooxRequests()
    data_manager = IvooxDataManager()

    episodes = data_manager.get_episodes_by_season(SEASON)
    poles = data_manager.get_poles_by_season(SEASON)

    episode = episodes[0].to_dict()
    pole = poles[0].to_dict()

    if episode['full_number'] != pole['episode_full_number']:
        comments = requests.request_episode_comments(episode)
        data_manager.update_comments(comments)
        data_manager.find_poles_in_episodes(episodes)