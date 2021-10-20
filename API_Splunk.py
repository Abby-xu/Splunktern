#!/usr/bin/python -u

import urllib
from urllib.parse import urlencode
import httplib2
from xml.dom import minidom
import time
import json

def splunk_Auth():
    baseurl = 'https://localhost:8089' # input("baseurl: ") 

    keep_loop = True
    while keep_loop:
        userName = input("userName: ")
        password = input("password: ")
        # Authenticate with server.
        # Disable SSL cert validation. Splunk certs are self-signed.
        serverContent = httplib2.Http(disable_ssl_certificate_validation=True).request(baseurl + '/services/auth/login',
            'POST', headers={}, body=urlencode({'username':userName, 'password':password}))[1]
        # print("serverContent:\n", serverContent)
        if not ("WARN" in str(serverContent)):
            keep_loop = False
            print("successfully login!!!\nbaseurl:", baseurl, "\ncurrent user:", userName)
    return baseurl, serverContent

def splunk_Search(baseurl, serverContent):
    searchQuery=[] #searchJob queue
    
    ##### input search jobs to the queue #####
    keep_input_searchJob = True
    while keep_input_searchJob:
        searchJob = 'sourcetype=csv | head 5' # input("search job('X' for stop): ")
        searchJob_test = 'sourcetype=csv | head 10' ### testing case ###
        # if searchJob == 'X':
        keep_input_searchJob = False
        searchQuery.append(searchJob)
        searchQuery.append(searchJob_test) ### testing case ###

    ##### traverse each search job #####
    for i in searchQuery:
        print("##########\ncurrent search job:", str(i))
        start = time.time()
        # check if the query has the search operator
        if not str(i).startswith('search'):
            i = 'search ' + i
        sessionKey = minidom.parseString(serverContent).getElementsByTagName('sessionKey')[0].childNodes[0].nodeValue
        # print("sessionKey: \n", sessionKey)
        sid_body = httplib2.Http(disable_ssl_certificate_validation=True).request(baseurl + '/services/search/jobs','POST', headers={'Authorization': 'Splunk %s' % sessionKey},body=urllib.parse.urlencode({'search': i}))[1]
        sid = minidom.parseString(sid_body).getElementsByTagName("sid")[0].childNodes[0].nodeValue
        print ("sid:", sid)
        splunk_JobResult(baseurl, sessionKey, sid)
        end = time.time()
        print("search time:", end - start)

def splunk_JobResult(baseurl, sessionKey, sid):
    start = time.time()
    response = httplib2.Http(disable_ssl_certificate_validation=True).request(baseurl + '/services/search/jobs/' + sid + "?output_mode=json", 'POST', headers={'Authorization': 'Splunk %s' % sessionKey},body=urllib.parse.urlencode({}))[1]
    data = json.loads(response)
    while not data["entry"][0]["content"]["isDone"]:
        time.sleep(0.001)
        response = httplib2.Http(disable_ssl_certificate_validation=True).request(baseurl + '/services/search/jobs/' + sid + "?output_mode=json", 'POST', headers={'Authorization': 'Splunk %s' % sessionKey},body=urllib.parse.urlencode({}))[1]
        data = json.loads(response)
    request_time = time.time() - start
    print ("result event count:", data["entry"][0]["content"]["eventCount"], "request time:", request_time)
    result_response = httplib2.Http(disable_ssl_certificate_validation=True).request(baseurl + '/services/search/jobs/' + sid + "/results", 'GET', headers={'Authorization': 'Splunk %s' % sessionKey},body=urllib.parse.urlencode({"output_mode": "json"}))[1]
    results = json.loads(result_response)["results"]
    assert data["entry"][0]["content"]["eventCount"] == len(results)
    end = time.time()
    print("result count:", len(results), "result request time:", end - start)


if __name__ == '__main__':
    baseurl, serverContent = splunk_Auth()
    splunk_Search(baseurl, serverContent)
    print("##########\nfinish all search jobs!!!")