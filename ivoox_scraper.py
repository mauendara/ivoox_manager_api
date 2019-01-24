from ivoox_data_manager import *
from ivoox_requests import *
from config import *
import logging


if __name__ == "__main__":
    logging.basicConfig(filename='scraper.log',
                        level=logging.INFO,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    config = read_config()

    requests = IvooxRequests(config['ivoox_base_url'], config['ivoox_podcast_url'])
    data_manager = IvooxDataManager(config['database_env'])

    episodes = requests.request_podcast_episodes()
    logging.info('-- consulta episodios. total = ' + str(len(episodes)))
    data_manager.update_episodes(episodes)
    logging.info('-- sincronización episodios.')

    episodes = data_manager.get_episodes_by_season_sorted(str(config['ivoox_podcast_season']))
    logging.info('-- consulta ultimos episodios. temporada = ' + config['ivoox_podcast_season'])
    i = 0
    for e in episodes:
        comments = requests.request_episode_comments(e)
        logging.info('-- consulta comentarios. episodio = ' + e.to_dict()['full_number'])
        data_manager.update_comments(comments)
        logging.info('-- sincronización comentarios. total = ' + str(len(comments)))
        i = i + 1
        if i > 2:
            break

    data_manager.find_poles_in_episodes(episodes)
    logging.info('-- sincronización poles.')
