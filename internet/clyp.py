# -*- coding: utf-8 -*-
import datetime
import json
import logging
import os
import requests
import urllib.request


class Token:
    def __init__(self):
        self._time_expires = None
        self.token = None

    def set(self, token, expires_in):
        self._time_expires = datetime.datetime.now() + datetime.timedelta(seconds=expires_in)
        self.token = token

    def is_valid(self):
        if self.token is not None:
            if self._time_expires > datetime.datetime.now():
                return True
        return False


class Clyp:
    def __init__(self, username, password):
        self.logger = logging.getLogger('app.internet.Clyp')
        self._token = Token()
        self._user = username
        self._pass = password

    def post_track(self, track):
        _id = self.post(track.path)
        self.edit(_id, track.name, track.description)

    def post(self, path_track):
        tok = self.get_token()

        upload_url = 'https://upload.clyp.it/upload'

        music_mp3 = open(path_track, 'rb')
        filename = os.path.basename(music_mp3.name)
        send_files = {'audioFile': (filename, music_mp3, 'audio/mpeg')}

        headers = {'Host': 'upload.clyp.it',
                   'Authorization': 'Bearer ' + tok,
                   'X-Client-Type': 'WebAlfa',
                   'Referer': 'https://clyp.it/',
                   'Origin': 'https://clyp.it'}

        r = requests.post(upload_url, headers=headers, files=send_files)
        self.logger.info('Status code post : ' + str(r.status_code))

        res = json.loads(r.text)
        return res['AudioFileId']

    def edit(self, id, title, description):
        tok = self.get_token()

        track_url = 'https://api.clyp.it/' + id

        data = {'title': title, 'description': description, 'status': 'Public', 'commentsEnabled': 'false'}
        headers = {'Authorization': 'Bearer ' + tok,
                   'Content-Type': 'application/json'}
        r = requests.patch(track_url, headers=headers, json=data)
        self.logger.info('Status code edit : ' + str(r.status_code))

    def get_token(self):
        if not self._token.is_valid():
            self.logger.debug('Token is not valid')

            token_url = 'https://api.clyp.it/oauth2/token'
            headers = {'Authorization': 'Basic MjkzMTE5Og=='}
            data = 'grant_type=password&username=' + urllib.request.quote(self._user) + '&password=' + \
                   urllib.request.quote(self._pass)

            r = requests.post(token_url, headers=headers, data=data)
            self.logger.info('Status code token : ' + str(r.status_code))

            token = json.loads(r.text)['access_token']
            expires_in = json.loads(r.text)['expires_in']
            self._token.set(token, expires_in)

            self.logger.debug('New token is store')

        return self._token.token


if __name__ == '__main__':
    import time

    logger = logging.getLogger('app')

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

    # Console output
    consolelog = logging.StreamHandler()
    consolelog.setFormatter(formatter)
    logger.addHandler(consolelog)
    logger.setLevel(logging.DEBUG)

    MP3_PATH = 'PATH_TO_MP3/file.mp3'

    c = Clyp(username='USERNAME_SERVICE', password='PASSWORD_SERVICE')
    c.get_token()

    start_time = time.time()
    track_id = c.post(MP3_PATH)
    c.edit(track_id, 'test-mp3', 'desc.')
    logger.info("--- %s seconds ---" % (time.time() - start_time))
