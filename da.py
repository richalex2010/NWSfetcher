#reference: https://www.weather.gov/media/epz/wxcalc/densityAltitude.pdf

#units in °C and hPa/mb
temperature = 0
dewpoint = -1
barometricPressure = 994.30

#conversions
airTemperature = temperature + 273.15
barometricPressureHg = 0.02952998751 * barometricPressure

#calculate vapor pressure
vaporPressure = 6.11 * (10 ** ((7.5 * dewpoint)/(237.7 + dewpoint)))
print("Vapor pressure:",vaporPressure)

#calculate virtual temperature
virtualTemperature = (airTemperature / (1 - ((vaporPressure / barometricPressure) * (0.378))))
print("Virtual temperature (K):",virtualTemperature)

#convert virtual temperature to Rankine
virtualTemperature = virtualTemperature * (9 / 5)
print("Virtual temperature (°R):",virtualTemperature)

#calculate density altitude
densityAltitudeFt = 145366 * (1 - (((17.326 * barometricPressureHg) / virtualTemperature) ** 0.235))

#convert to metric
densityAltitudeM = densityAltitudeFt * 0.3048

#convert to readable format and print
densityAltitudeFt = int(round(densityAltitudeFt))
densityAltitudeM = int(round(densityAltitudeM))
print("Density altitude (ft):",densityAltitudeFt)
print("Density altitude (m):",densityAltitudeM)