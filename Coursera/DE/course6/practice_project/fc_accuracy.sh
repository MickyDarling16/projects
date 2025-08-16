#######         Scenario: Assume current date is 2023-04-15. This script will be run            #######
#######         to fetch the observed and forecasted temperatures that were logged in           #######
#######         rx_poc4.log for 2023-03-15 and then it will calculate how                       #######
#######         accurate the logged observed and forecasted temperatures for 2023-03-15 were.   #######
#######         And then it will log the accuracy in a file named historical_fc_accuracy.tsv    #######
#######         while weather1.sh fetches the weather report for                                #######
#######         Casablanca, Morocco, for 2023-04-15.                                            #######

#!/bin/bash
echo -e "year\tmonth\tday\tobs_temp\tfc_temp_accuracy\taccuracy_range" > historical_fc_accuracy.tsv

# Read the number of rows in rx_poc4.log
# Exclude the header row
num_rows=$(wc -l < rx_poc4.log)
num_rows=$((num_rows - 1))  # Exclude header row
echo -e "Number of rows in rx_poc4.log: $num_rows"

while [ $num_rows -ne 0 ]; do
    row=$(tail -n $num_rows rx_poc4.log | head -n 1)
    echo -e "Current row: $row"

    num_rows=$((num_rows-1))

    year=$(gawk -F '\t' '{print $1}' <<< $row)
    month=$(gawk -F '\t' '{print $2}' <<< $row)
    day=$(gawk -F '\t' '{print $3}' <<< $row)
    # Get the observed temperature from the tab separated file
    obs_temp=$(gawk -F '\t' '{print $4}' <<< $row)

    # Get the forecasted temperature from the tab separated file
    fc_temp=$(gawk -F '\t' '{print $5}' <<< $row)
    echo -e "year: $year, month: $month, day: $day, obs_temp: $obs_temp, fc_temp: $fc_temp"

    # Calculate the forecast accuracy
    fc_accuracy=$((fc_temp-obs_temp))
    echo -e "Accuracy of forecast for $year-$month-$day is $fc_accuracy"

    if [ $fc_accuracy -eq 1 ] || [ $fc_accuracy -eq -1 ]; then
        accuracy_range='Excellent'
    elif [ $fc_accuracy -eq 2 ] || [ $fc_accuracy -eq -2 ]; then
        accuracy_range='Good'
    elif [ $fc_accuracy -eq 3 ] || [ $fc_accuracy -eq -3 ]; then
        accuracy_range='Fair'
    else
        accuracy_range='Poor'
    fi


    # Log the observed and forecasted temperatures
    echo -e "$year\t$month\t$day\t$obs_temp\t$fc_accuracy\t$accuracy_range" >> historical_fc_accuracy.tsv


done