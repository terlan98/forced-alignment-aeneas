import os
import sys
import argparse
import re
from aeneas.executetask import ExecuteTask
from aeneas.task import Task

DELIMITERS = ['.', '!', '?', ':']

def executeAeneas(text_path, audio_path):
	audio_name, _ = os.path.splitext(audio_path)

	# create Task object
	config_string = u'task_language=tur|is_text_type=plain|os_task_file_format=json'
	task = Task(config_string=config_string)
	task.audio_file_path_absolute = audio_path
	task.text_file_path_absolute = text_path
	task.sync_map_file_path_absolute = audio_name + "_syncmap.json"

	# process Task
	ExecuteTask(task).execute()

	# output sync map to file
	task.output_sync_map_file()

def clean_text(file_path):
    file_name, _ = os.path.splitext(file_path)

    with open(file_path, encoding='utf-8') as file:
        contents = ''.join(file.read().splitlines())
        contents = contents.replace('- ', '').replace('– ', '')

    for delimiter in DELIMITERS:
        contents = contents.replace(delimiter, delimiter + '\n')

    new_contents = ''
    cleaned_file_path = file_name + '_plain.txt'

    for line in contents.splitlines():
        if line != '.':
            new_contents += line.strip() + '\n'

    with open(cleaned_file_path, 'w', encoding='utf-8') as file:
        file.write(new_contents)

    return cleaned_file_path

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('textPath', help='Path to the txt file')
    parser.add_argument('audioPath', help='Path to the mp3 file')
    args = parser.parse_args()

    text_path = args.textPath
    audio_path = args.audioPath
    new_text_path = clean_text(text_path)
    executeAeneas(new_text_path, audio_path)



