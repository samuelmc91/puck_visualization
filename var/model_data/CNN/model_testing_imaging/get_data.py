import pandas as pd
import os

base_dir = os.getcwd()
graphs = os.path.join(base_dir, 'graphs')

export_file = os.path.join(graphs, 'export_file.txt')
key_words = ['Run', 'First Conv Layer', 'Second Conv Layer', 'Third Conv Layer', 'Accuracy', 'Validation Accuracy', 'Loss', 'Validation Loss']

with open(export_file, 'r') as f:
    run_list = []
    for line in f:
        run_list.append(line[:-1])

run_list = [run.split(',') for run in run_list]

run_numbers = []

for runs in run_list:
    inner_numbers = []
    for inner_run in runs:
        inner_run = inner_run.split(':')[1]
        inner_numbers.append(inner_run)
    run_numbers.append(inner_numbers)

run_df = pd.DataFrame(run_numbers, columns=key_words)

print(run_df[run_df['Accuracy'] == run_df['Accuracy'].max()])
print(run_df.detail())