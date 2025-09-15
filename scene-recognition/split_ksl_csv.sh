#!/bin/bash

# Usage: ./split_csv.sh input.csv output_dir
input="$1"
outdir="$2"

if [ -z "$input" ] || [ -z "$outdir" ]; then
    echo "Usage: $0 input.csv output_dir"
    exit 1
fi

mkdir -p "$outdir"
header=$(head -n 1 "$input")

# Remove any previous split files in the output directory
find "$outdir" -type f -name '*.csv' -delete

# Collect all lines and split by source_id
tail -n +2 "$input" | while IFS= read -r line || [ -n "$line" ]; do
    first_col=$(echo "$line" | cut -d',' -f1)
    second_col=$(echo "$line" | cut -d',' -f2)
    source_id=$(echo "$first_col" | cut -d'_' -f1 | cut -c2-)
    echo $source_id found
    if [ "$second_col" = "false" ]; then
        echo "skipping unseen image $first_col"
    else
        out="$outdir/${source_id}.csv.tmp"
        echo "$line" >> "$out"
    fi
done

# For each split file, sort rows and add header
for tmpfile in "$outdir"/*.csv.tmp; do
    outfile="${tmpfile%.tmp}"
    echo "$header" > "$outfile"
    sort "$tmpfile" >> "$outfile"
    rm "$tmpfile"
done

