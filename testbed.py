import json, time
from tpeHelper import tagHelper, apiHelper

def process_tag(data, userdata):
    print(time.strftime('%Y/%m/%d %H:%M:%S') + ' ' + str(userdata) + '; ' + data + '\n')

if __name__ == '__main__':

    print('Testing tagHelper')
    tagHelper1 = tagHelper()
    tagHelper2 = tagHelper(username='admin', password='admin@123', protocol='http', ip='172.31.8.1', port=59000)
    tagHelper1.set_callback(process_tag)
    tagHelper2.set_callback(process_tag)
    i = 0
    while True:
        if i == 0:
            print('--- Streaming by Interval ---')
            print('Time: ' + time.strftime('%Y/%m/%d %H:%M:%S') + '\n')
            tag_list = json.loads('{"system":{"status":["cpuSystem","memoryTotal"],"network":["lan1NetworkUsage"]},"modbus_tcp_master":{"tcp_simulator":["tag"]}}')
            tagHelper1.set_tags(tag_list)
            tagHelper2.set_tags(tag_list)
            tagHelper1.start_stream(interval=20000, userdata='[1] Streaming, interval = 20000ms')
            tagHelper2.start_stream(interval=10000, userdata='[2] Streaming, interval = 10000ms')
        if i == 45:
            print('--- Streaming on Change ---')
            print('Time: ' + time.strftime('%Y/%m/%d %H:%M:%S') + '\n')
            tagHelper1.stop_stream()
            tagHelper2.stop_stream()
            tag_list = json.loads('{"system":{"status":["cpuUsage","memoryUsage"],"network":["lan2NetworkUsage"]},"modbus_tcp_master":{"tcp_simulator":["tag"]}}')
            tagHelper1.set_tags(tag_list)
            tagHelper2.set_tags(tag_list)
            tagHelper1.start_stream(userdata='[1] Streaming, update on change')
            tagHelper2.start_stream(userdata='[2] Streaming, update on change')
        if i == 120:
            print('--- Get Latest Value by Request ---')
            print('Time: ' + time.strftime('%Y/%m/%d %H:%M:%S') + '\n')
            tagHelper1.stop_stream()
            tagHelper2.stop_stream()
        if i >= 120 and i < 130:
            tagHelper1.get_tag_values(userdata='[1] Get latest value from tag hub')
            tagHelper2.get_tag_values(userdata='[2] Get latest value from tag hub')
        if i == 130:
            break
        time.sleep(1)
        i += 1

    time.sleep(5)
    print('Testing apiHelper')
    print('--- Invoke API ---')
    print('Time: ' + time.strftime('%Y/%m/%d %H:%M:%S') + '\n')
    apiHelper1 = apiHelper()
    apiHelper2 = apiHelper(username='admin', password='admin@123', protocol='http', ip='172.31.8.1', port=59000)
    if 'Authorization' in apiHelper1._headers:
        print('[1] Current Token: ' + apiHelper1._headers['Authorization'][7:] + '\n')
    if 'Authorization' in apiHelper2._headers:
        print('[2] Current Token: ' + apiHelper2._headers['Authorization'][7:] + '\n')
    response1 = apiHelper1.invoke_api('get', '/users/me', None)
    response2 = apiHelper2.invoke_api('get', '/users/me', None)
    print('Return Code: ' + str(response1['status']) + '\nResponse: ' + json.dumps(json.loads(response1['message']), indent=2))
    print('Return Code: ' + str(response2['status']) + '\nResponse: ' + json.dumps(json.loads(response2['message']), indent=2))

    time.sleep(5)
    print('--- Renew Token ---')
    print('Time: ' + time.strftime('%Y/%m/%d %H:%M:%S') + '\n')
    apiHelper1.renew_token()
    apiHelper2.renew_token()
    if 'Authorization' in apiHelper1._headers:
        print('[1] Renewed Token: ' + apiHelper1._headers['Authorization'][7:] + '\n')
    if 'Authorization' in apiHelper2._headers:
        print('[2] Renewed Token: ' + apiHelper2._headers['Authorization'][7:] + '\n')
    response1 = apiHelper1.invoke_api('get', '/users/me', None)
    response2 = apiHelper2.invoke_api('get', '/users/me', None)
    print('Return Code: ' + str(response1['status']) + '\nResponse: ' + json.dumps(json.loads(response1['message']), indent=2))
    print('Return Code: ' + str(response2['status']) + '\nResponse: ' + json.dumps(json.loads(response2['message']), indent=2))

