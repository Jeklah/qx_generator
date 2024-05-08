import json
import getopt
import time
import sys
import requests

BG_PASS = '\x1b[2;30;42m'
BG_FAIL = '\x1b[2;30;41m'
BG_RESET = '\x1b[0m'
HEADERS = {'Content-Type': 'application/json'}
DATA = {'action': 'start'}
standards = []
gamuts = []
test_patterns = []
count = 0

try:
    opts, args = getopt.getopt(sys.argv[1:], 'h', ['help'])
    # for _ in args:
    #     print(_)
    unit = args[0]
    base_url = f'http://{unit}.local:8080/api/v1/generator/standards/'
except getopt.GetoptError:
    print('generate_standards_long.py')
    sys.exit(2)

response = requests.get(base_url, headers=HEADERS, data=json.dumps(DATA))
resp_str = json.dumps(response.json())

resp_dict = json.loads(resp_str)

for entry in resp_dict['links']:
    if entry['rel'] != 'self':
        standards.append(entry)

for standard in standards:
    # print(f'{standard["href"]}')
    response = requests.get(
        standard['href'], headers=HEADERS, data=json.dumps(DATA))
    resp_str2 = json.dumps(response.json())
    resp_dict_std = json.loads(resp_str2)
    for resp in resp_dict_std['links']:
        if resp['rel'] == 'self':
            continue
        # print(f'{resp["href"]}')
        response_gamut = requests.get(
            resp['href'], headers=HEADERS, data=json.dumps(DATA)
        )
        gamut_str = json.dumps(response_gamut.json(), indent=4)
        # print(f'{gamut_dict}')
        gamut_dict = json.loads(gamut_str)
        for gam in gamut_dict['links']:
            # print(gamut)
            if gam['rel'] == 'self':
                continue
            gamuts.append(gam)
            for gamut in gamuts:
                # print(gamut['href'])
                response_test_pattern = requests.get(
                    gamut['href'], headers=HEADERS, data=json.dumps(DATA)
                )
                test_pattern_str = json.dumps(
                    response_test_pattern.json(), indent=4)
                # print(f'{test_pattern_str}')
                test_patter_dict = json.loads(test_pattern_str)
                for pattern in test_patter_dict['links']:
                    if pattern['rel'] == 'self':
                        continue
                    test_patterns.append(pattern)
                    for patt in test_patterns:
                        generate_resp = requests.put(
                            patt['href'],
                            headers=HEADERS,
                            data=json.dumps(DATA)
                        )
                        time.sleep(4.5)
                        if response.status_code == 200:
                            count += 1
                            print(
                                f'Generating std {count}: {patt["href"]} - {BG_PASS}PASS{BG_RESET}')
                        # print(patt['href'])
