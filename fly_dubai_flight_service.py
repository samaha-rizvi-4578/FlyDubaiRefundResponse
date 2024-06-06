from datetime import datetime
from decimal import Decimal
from typing import List, Tuple
import json



class FlyDubaiFlightService:
    
    def cancel_api_response(self, file):
        # with open(file, "r") as read_file:
        #     data = json.load(read_file)
        pnr_response = FlyDubaiPNRResponse.from_json(file)
        # print(type(data))
        print (data)

d = FlyDubaiFlightService()
d.cancel_api_response("Cancel_API _resp.json")
