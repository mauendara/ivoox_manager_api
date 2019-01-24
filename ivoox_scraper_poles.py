from ivoox_data_manager import *
from ivoox_requests import *
from config import *
import logging


if __name__ == "__main__":
    logging.basicConfig(filename='scraper_poles.log',
                        level=logging.INFO,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    config = read_config()

    requests = IvooxRequests(config['ivoox_base_url'], config['ivoox_podcast_url'])
    data_manager = IvooxDataManager(config['database_env'])

    episodes = data_manager.get_episodes_by_season_sorted(str(config['ivoox_podcast_season']))
    poles = data_manager.get_poles_by_season(str(config['ivoox_podcast_season']))

    if len(episodes) > 0:
        episode = episodes[0].to_dict()

        if len(poles) > 0:
            check = False
            pole = poles[0].to_dict()
        else:
            check = True

        logging.info('-- verificando si el último episodio ya tiene pole')
        if check or episode['full_number'] != pole['episode_full_number']:
            comments = requests.request_episode_comments(IvooxEpisode(**episode))
            logging.info('-- consulta comentarios. episodio = ' + episode['full_number'])
            data_manager.update_comments(comments)
            logging.info('-- sincronización comentarios. total = ' + str(len(comments)))
            data_manager.find_poles_in_episodes(episodes)
            logging.info('-- sincronización poles.')