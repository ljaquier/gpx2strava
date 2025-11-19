from dataclasses import dataclass
from datetime import datetime
import gpxpy
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

    gpx_track = gpxpy.gpx.GPXTrack()
    gpx_track.name=name
    gpx_track.description=description
    gpx_track.type=sport_type
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
    gpx_track = gpxpy.parse(gpx_content).tracks[0]
    return requests.post(
        "https://www.strava.com/api/v3/uploads",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        files={
            "file": ("activity.gpx", gpx_content, "application/gpx+xml")
        },
        data={
            "name": gpx_track.name,
            "description": gpx_track.description,
            "data_type": "gpx",
            "sport_type": gpx_track.type
        }
    )
