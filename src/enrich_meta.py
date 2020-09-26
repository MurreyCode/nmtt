import os
from requests import Session, Request
from json import load, loads
from datetime import datetime


def load_api_params(api_name):
    with open(os.getenv('API_PATH'), 'r') as api_file:
        api_dict = load(api_file).get(api_name)
    with open(os.getenv('API_KEYS_PATH'), 'r') as api_file:
        api_key = load(api_file).get(api_name).get('api_key')
    return api_dict, api_key


def parse_track_meta(content, metadata):
    metadata['album'] = [content.get('album').get('album').get('title')]
    toptags = content.get('toptags').get('tag')
    metadata['organization'] = [label.get('name') for label in toptags[:5]]
    return metadata


def parse_album_meta(content: dict,
                     metadata: dict):
    if content.get('wiki'):
        date_str = content.get('wiki').get('published')
        metadata['date'] = [datetime.strptime(date_str, "%d %b %Y, %H:%M").year]
    else:
        tags = content.get('tags').get('tag')
        for tag_name in [tag.get('name') for tag in tags]:
            if len(tag_name) == 4 and tag_name.isdigit() and int(tag_name) > 1950:
                metadata['date'] = [tag_name]
                return metadata
    return metadata


def get_metadata(info_type: str,
                 url: str,
                 method_params: dict,
                 metadata: dict):

    session = Session()
    call_method = method_params.pop('call_method')
    method_params['artist'] = metadata.get('artist')
    method_params[info_type] = metadata.get(info_type)
    request_setup = Request(method=call_method,
                            url=url,
                            params=method_params)
    prepared_request = session.prepare_request(request_setup)
    response = session.send(prepared_request)
    if response.ok:
        content = loads(response.content).get(info_type)
        return parse_track_meta(content, metadata) \
            if info_type == 'track' else parse_album_meta(content, metadata)
    return metadata


def enrich_meta(metadata):
    api_dict, api_key = load_api_params('lastfm')
    api_url = api_dict.get('url')
    api_methods = api_dict.get('methods')
    for info_type in ['track', 'album']:
        if metadata.get(info_type):
            method_params = api_methods.get(info_type)
            method_params['api_key'] = api_key
            metadata = get_metadata(info_type='track',
                                    url=api_url,
                                    method_params=method_params,
                                    metadata=metadata)
    return metadata
