import requests
import json
import argparse
import pymysql

# Important variables - hard set in code, replaced with CLI arguments
#StationID = "KBDL" #nearest airport code typically
#timeOffset = -4 #timezone (from UTC)

# adding CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument('StationID', help="The station ID of the NWS weather station you'd like to fetch weather reports from")
parser.add_argument('Offset', help="The offset from UTC for the weather station you're fetching reports from, for accurate local timestamps",type=int)
args = parser.parse_args()

# Set variables from arguments
StationID = args.StationID
timeOffset = args.Offset

# Access NWS observations and load into variable 'data'
response = requests.get("https://api.weather.gov/stations/%s/observations/current" % StationID)
data = response.json()

# Temporary solution to access local JSON file, copied direct from above API
#filename = 'H:/GitHub/NWSfetcher/sample.json'
#if filename:
#   with open(filename,'r') as f:
#        data = json.load(f)

timestampRaw = data.get('properties').get('timestamp')
temperatureRaw = data.get('properties').get('temperature').get('value')
dewpointRaw = data.get('properties').get('dewpoint').get('value')
windDirectionRaw = data.get('properties').get('windDirection').get('value')
windSpeedRaw = data.get('properties').get('windSpeed').get('value')
windGustRaw = data.get('properties').get('windGust').get('value')
barometricPressureRaw = data.get('properties').get('barometricPressure').get('value')

# If data is empty, use 0
if temperatureRaw is None:
    temperatureRaw = 0

if dewpointRaw is None:
    dewpointRaw = 0

if windDirectionRaw is None:
    windDirectionRaw = 0

if windSpeedRaw is None:
    windSpeedRaw = 0

if windGustRaw is None:
    windGustRaw = 0

if barometricPressureRaw is None:
    barometricPressureRaw = 0

# Convert all data to integers

temperature = int(round(temperatureRaw)) # °C
dewpoint = int(round(dewpointRaw)) # °C
windDirection = int(round(windDirectionRaw)) # bearing
windSpeed = int(round(windSpeedRaw)) # m/s
windGust = int(round(windGustRaw)) # m/s
barometricPressure = int(round(barometricPressureRaw)) # Pa

# Unit conversion
temperatureF = (temperature * 9/5) + 32
dewpointF = (dewpoint * 9/5) + 32
windSpeedMPH = windSpeed * 2.2369
windGustMPH = windGust * 2.2369
windSpeedKPH = windSpeed * (3.6/1)
windGustKPH = windGust * (3.6/1)
barometricPressureHg = 0.0002952998751 * barometricPressure # Pa to inHg
barometricPressure = barometricPressure / 100

#rounding pressures
barometricPressure = round(barometricPressure,1)
barometricPressureHg = round(barometricPressureHg,2)

#calculate density altitude
#reference: https://www.weather.gov/media/epz/wxcalc/densityAltitude.pdf

#convert temperature in celsius to kelvin
airTemperature = temperature + 273.15

#calculate vapor pressure
vaporPressure = 6.11 * (10 ** ((7.5 * dewpoint)/(237.7 + dewpoint)))

#calculate virtual temperature
virtualTemperature = (airTemperature / (1 - ((vaporPressure / barometricPressure) * (0.378))))

#convert virtual temperature to Rankine
virtualTemperature = virtualTemperature * (9 / 5)

#calculate density altitude
densityAltitudeFt = 145366 * (1 - (((17.326 * barometricPressureHg) / virtualTemperature) ** 0.235))

#convert to metric
densityAltitudeM = densityAltitudeFt * 0.3048

#convert to readable format
densityAltitudeFt = int(round(densityAltitudeFt))
densityAltitudeM = int(round(densityAltitudeM))

#parse wind direction
if (windDirection >= 348.75) and (windDirection <=360) or (windDirection < 11.25) and (windDirection >= 0): 
    windDirectionStr = "N"
elif (windDirection >= 11.25) and (windDirection < 33.75): 
    windDirectionStr = "NNE"
elif (windDirection >= 33.75) and (windDirection < 56.25):
    windDirectionStr = "NE"
elif (windDirection >= 56.25) and (windDirection < 78.75):
    windDirectionStr = "ENE"
elif (windDirection >= 78.75) and (windDirection < 101.25):
    windDirectionStr = "E"
elif (windDirection >= 101.25) and (windDirection < 123.75):
    windDirectionStr = "ESE"
elif (windDirection >= 123.75) and (windDirection < 146.25):
    windDirectionStr = "SE"
elif (windDirection >= 146.25) and (windDirection < 168.75):
    windDirectionStr = "SSE"
elif (windDirection >= 168.75) and (windDirection < 191.25):
    windDirectionStr = "S"
elif (windDirection >= 191.25) and (windDirection < 213.75):
    windDirectionStr = "SSW"
elif (windDirection >= 213.75) and (windDirection < 236.25):
    windDirectionStr = "SW"
elif (windDirection >= 236.25) and (windDirection < 258.75):
    windDirectionStr = "WSW"
elif (windDirection >= 258.75) and (windDirection < 281.25):
    windDirectionStr = "W"
elif (windDirection >= 281.25) and (windDirection < 303.75):
    windDirectionStr = "WNW"
elif (windDirection >= 303.75) and (windDirection < 326.25):
    windDirectionStr = "NW"
elif (windDirection >= 326.25) and (windDirection < 348.75):
    windDirectionStr = "NNW"
else:
    windDirectionStr = "INV"

#work with timestamp, convert to local time

timestamp = {
    'year': timestampRaw[0:4],
    'month': timestampRaw[5:7],
    'day': timestampRaw[8:10],
    'hour': timestampRaw[11:13],
    'minute': timestampRaw[14:16],
}

#convert hour and day to int for time zone conversion
timestamp['hour'] = int(timestamp['hour']) 
timestamp['day'] = int(timestamp['day'])

#convert time zone
timestamp['hour'] = timestamp['hour'] + timeOffset 

#if time zone conversion pushes into next/previous day, adjust day and hour accordingly
if timestamp['hour'] < 0: 
    timestamp['hour'] = timestamp['hour'] + 24
    timestamp['day'] = timestamp['day'] - 1
elif timestamp['hour'] > 24:
    timestamp['hour'] = timestamp['hour'] - 24
    timestamp['day'] = timestamp['day'] + 1

#re-add leading zeroes, convert back to string
if timestamp['hour'] < 10:
    timestamp['hour'] = str('0%d' % timestamp['hour'])
else:
    timestamp['hour'] = str(timestamp['hour'])

if timestamp['day'] < 10:
    timestamp['day'] = str('0%d' % timestamp['day'])
else:
    timestamp['day'] = str(timestamp['day'])

#convert timestamp dictionary to updateTime string
updateTime = str('Last updated: %s:%s on %s-%s-%s' % (timestamp['hour'],timestamp['minute'],timestamp['month'],timestamp['day'],timestamp['year']))

#display results, US Customary
#print('US Customary:')
#print('Temperature: %d°F' % temperatureF)
#print('Dewpoint: %d°F' % dewpointF)
#print('Wind speed: %d MPH' % windSpeedMPH)
#print('Wind gust: %d MPH' % windGustMPH)
#print('Station pressure: %.2f inHg' % barometricPressureHg)
#print("Density altitude: %d ft" % densityAltitudeFt)
#print('\n')

#display results, Metric
#print('Metric:')
#print('Temperature: %d°C' % temperature)
#print('Dewpoint: %d°C' % dewpoint)
#print('Wind speed: %d KPH' % windSpeedKPH)
#print('Wind gust: %d KPH' % windGustKPH)
#print('Station pressure: %.1f hPa' % barometricPressure)
#print("Density altitude: %d m" % densityAltitudeM)
#print('\n')

#simplify to display text
outputUSC = "%d°F, %s %d G %d mph, %d ft DA" % (temperatureF, windDirectionStr, windSpeedMPH, windGustMPH, densityAltitudeFt)
outputMetric = "%d°C, %s %d G %d kph, %d m DA" % (temperature, windDirectionStr, windSpeedKPH, windGustKPH, densityAltitudeM)
print(StationID)
print('US Customary:',outputUSC)
print('Metric:',outputMetric)
print(updateTime)
print(timeOffset)
print("Uploading...")

#MySQL DB setup