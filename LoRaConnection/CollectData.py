from ConvertImage import *
import json
from datetime import datetime

def create_list(list_before):
    total_list = []
    data = {
        "latitude": 21.00544595046039,
        "longtitude": 105.84517779542294,
        "tx_time": datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    }
    json_string = json.dumps(data)
    total_list.append(json_string) 
    total_list.extend(list_before)
    total_list.append('End Of Data')
    return total_list
