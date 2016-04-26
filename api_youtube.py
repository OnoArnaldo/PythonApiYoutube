# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import sys
import json
import urllib2
import codecs

BASE_DIR = os.path.dirname(__file__)
BASE_URL = 'https://www.googleapis.com/youtube/v3/'
API_CHANNELS = 'channels'
API_PLAYLIST = 'playlistItems'
API_KEY = 'YOUR KEY'

CHANNELS = [
    'videosimprovaveis',
    'nerdologia',
    'Kurzgesagt',
    '1veritasium',
    'minutephysics',
    'xadrezverbal',
    'estevaoslow',
    'Vsauce',
    'braincraftvideo',
    'CienciaTodoDia',
]


class UrlEncoder(object):
    API_URL = ''

    def __init__(self, **kwargs):
        self.args = kwargs

    def _parms(self):
        args = []
        for k, v in self.args.items():
            args.append(k + '=' + str(v))

        return '&'.join(args)

    def get(self):
        parms = '?' + self._parms() if len(self.args) else ''
        return self.API_URL + parms

    def set(self, key, value):
        if value:
            self.args[key] = value


class ApiChannel(object):
    URL = BASE_URL + API_CHANNELS
    FILE_NAME = os.path.join(BASE_DIR, 'channels.json')

    def __init__(self, channels):
        self.encoder = self.build_encoder(API_KEY)
        self.channels = channels

    def run(self):
        data = self.generate_data()
        self.save(data)

    def generate_data(self):
        encoder = self.encoder

        ret = {}
        for channel in self.channels:
            encoder.set('forUsername', channel)
            data = self.get_data(encoder.get())
            ret[channel] = self.get_playlist_id(data)

        return ret

    def get_data(self, url):
        url = urllib2.urlopen(url)
        data = url.read()
        return json.loads(data)

    def get_playlist_id(self, data):
        items = data.get('items')
        content = items[0].get('contentDetails')
        playlists = content.get('relatedPlaylists')
        return playlists.get('uploads')

    def save(self, data):
        with open(self.FILE_NAME, 'w') as f:
            f.write(json.dumps(data))
        f.close()

    def build_encoder(self, api_key):
        UrlEncoder.API_URL = self.URL

        encoder = UrlEncoder()
        encoder.set('key', api_key)
        encoder.set('part', 'contentDetails')

        return encoder


class ApiPlayList(object):
    URL = BASE_URL + API_PLAYLIST
    FILE_NAME = os.path.join(BASE_DIR, 'playlist.txt')

    def __init__(self, channels):
        self.channels = channels
        self.encoder = self.build_encoder(API_KEY)

    def run(self):
        data = self.generate_data()
        self.save(data)

    def generate_data(self):
        encoder = self.encoder
        channels = self.channels

        ret = []
        for key in channels:
            encoder.set('playlistId', channels[key])
            data = self.get_data(encoder.get())
            ret += [[key] + self.get_info(data)]

        return ret

    def get_info(self, data):
        items = data.get('items')
        snippet = items[0].get('snippet')
        title = snippet.get('title')
        published_at = snippet.get('publishedAt')
        description = snippet.get('description')

        return [title, published_at, description]

    def save(self, data):
        fname = os.path.join(BASE_DIR, 'last_update.txt')
        with codecs.open(fname, 'w', encoding='utf-8') as f:
            for key, title, published_at, description in sorted(data, key=lambda x: x[2]):
                f.write('{}: {} - {}\n'.format(published_at[:10], key, title))
        f.close()

    def get_data(self, url):
        url = urllib2.urlopen(url)
        data = url.read()
        return json.loads(data)

    def build_encoder(self, api_key):
        UrlEncoder.API_URL = self.URL

        encoder = UrlEncoder()
        encoder.set('key', api_key)
        encoder.set('part', 'snippet')
        encoder.set('maxResults', '1')

        return encoder

    @classmethod
    def import_channels(cls, fname):
        with open(fname, 'r') as f:
            text = f.read()
        f.close()

        return json.loads(text)


if __name__ == '__main__':
    args = sys.argv[1:]
    
    if '-channel' in args:
        channel = ApiChannel(CHANNELS)
        channel.run()
    
    if '-playlist' in args:
        channels = ApiPlayList.import_channels(ApiChannel.FILE_NAME)

        play_list = ApiPlayList(channels)
        play_list.run()
