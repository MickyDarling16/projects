# !/bin/bash

# Get the last 7 accuracy values from the synthetic_historical_fc_accuracy.tsv file
echo $(tail -7 synthetic_historical_fc_accuracy.tsv | gawk '{print $6}') > scratch.txt

accuracy_history_array=($(echo $(cat scratch.txt)))
# echo ${accuracy_history_array[1]}

# echo "Original array: ${accuracy_history_array[@]}"
for i in "${!accuracy_history_array[@]}"; do

  if [ "${accuracy_history_array[$i]}" -lt 0 ]; then
    # Convert negative values to positive
    current_value=${accuracy_history_array[$i]}
    accuracy_history_array[$i]=$((current_value * -1))
    echo "Converted negative value to positive: ${accuracy_history_array[$i]}"
  fi
done
echo "Accuracy History: ${accuracy_history_array[@]}"



# Initialize maximum and minimum values
maximum=${accuracy_history_array[0]}
minimum=${accuracy_history_array[0]}

# Loop through the accuracy values to find the maximum and minimum
for i in "${accuracy_history_array[@]}"; do
  if [ $i -gt $maximum ]; then
    maximum=$i

  elif [ $i -lt $minimum ]; then
    minimum=$i
  fi
done

echo "Maximum: $maximum"
echo "Minimum: $minimum"