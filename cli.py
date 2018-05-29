import argparse

# adding CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument('StationID', help="The station ID of the NWS weather station you'd like to fetch weather reports from")
parser.add_argument('Offset', help="The offset from UTC for the weather station you're fetching reports from, for accurate local timestamps",type=int)
args = parser.parse_args()

# Set variables from arguments
StationID = args.StationID
timeOffset = args.Offset

# print command line arguments
print(StationID)
print(timeOffset)