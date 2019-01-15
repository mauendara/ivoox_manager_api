from ivoox_data_manager import *
from ivoox_requests import *
from ivoox_models import *

if __name__ == "__main__":
    requests = IvooxRequests()
    data_manager = IvooxDataManager()

    episodes = requests.request_podcast_episodes()
    data_manager.update_episodes(episodes)

    episodes = data_manager.get_episodes()
    for e in episodes:
       comments = requests.request_episode_comments(e)
       for c in comments:
           data_manager.insert_comment(c.to_dict())

    # comments = requests.request_episode_comments(episodes[1])
    # for c in comments:
    #     data_manager.insert_comment(c.to_dict())
    #
    # all_comments = data_manager.get_comments()
    # for cc in all_comments:
    #      print(c.episode_full_number)
    #      print('-' + c.username)
    #      print('--' + c.text)