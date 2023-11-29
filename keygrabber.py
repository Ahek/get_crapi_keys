import requests
import socket

def get_developer_login():
    try:
        with open('developer_credentials.txt') as f:
            txt_logindata = f.read()
            dict_logindata = eval(txt_logindata)
    except Exception as e:
        print(f"Problem reading credentials file in get_developer_login() function:\n{e}")
    return dict_logindata

def get_key():
    '''
    check whether the current ip already has a key
        if not, call get_new_key to make a new one
    '''
    base_url = 'https://developer.clashroyale.com'
    session = requests.Session()
    
    key_request = get_current_keys()
    if 'keys' in key_request:
        current_keys = key_request['keys']
    
    my_public_ip = get_public_ip()
    for key in current_keys:
        if my_public_ip in key['cidrRanges']:
            my_token = key['key']
            return my_token
    keyname = input("New key needed, give it a name: ")
    keydescription = input("New key description: ")
    return get_new_key(base_url, session, my_public_ip, keyname, keydescription)

def get_current_keys():
     '''
    Returns current_keys(dict)
            - keys(list of dicts)
                - keys[x]:
                    - cidrRanges: allowed ip addresses in list
                    - description
                    - developerId
                    - id
                    - key
                    - name
                    - origins
                    - scopes
                    - tier
                    - validUntil
            - sessionExpiresInSeconds(INT)
            - status(dict):
                - code(INT)
                - message(STR): 'ok' if everything good
                - detail(STR/None): NoneType if good
     '''
     session = requests.Session()
     
     base_url = 'https://developer.clashroyale.com'
     email, password = get_developer_login().values()
     session.post(url = f'{base_url}/api/login', 
                  json = {'email':email, 'password':password})
     
     key_request = session.post(url = f'{base_url}/api/apikey/list', json = {}).json()
     return key_request
    
def get_new_key(base_url, session, public_ip, name, description):
    session.post(url=f"{base_url}/api/apikey/create", 
                 json={'cidrRanges': [public_ip], 
                       'name':name,
                       'description': description, 
                       'scopes': 'royale'})
    keys_request = get_current_keys()
    current_keys = keys_request['keys']
    new_key = current_keys[0]
    my_token = new_key['key']
    return my_token
    
def get_public_ip():
    # Use a public DNS server to get the public IP address
    dns_resolver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dns_resolver.connect(("1.1.1.1", 80))  # Using Google's public DNS server
    public_ip = dns_resolver.getsockname()[0]
    dns_resolver.close()
    return public_ip

my_key = get_key()
