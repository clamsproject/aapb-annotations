'''
This script takes as input a directory containing VIA version 3 project files containing video annotations and
generates a CSV file with the following columns: video_filename, start_time, end_time, text
for each annotation in the project file.
'''
import argparse
import json
import csv
import os

if __name__ == '__main__':
    # Parse the input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', type=str, required=True,
                        help='Path to the directory containing the VIA project files')
    parser.add_argument('--output_path', type=str, required=True,
                        help='Path to the output CSV file')
    args = parser.parse_args()

    # Loop through each file in the input directory and process it
    csv_data = []
    for filename in os.listdir(args.input_path):
        if filename.endswith('.json'):
            # Load the VIA project file
            with open(os.path.join(args.input_path, filename), 'r') as f:
                data = json.load(f)

            # Loop through each annotation in the VIA project file, if it contains 2 z values, add it to a dictionary
            # with the key being the first z value and the value being the second z value
            z_dict = {}
            for annotation_id, annotation_data in data['metadata'].items():
                if 'z' in annotation_data and len(annotation_data['z']) == 2:
                    z_dict[annotation_data['z'][0]] = annotation_data['z'][1]

            # Loop through each annotation in the VIA project file, if it contains 1 z value, find the lowest key in the z_dict
            # that is less than the z value of the annotation if the value of that key is greater than the z value for the annotation
            # use the key as the start time and the value as the end time
            # add a row to the csv_data list with the video filename, start time, end time, and text
            for annotation_id, annotation_data in data['metadata'].items():
                # lookup video filename in data["file"] based on annotation_data[vid]
                video_filename = data["file"][annotation_data["vid"]]["fname"]
                if 'z' in annotation_data and len(annotation_data['z']) == 1:
                    z_value = annotation_data['z'][0]
                    start_time = max([key for key in z_dict.keys() if key < z_value])
                    end_time = z_dict[start_time]
                    if end_time > z_value:
                        try:
                            csv_data.append([video_filename, start_time, end_time, annotation_data['av']["text-boxes"]])
                        except KeyError as e:
                            print (e)
                            print (annotation_data)

    # Write the CSV file, text value may contain new lines
    with open(args.output_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['video_filename', 'start_time', 'end_time', 'text'])
        for row in csv_data:
            # escape new lines in final value of row
            row[-1] = row[-1].replace('\n', '\\n')
            writer.writerow(row)

