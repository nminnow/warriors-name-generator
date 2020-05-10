# -*- coding: utf-8 -*-
'''Update data with query results from Crystal Pool's RDF dump.'''
import json
import ssl
import urllib.request
import rdflib

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

graph = rdflib.Graph()
graph.parse(format='n3', data=urllib.request.urlopen(
    'https://raw.githubusercontent.com/crystal-pool/Dump/master/wbdump.ttl',
    context=ctx).read().decode('utf-8'))

prefixes_en = []
suffixes_en = []
apprentices_en = 0
kits_en = 0
query_en = graph.query(
    '''SELECT ?prefix ?suffix WHERE {
        ?cat  wdt:P3  wd:Q622 .
        ?cat  p:P84  ?name .
        ?name  pq:P110  ?prefix .
        ?name  pq:P111  ?suffix .
    }''')
for row in query_en:
    prefixes_en.append(row.prefix.value)
    if row.suffix.value == 'paw':
        apprentices_en += 1
    elif row.suffix.value == 'kit':
        kits_en += 1
    else:
        suffixes_en.append(row.suffix.value)
with open('data/en.js', 'w') as fw_en:
    fw_en.write('const data = ' + json.dumps({
        'language': 'en',
        'prefixes': prefixes_en,
        'suffixes': suffixes_en,
        'apprentices': apprentices_en,
        'kits': kits_en
    }))

prefixes_CN = []
suffixes_CN = []
apprentices_CN = 0
kits_CN = 0
specials_CN = {
    '回声之歌': ['回声', '之歌'],
    '桦树皮': ['桦', '树皮']
}
query_CN = graph.query(
    '''SELECT ?translation ?suffix WHERE {
        ?cat  wdt:P3  wd:Q622 .
        ?cat  p:P84  ?name .
        ?name  pq:P85  ?translation .
        ?name  pq:P111  ?suffix .
        FILTER (lang(?translation) = 'zh-cn')
    }''')
for row in query_CN:
    if row.translation.value in specials_CN:
        prefixes_CN.append(specials_CN[row.translation.value][0])
        suffixes_CN.append(specials_CN[row.translation.value][1])
    else:
        if row.suffix.value == 'paw':
            prefixes_CN.append(row.translation.value[:-1])
            apprentices_CN += 1
        elif row.suffix.value == 'kit':
            prefixes_CN.append(row.translation.value[1:])
            kits_CN += 1
        else:
            prefixes_CN.append(row.translation.value[:-1])
            suffixes_CN.append(row.translation.value[-1])
with open('data/zh-cn.js', 'w') as fw_CN:
    fw_CN.write('const data = ' + json.dumps({
        'language': 'zh-cn',
        'prefixes': prefixes_CN,
        'suffixes': suffixes_CN,
        'apprentices': apprentices_CN,
        'kits': kits_CN
    }))

prefixes_TW = []
suffixes_TW = []
apprentices_TW = 0
kits_TW = 0
specials_TW = {
    '樺樹皮': ['樺', '樹皮']
}
query_TW = graph.query(
    '''SELECT ?translation ?suffix WHERE {
        ?cat  wdt:P3  wd:Q622 .
        ?cat  p:P84  ?name .
        ?name  pq:P85  ?translation .
        ?name  pq:P111  ?suffix .
        FILTER (lang(?translation) = 'zh-tw')
    }''')
for row in query_TW:
    if row.translation.value in specials_TW:
        prefixes_TW.append(specials_TW[row.translation.value][0])
        suffixes_TW.append(specials_TW[row.translation.value][1])
    else:
        if row.suffix.value == 'paw':
            prefixes_TW.append(row.translation.value[:-1])
            apprentices_TW += 1
        elif row.suffix.value == 'kit':
            prefixes_TW.append(row.translation.value[1:])
            kits_TW += 1
        else:
            prefixes_TW.append(row.translation.value[:-1])
            suffixes_TW.append(row.translation.value[-1])
with open('data/zh-tw.js', 'w') as fw_TW:
    fw_TW.write('const data = ' + json.dumps({
        'language': 'zh-tw',
        'prefixes': prefixes_TW,
        'suffixes': suffixes_TW,
        'apprentices': apprentices_TW,
        'kits': kits_TW
    }))
