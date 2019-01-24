from ivoox_data_manager import *
from ivoox_requests import *
from config import *
import logging

if __name__ == "__main__":
    logging.basicConfig(filename='main.log',
                        level=logging.INFO,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    config = read_config()

    requests = IvooxRequests(config['ivoox_base_url'], config['ivoox_podcast_url'])
    data_manager = IvooxDataManager(config['database_env'])

    # episodes = requests.request_podcast_episodes()
    # data_manager.update_episodes(episodes)
    #
    # episodes = data_manager.get_episodes()
    # for e in episodes:
    #    comments = requests.request_episode_comments(e)
    #    data_manager.update_comments(comments)

    # data_manager.delete_comments()
    # comments = requests.request_episode_comments(episodes[0])
    # for c in comments:
    #     data_manager.insert_comment(c.to_dict())

    # episodes = data_manager.get_episodes()
    # data_manager.find_poles_in_episodes(episodes)
    # poles = data_manager.get_poles_sorted()
    # for p in poles:
    #     print(p.to_dict())

    # data_manager.delete_poles()
    print(data_manager.count_poles_by_season('9'))
