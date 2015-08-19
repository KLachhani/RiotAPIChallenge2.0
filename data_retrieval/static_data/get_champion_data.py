__author__ = 'Kishan'

from config import config
from data_retrieval import url_requests
from  data_retrieval.static_data import io


def get_champion_by_id(region='euw'):
    url = 'https://global.api.pvp.net/api/lol/static-data/' \
          + region + '/v1.2/champion?locale=en_US&champData=all&api_key=' \
          + config.riot_api_key

    champion_by_id = url_requests.request(url)['keys']
    io.write_json(champion_by_id, 'champions_by_id.json')
    return champion_by_id


def get_champion_by_key(region='euw'):
    champion_by_name = dict(
        zip(get_champion_by_id(region).values(), get_champion_by_id(region).keys()))

    io.write_json(champion_by_name, 'champions_by_name.json')


def main():
    get_champion_by_key()
    get_champion_by_id()


if __name__ == '__main__':
    main()
