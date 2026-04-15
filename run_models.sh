#!/bin/bash

# Find all YAML files recursively inside experiments that contain "dino" or "labnet"
# configs=($(grep -rlE 'labnet' experiments --include="*.yaml"))

# get all experiments over experiments/best_models
# configs=($(find experiments/best_models -type f -name "*.yaml" ))

configs=(
"experiments/vit_small_baseline.yaml"
)

for config in "${configs[@]}"; do
    echo "Found matching config: $config"
done

output_prefix="log"
i=1

for config in "${configs[@]}"; do
    output_file="${output_prefix}_${i}.txt"
    echo "In progress: $config > $output_file"

    nohup python3 main.py --config "$config" > "$output_file" 2>&1

    echo "Finished: $config"
    ((i++))
done

echo "All models have been run sequentially."
