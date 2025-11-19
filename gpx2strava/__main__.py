# gpx2strava/__main__.py

if __name__ == "__main__":
    import argparse
    from gpx2strava import gpx2strava, utils

    parser = argparse.ArgumentParser(description='Create activity on Strava from a GPX file')
    parser.add_argument('config_file', nargs='?', help='Config file')
    parser.add_argument('gpx_file', nargs='?', help='GPX file')

    args = parser.parse_args()
    if args.config_file and args.gpx_file:
        config = utils.load_json(args.config_file)
        with open(args.gpx_file) as f:
            response = gpx2strava.upload_to_strava(gpx2strava.get_access_token(config), f.read())
            print(f"{args.gpx_file} : {response.status_code} : {response.text}")
        utils.save_json(args.config_file, config)
    else:
        parser.print_help()
