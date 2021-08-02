import requests
import csv
from sample import userCredentials
from sample import parseaccount

#Confluence Page ID

def postOnConfluence():
    page_id = '1497858644'
    credentials = (userCredentials.user['user_name'],userCredentials.user['password'])

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
    with open('temp/accountslist.csv') as l:
        reader = csv.reader(l, delimiter=',')
        for row in reader:
            content += '<tr>'
            #last 7 digits in bold
            content += f'<td>{row[0][0:10]}<b>{row[0][10:17]}</b></td>'
            content += f'<td>{row[1]}</td>'
            #color de element
            content += f'<td style="background-color: {parseaccount.getColor(row[2])};">{row[2]}</td>'
            content += f'<td>{row[3]}</td>'
            content += f'<td style="background-color: {parseaccount.getColor(row[4])};">{row[4]}</td>'
            content += '</tr>'
        content += '</tbody></table>'

    info = get_page_info(page_id, credentials)
    print(f'found page {page_id}@v{info["version"]["number"]}')

    add_content_to_page(info, content)
    bump_page_version(info)
    status = put_page(page_id, info, credentials)
    print(f'updated page {page_id}@v{status["version"]["number"]}')

    return True


# -- Confluence --
confluence_url = 'https://atc.bmwgroup.net/confluence/rest/api/content/{0}'

def get_page_info(page_id, credentials):
    url = confluence_url.format(page_id)
    r = requests.get(url, auth=credentials) #Stopped working. On postman it works on two header: authorization and cookies
    r.raise_for_status()

    response = r.json()
    page_info = slice(response, 'id', 'type', 'title')
    version = slice(response['version'], 'number')
    page_info['version'] = version

    return page_info


def put_page(page_id, page_info, credentials):
    url = confluence_url.format(page_id)
    headers = {
        'User-Agent': 'vehicleaccountautomation/0.0.1',
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate',
        'Cache-Control': 'no-cache'
    }
    response = requests.put(url, headers=headers, json=page_info, auth=credentials)
    response.raise_for_status()
    return response.json()


def bump_page_version(page_info):
    page_info['version']['number'] += 1

def add_content_to_page(page_info, content):
    page_info['body'] = {
        'storage': {
            'value': content,
            'representation': 'storage'
        }
    }

def slice(dict, *keys):
    return {k: dict[k] for k in keys}