import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import parseResume
import updateAssistant
import createAssistants
import json

with open('config.json', 'r') as json_file:
    config = json.load(json_file)

class MyHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.new_files = []
        self.deleted_files = []

    def on_created(self, event):
        if not event.is_directory:
            self.new_files.append(event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            self.deleted_files.append(event.src_path)

def watch_directory(path):
    print("Starting watcher")
    if not os.listdir(config['file_watch_path']):
        print("Resumes not parsed! Parsing the resumes and creating the Assistants.....")
        parseResume.main(path)
        createAssistants.get_assistant_ids(config['file_watch_path'])
        
    else:
        event_handler = MyHandler()
        observer = Observer()
        observer.schedule(event_handler, path, recursive=True)
        observer.start()

        try:
            while True:
                # Process new files
                if event_handler.new_files:
                    print("New files added:")
                    print(event_handler.new_files)
                    assistant_updated = set()
                    for file_path in event_handler.new_files:
                        key = file_path.split("\\")[-1]
                        folder_name = file_path.split("\\")[-2]
                        print("------------------------------------------------------------------------")
                        output_path = config['file_watch_path'] + f"\\{folder_name}.json"
                        assistant_updated.add(output_path)
                        
                        with open(output_path, "r") as json_file:
                            contents = json.load(json_file)
                        if key.endswith('.pdf'):
                            print(f'Reading PDF: {file_path} added.')
                            contents[key] = parseResume.read_pdf(file_path)
                        elif key.endswith('.docx'):
                            print(f'Reading DOCX: {file_path} added.')
                            contents[key] = parseResume.read_docx(file_path)
                        elif key.endswith('.doc'):
                            print(f'Reading DOC: {file_path} added.')
                            contents[key] = parseResume.read_doc(file_path)
                        with open(output_path, 'w') as json_file:
                            json.dump(contents, json_file, indent=4, ensure_ascii=False)
                    print("All files added are processed!") 
                    print("Updating the assistant now!")
                    updateAssistant.update_assistant(list(assistant_updated))
                    event_handler.new_files=[]
                # Process deleted files
                if event_handler.deleted_files:
                    print("Files deleted:")
                    print(event_handler.deleted_files)
                    assistant_updated = set()

                    for file_path in event_handler.deleted_files:
                        key = file_path.split("\\")[-1]
                        folder_name = file_path.split("\\")[-2]
                        output_path = config['file_watch_path'] + f"\\{folder_name}.json"
                        assistant_updated.add(output_path)
                        print(output_path)
                        with open(output_path, "r") as json_file:
                            contents = json.load(json_file)
                        del contents[key]
                        with open(output_path, 'w') as json_file:
                            json.dump(contents, json_file, indent=4, ensure_ascii=False)
                    print("All files deleted are processed!") 
                    print("Updating the assistant now!")
                    updateAssistant.update_assistant(list(assistant_updated))
                    event_handler.deleted_files = []

                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()


def run_watcher(path):
    watch_directory(path)

#run_watcher()
