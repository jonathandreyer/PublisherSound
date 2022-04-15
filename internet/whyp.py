# -*- coding: utf-8 -*-
import datetime
import json
import logging
import os
import requests


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


class Whyp:
    def __init__(self, username, password):
        self.logger = logging.getLogger('app.internet.Whyp')
        self._token = Token()
        self._user = username
        self._pass = password

    def post_track(self, track, publish=True):
        try:
            _uuid = self.post(track.path)
            _uid = self.get_uid_track(_uuid)
            self.edit(_uid, track.name, track.description)
            if publish:
                self.publish(_uid)
            return True
        except:
            return False

    def post(self, path_track):
        _token = self.get_token()

        upload_url = 'https://api.whyp.it/api/tracks'

        music_mp3 = open(path_track, 'rb')
        filename = os.path.basename(music_mp3.name)
        multipart_form_data = {'file': (filename, music_mp3),
                               'title': (None, os.path.splitext(filename)[0])}

        headers = {'Accept': 'application/json',
                   'Host': 'api.whyp.it',
                   'Authorization': 'Bearer ' + _token,
                   'Referer': 'https://whyp.it/',
                   'Origin': 'https://whyp.it'}

        r = requests.post(upload_url, headers=headers, files=multipart_form_data)
        self.logger.debug('Status code post : ' + str(r.status_code))

        if r.status_code != 200:
            raise Exception('Error post track - Request is not valid')

        res = json.loads(r.text)

        return res['uuid']

    def get_uid_track(self, uuid):
        _token = self.get_token()

        get_slug_url = 'https://api.whyp.it/api/tracks/{}/first-long-poll'.format(uuid)

        headers = {'Authorization': 'Bearer ' + _token,
                   'Content-Type': 'application/json'}

        r = requests.get(get_slug_url, headers=headers)
        self.logger.debug('Status code edit : ' + str(r.status_code))

        if r.status_code != 200:
            raise Exception('Error get track name - Request is not valid')

        res = json.loads(r.text)

        _token = self.get_token()
        get_uid_url = 'https://api.whyp.it/api/tracks/{}'.format(res['slug'])

        headers = {'Authorization': 'Bearer ' + _token,
                   'Content-Type': 'application/json'}

        r = requests.get(get_uid_url, headers=headers)
        self.logger.debug('Status code edit : ' + str(r.status_code))

        if r.status_code != 200:
            raise Exception('Error get track uid - Request is not valid')

        res = json.loads(r.text)

        return res['track']['uid']

    def edit(self, track_uid, title, description, allow_downloads=True):
        _token = self.get_token()

        track_url = 'https://api.whyp.it/api/tracks/{}'.format(track_uid)

        data = {'title': title, 'description': description, 'allow_downloads': allow_downloads}
        headers = {'Authorization': 'Bearer ' + _token,
                   'Content-Type': 'application/json'}
        r = requests.put(track_url, headers=headers, json=data)
        self.logger.debug('Status code edit : ' + str(r.status_code))

        if r.status_code != 200:
            raise Exception('Error edit track - Request is not valid')

    def publish(self, track_uid):
        _token = self.get_token()

        publish_url = 'https://api.whyp.it/api/tracks/{}/publish'.format(track_uid)

        headers = {'Authorization': 'Bearer ' + _token}

        r = requests.post(publish_url, headers=headers)
        self.logger.debug('Status code edit : ' + str(r.status_code))

        if r.status_code != 200:
            raise Exception('Error edit track - Request is not valid')

    def get_token(self):
        if not self._token.is_valid():
            self.logger.debug('Request a new token')

            token_url = 'https://api.whyp.it/api/auth/login'
            data = {'email': self._user, 'password': self._pass}

            r = requests.post(token_url, data=data)
            self.logger.debug('Status code token : ' + str(r.status_code))

            if r.status_code != 200:
                raise Exception('Error authentication - Unable to get a token')

            token = json.loads(r.text)['access_token']
            expires_in = json.loads(r.text)['expires_in']
            self._token.set(token, expires_in)

            self.logger.debug('New token is store ({})'.format(token))

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

    w = Whyp(username='USERNAME_SERVICE', password='PASSWORD_SERVICE')
    w.get_token()

    start_time = time.time()
    track_uuid = w.post(MP3_PATH)
    track_uid = w.get_uid_track(track_uuid)
    w.edit(track_uid, 'test-mp3', 'desc.')
    w.publish(track_uid)
    logger.info("--- %s seconds ---" % (time.time() - start_time))
