# gpx2strava
Simple Python script/library that allows to create an activity on Strava from a GPX file.

## How to get credentials from Strava

1. Create a "My API Application"\
   https://www.strava.com/settings/api

2. Retrieve the `<client_id>` and `<client_secret>`

3. Request and allow access from a browser\
   `https://www.strava.com/oauth/authorize?client_id=<client_id>&response_type=code&redirect_uri=http://localhost/exchange_token&scope=activity:write,read`

4. Retrieve the `<authorization_code>` that is in the browser URL bar\
   `http://localhost/exchange_token?state=&code=<authorization_code>&scope=activity:write,read`

5. Exchange the `<authorization_code>` for a `<refresh_token>`\
   `curl -s -X POST https://www.strava.com/oauth/token -d client_id="<client_id>" -d client_secret="<client_secret>" -d code="<authorization_code>" -d grant_type=authorization_code`

6. Create a `config.json` with the credentials
   ```json
   {
     "client_id": "<client_id>",
     "client_secret": "<client_secret>",
     "refresh_token": "<refresh_token>"
   }
   ```

## Usage
As a script:
```bash
pip3 install -r requirements.txt -t lib
PYTHONPATH=./lib python3 gpx2strava/gpx2strava.py config.json activity.gpx
```

As a library:
```python
import gpx2strava
from datetime import datetime

# Load the config and get the access token
config = utils.load_json('config.json')
access_token = gpx2strava.get_access_token(config)

# Option 1 : From a generated GPX
gpx = gpx2strava.get_gpx('A run', 'A nice Morning run', 'Running', [
    gpx2strava.TrackPoint(
        42.234535,
        7.233453,
        1025.23,
        datetime.fromisoformat('2025-11-14T12:34:56Z')
    ),
    ...
])
response = gpx2strava.upload_to_strava(access_token, gpx)
print(f"{args.ctb_file} : {response.status_code} : {response.text}")

# Option 2 : From a GPX file
with open('activity.gpx') as f:
    gpx = f.read()
    response = gpx2strava.upload_to_strava(access_token, gpx)
    print(f"{args.ctb_file} : {response.status_code} : {response.text}")

# Need to be saved to keep the new refresh token for the next execution
utils.save_json('config.json', config)
```

As a Docker container:
```
docker build -t gpx2strava .
docker run -it --rm -v config.json:/usr/src/app/config.json -v activity.gpx:/usr/src/app/activity.gpx --name gpx2strava gpx2strava
```
