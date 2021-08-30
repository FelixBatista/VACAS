import requests
import csv
import parseaccount
import yaml


class ConcluenceClient:
    #Load Configuration
    config_file = yaml.load(open("config.yaml", 'r'), Loader=yaml.SafeLoader)
    confluence_url =config_file['confluence_url']
    page_id = config_file['confluence_page']

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.jwt = {    'int': '',
                        'prod': ''
                        }

    def __del__(self):
        # any cleanup task for the resources allocated BY THIS CLASS should go here
        pass

    #Confluence Page ID
    def postOnConfluence(self):
        credentials = (self.username,self.password)

        #make table header
        content = '<h2>INT and PROD accounts for each vehicle</h2>'
        content += '<table><thead><tr>'
        content += '<th>VIN</th>'
        content += '<th>Int Market</th>'
        content += '<th>Int account</th>'
        content += '<th>Prod Market</th>'
        content += '<th>Prod Account</th>'
        content += '</tr></thead><tbody>'

        #insert all rows on the table from the CSV file
        with open('generated/accountslist.csv') as l:
            reader = csv.reader(l, delimiter=',')
            for row in reader:
                content += '<tr>'
                #last 7 digits in bold
                content += f'<td>{row[0][0:10]}<b>{row[0][10:17]}</b></td>'
                content += f'<td>{row[1]}</td>'
                #color the element
                content += f'<td style="background-color: {parseaccount.getColor(row[2])};">{row[2]}</td>'
                content += f'<td>{row[3]}</td>'
                content += f'<td style="background-color: {parseaccount.getColor(row[4])};">{row[4]}</td>'
                content += '</tr>'
            content += '</tbody></table>'

        info = self._get_page_info(self.page_id, credentials)
        print(f'found page {self.page_id}@v{info["version"]["number"]}')

        self._add_content_to_page(info, content)
        self._bump_page_version(info)
        status = self._put_page(self.page_id, info, credentials)
        print(f'updated page {self.page_id}@v{status["version"]["number"]}')

        return True


    # -- Confluence --
    def _get_page_info(self, page_id, credentials):
        url = self.confluence_url.format(page_id)
        r = requests.get(url, auth=(credentials)) #Stopped working. On postman it works on two header: authorization and cookies
        r.raise_for_status()

        response = r.json()
        page_info = self._slice(response, 'id', 'type', 'title')
        version = self._slice(response['version'], 'number')
        page_info['version'] = version

        return page_info


    def _put_page(self, page_id, page_info, credentials):
        url = self.confluence_url.format(page_id)
        headers = {
            'User-Agent': 'vehicleaccountautomation/0.0.1',
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate',
            'Cache-Control': 'no-cache'
        }
        response = requests.put(url, headers=headers, json=page_info, auth=credentials)
        response.raise_for_status()
        return response.json()


    def _bump_page_version(self, page_info):
        page_info['version']['number'] += 1

    def _add_content_to_page(self, page_info, content):
        page_info['body'] = {
            'storage': {
                'value': content,
                'representation': 'storage'
            }
        }

    def _slice(self, dict, *keys):
        return {k: dict[k] for k in keys}