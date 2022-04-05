import jwt
import datetime
import requests
import json

time_now = datetime.datetime.now()
expiration_time = time_now+datetime.timedelta(seconds=20)
rounded_off_exp_time =round(expiration_time.timestamp())

headers = {"alg": "HS256", "typ":"JWT"}
payload = {"iss": "pcjuCAvhQ7qmjrGWqeyG6g", "exp": rounded_off_exp_time}
encoded_jwt = jwt.encode(payload, "nnLhZd4XjV9rgSMpbdHAiKvxOMyrVcZdmMyE", algorithm="HS256")
email ="surve790@gmail.com"

url ="https://api.zoom.us/v2/users/{}/meetings". format (email)
date = datetime.datetime(2022,7,5,13,30).strftime("$Y-sm-&dT%H:8M:8SZ")
obj = {"topic": "Test meeting", "starttime": date, "duration":30, "password": "12345"}
header = {"authorization": "Bearer {}".format(encoded_jwt)}
create_meeting = requests. post (url, json=obj, headers=header)
print (create_meeting.text)