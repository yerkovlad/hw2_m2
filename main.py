import platform
import time
import os
import shutil
import threading
from pathlib import Path

# Dictionary of file extensions for each file type
file_extensions = {
    'images': ['JPEG', 'PNG', 'JPG', 'SVG'],
    'documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
    'audio': ['MP3', 'OGG', 'WAV', 'AMR'],
    'video': ['AVI', 'MP4', 'MOV', 'MKV'],
    'archives': ['ZIP', 'GZ', 'TAR'],
    'unknown': '',
}


def sort_files(source_path, destination_path):
    source_directory = Path(source_path)
    
    for item in source_directory.iterdir():
        if item.is_file():
            file_extension = item.suffix

            for file_type, extensions in file_extensions.items():
                if file_extension[1:].upper() in extensions:
                    destination_directory = Path(destination_path) / file_type
                    destination_directory.mkdir(exist_ok=True)

                    shutil.move(item, destination_directory / item.name)
                    break
            else:
                destination_directory = Path(destination_path) / 'unknown'
                destination_directory.mkdir(exist_ok=True)
                shutil.move(item, destination_directory / item.name)


def process_directory(source_path, destination_path):
    sort_files(source_path, destination_path)


def delete_empty_folders(directory):
    for item in directory.iterdir():
        if item.is_dir():
            delete_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                continue


def main():
    while True:
        print("1. Сортувати каталог")
        print("2. Вихід")
        choice = input("Введіть значення для вибору ")
        if choice == "1":
            source_path = input('Введіть повний шлях до вашого каталогу ')

            if platform.system() == "Windows":
                if len(source_path.split(":")[0]) > 1:
                    current_directory = Path.cwd()
                    source_path = current_directory / source_path

            source_directory = Path(source_path)
            if source_directory.exists() and source_directory.is_dir():
                print(f"Каталог '{source_path}' існує.")
                for file_type in file_extensions.keys():
                    destination_directory = source_directory / file_type
                    destination_directory.mkdir(exist_ok=True)

                threads = []
                for item in source_directory.iterdir():
                    if item.is_dir():
                        t = threading.Thread(target=process_directory, args=(str(item), str(source_path)))
                        threads.append(t)
                        t.start()

                for t in threads:
                    t.join()

                delete_empty_folders(source_directory)
                print("Сортування завершено!")

            else:
                print(f"Каталог '{source_path}' не існує або це не каталог.")
        elif choice == "2":
            os.system('cls')
            break
        else:
            print('Некоректний вибір, спробуйте ще раз')
            time.sleep(2)
            os.system('cls')


if __name__ == '__main__':
    main()
