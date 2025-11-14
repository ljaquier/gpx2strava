from dataclasses import dataclass
from datetime import datetime
import gpxpy
from xml.etree.ElementTree import Element
import requests
import gpx2strava.utils as utils


@dataclass
class TrackPoint:
    latitude: float
    longitude: float
    elevation: float
    time: datetime

def get_gpx(name, description, sport_type, track_points):
    gpx = gpxpy.gpx.GPX()
    gpx.creator='gpx2strava.py with barometer'
    gpx.name=name
    gpx.description=description

    ext_sport_type = Element('sport_type')
    ext_sport_type.text=sport_type
    gpx.metadata_extensions=[ext_sport_type]
    
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)

    for track_point in track_points:
        gpx_segment.points.append(
            gpxpy.gpx.GPXTrackPoint(
                latitude=track_point.latitude,
                longitude=track_point.longitude,
                elevation=track_point.elevation,
                time=track_point.time
            )
        )

    return gpx.to_xml()

def get_access_token(config):
    response = requests.post(
        "https://www.strava.com/oauth/token",
        data={
            "client_id": config["client_id"],
            "client_secret": config["client_secret"],
            "grant_type": "refresh_token",
            "refresh_token": config["refresh_token"],
        },
    ).json()

    if "access_token" not in response:
        raise Exception(f"Error refreshing token: {response}")

    config['refresh_token'] = response["refresh_token"]

    return response["access_token"]

def upload_to_strava(access_token, gpx_content):
    gpx = gpxpy.parse(gpx_content)
    return requests.post(
        "https://www.strava.com/api/v3/uploads",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        files={
            "file": ("activity.gpx", gpx_content, "application/gpx+xml")
        },
        data={
            "name": gpx.name,
            "description": gpx.description,
            "data_type": "gpx",
            "sport_type": next((ext.text for ext in gpx.metadata_extensions if ext.tag == 'sport_type'), None)
        }
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Create activity on Strava from a GPX file')
    parser.add_argument('config_file', nargs='?', help='Config file')
    parser.add_argument('gpx_file', nargs='?', help='GPX file')

    args = parser.parse_args()
    if args.config_file and args.gpx_file:
        config = utils.load_json(args.config_file)
        with open(args.gpx_file) as f:
            response = upload_to_strava(get_access_token(config), f.read())
            print(f"{args.gpx_file} : {response.status_code} : {response.text}")
        utils.save_json(args.config_file, config)
    else:
        parser.print_help()
