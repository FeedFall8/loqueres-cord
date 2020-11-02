def run(inputs):
    try:
        data = inputs['data']
        #print('got cmd:',data)
        if data.decode() == '/kick':
            print('kicking')
            inputs['cs'] = True
            inputs['Client'].conn.sendall(b'A'*99999)
        if inputs['cs']==True:
            print('its on!')
        if inputs['cs']==False:
            print('its off!')
    except Exception as e:
        print("error:",e)
    
