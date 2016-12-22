import requests

class html_downloader:

    def __init__(self):
        pass



    def one_downloader(self, url, method):
        if method == 'post':
            re = requests.post(url)
        else:
            re = requests.get(url)
        return re.text