
def lambda_handler(event, context):
    
    fields = ('username', 'first_name', 'last_name', 'lang')
    datas = {}
    
    for key, value in event['datas'].items():
        if key in fields :
            datas[key] = value
    
    if datas :
        event['datas'] = datas
        event['neo'] = True
    else:
        event['neo'] = False
        
    return event
