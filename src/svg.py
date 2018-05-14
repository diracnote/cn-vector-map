#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os
import requests

'''\
dump svg version for administrative divisions of china from mca.org.cn

NOTE:
some of the svg files are malformed and may outdated.
'''

def dump(path, gbcode = None):
    if not os.path.exists(path):
        os.mkdir(path)
    if not os.path.exists(os.path.join(path, 'svg')):
        os.mkdir(os.path.join(path, 'svg'))

    if not gbcode:
        prefectures = requests.post('http://202.108.98.30/selectJson', '{}').json()
        with open(os.path.join(path, 'gbcodes.json'), 'w', encoding='utf-8') as fd:
            json.dump(prefectures, fd, ensure_ascii=False, indent = '\t')

        for prefecture in prefectures:
            prefecture_code = prefecture['quHuaDaiMa']
            _dump(path, prefecture_code)
    else:
        _dump(path, gbcode)

def _dump(path, gbcode):
    province_code = gbcode[:2]
    resp = requests.get('http://202.108.98.30/flash/' + province_code + '/' + gbcode + '.svg')
    with open(os.path.join(path, 'svg', gbcode + '.svg'), 'wb') as fd:
        for chunk in resp.iter_content(chunk_size = 128):
            fd.write(chunk)

if __name__ == '__main__':
    dump('svg')
