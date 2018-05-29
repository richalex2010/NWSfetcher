# NWSfetcher
Pulls a weather report from the National Weather Service, interprets, and outputs the results to a MySQL database.

Run fetcher.py with two arguments:
StationID: The ID for the NWS weather station readings you'd like to use
Offset: offset from UTC

Examples:

fetcher.py KPWM -4
returns the readings for KPWM (Portland International Jetport) and time time zone is UTC -4 (Eastern Daylight Time)

fetcher.py KASH -5
returns the readings for KASH (Boire Field Airport, Nashua, NH) and time zone is UTC -5 (Eastern Standard Time)