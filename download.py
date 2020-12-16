import requests
from requests.exceptions import HTTPError
import json
import os


BASE_URL = 'https://api.figshare.com/v2/'

# the param indicates whether the target artile is private
private = False
# authorization token in header
token=''

# build target url
def endpoint(link):
    return BASE_URL + link

# create authorization header
def header(token = None):
    header = {'Content-Type':'application/json'}
    if token:
        header['Authorization'] = 'token {0}'.format(token)
    return header


def issue_request(method, url, headers, data=None, binary=False):
    if data is not None and not binary:
        data = json.dumps(data)

    response = requests.request(method, url, headers=headers, data=data)

    try:
        response.raise_for_status()
        try:
            response_data = json.loads(response.text)
        except ValueError:
            response_data = response.content
    except HTTPError as error:
        print('Caught an HTTPError: {}'.format(error))
        print('Body:\n', response.text)
        raise
    return response_data


def list_files(article_id, version=None):
    if version is None:
        if private:
            url = endpoint('account/articles/{}/files'.format(article_id))
        else:
            url = endpoint('articles/{}/files'.format(article_id))
        headers = header(token)
        response = issue_request('GET',url, headers=headers)
        return response
    else:
        request = get_article_details(article_id, version)
        return request['files']


def get_article_details(self, article_id, version=None):
    if version is None:
        if private:
            url = endpoint('/account/articles/{}'.format(article_id))
        else:
            url = endpoint('/articles/{}'.format(article_id))
    else:
        if private:
            url = endpoint('/account/articles/{}/versions/{}'.format(
                article_id,
                version))
        else:
            url = endpoint('/articles/{}/versions/{}'.format(
                article_id,
                version))
    headers = header(self.token)
    response = issue_request('GET', url, headers=headers)
    return response


def download_files(artile_id, directory=None, file_name=None):
    if (directory is None):
        directory = os.getcwd()
    list = list_files(artile_id)
    dir = os.path.join(directory, "figshare_{0}/".format(artile_id))
    os.makedirs(dir, exist_ok=True)
    print('download file at:', directory+'\n')

    for file_dict in list:
        if (file_name is None):
            print('downloading ' + file_dict['name'] + '\n')

            r = requests.get(file_dict['download_url'], stream = True, headers = header())
            with (open(dir + '/{0}'.format(file_dict['name']), 'ab')) as f:
                for chunk in r.iter_content(chunk_size = 512):
                    if chunk:
                        f.write(chunk)
        else:
            if (file_name == file_dict['name']):
                print('downloading ' + file_dict['name'] + '\n')
                r = requests.get(file_dict['download_url'], stream=True, headers=header())
                with (open(dir + '/{0}'.format(file_dict['name']), 'ab')) as f:
                    for chunk in r.iter_content(chunk_size=512):
                        if chunk:
                            f.write(chunk)

    print('download complete')


def main():
    article_id = '3523262'
    artile_name = 'suppl-1.htm'
    download_files(article_id,file_name=artile_name)


if __name__ == '__main__':
    main()
