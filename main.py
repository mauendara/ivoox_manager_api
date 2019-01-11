from ivoox_data_manager import *
from ivoox_requests import *

if __name__ == "__main__":
    requests = IvooxRequests()
    requests.request_podcast_episodes()

    data_manager = IvooxDataManager()
    data_manager.update_episodes(requests.episodes)

    print(len(data_manager.get_episodes()))