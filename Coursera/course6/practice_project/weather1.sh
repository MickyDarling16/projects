#! /bin/bash
# This script fetches the weather report for Casablanca, Morocco,
# extracts the observed and forecasted temperatures for noon UTC,
# and logs the information in a file named rx_poc4.log.

#######         Scenario: Assume current date is 2023-03-15. This script will be run            #######
#######         to fetch the weather report for Casablanca for 2023-03-15.                      #######
#######         And then it will log the observed and forecasted temperatures for 2023-03-15.   #######




# Assign city name as Casablanca
city=Casablanca

# Obtain the weather report for Casablanca
curl -s wttr.in/$city?T --output weather_report

# To extract observed temperature for the current day (assuming for noon)
obs_temp=$(curl -s wttr.in/$city?T | head -4 | grep -m 1 -Eoe '-?[[:digit:]]+')
echo -e "The observed temperature for noon today for $city: $obs_temp"

# To extract the forecasted temperature for noon the current day
fc_temp=$(curl -s wttr.in/$city?T | head -13 | tail -1 | gawk -F '°C' '{print $2}' | grep -Eoe '-?[[:digit:]].*' | gawk -F '(' '{print $1}')
echo -e "The forecasted temperature for noon today for $city: $fc_temp"

# Assign Country and City to variable TZ
TZ='Morocco/Casablanca'


# Use command substitution to store the current day, month, and year in corresponding shell variables:
day=$(TZ='Morocco/Casablanca' date -u +%d)
month=$(TZ='Morocco/Casablanca' date +%m)
year=$(TZ='Morocco/Casablanca' date +%Y)

# echo -e "year\tmonth\tday\tobs_temp\tfc_temp" > rx_poc4.log


# Log the weather
echo -e "$year\t$month\t$day\t$obs_temp\t$fc_temp" >> rx_poc4.log
