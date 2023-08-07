import sys
from pathlib import Path
import re
import shutil

files_groups = {
'images' : ['JPEG', 'PNG', 'JPG', 'SVG'],
'video' : ['AVI', 'MP4', 'MOV', 'MKV'],
'documents' : ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
'audio' : ['MP3', 'OGG', 'WAV', 'AMR'],
'archives' : ['ZIP', 'GZ', 'TAR']}

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "zh", "z", "y", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

trans = {}
known_ext_list = []
unknown_ext_list = []
#ignore_list = ['archives', 'video', 'audio', 'documents', 'images']
ignore_list = []

def normalize(f_name):
    f_new = f_name.translate(trans)
    f_new = re.sub('[^a-zA-z0-9]', '_', f_new)
    return f_new

def rename_f(path):
    f_oldname = path.name
    if path.is_file():
        f_newname = normalize(path.stem) + path.suffix
    elif path.is_dir():
        f_newname = normalize(path.name)
    else:
        f_newname = path.name
    try:
        if f_oldname != f_newname:
            return path.rename(path.parent  /  f_newname)
    except:
        print(f'Can\'t rename file: "{f_oldname}"')
    return path

# Створюємо кінцеві папки якшо їх немає
def create_dirs(path):
    for dir_name in ignore_list:
        p = Path(path / dir_name)
        if p.exists():
            continue
        p.mkdir()

# Видаляємо пусті папки
def delete_empty_dirs(path):
    for p in path.iterdir():
        if p.name in ignore_list:
            continue
        if p.is_dir():
            delete_empty_dirs(p)
            try:
                p.rmdir()
            except:
                pass

# Функція розпаковує архів
def unpack_archives():
    path_archives = Path(global_path / 'archives')
    for path in path_archives.iterdir():
        if path.is_file():
            p = Path(global_path / 'archives' / path.stem )
            try:
                p.mkdir()
                shutil.unpack_archive(path, p)
            except:
                print(f'Folder "{p.name}" already exists!')
        
    
# Основна функція сортування
def sort_files(path):
    for p in path.iterdir():
        if p.is_dir() and p.name in ignore_list:
            continue
        if p.is_dir():
            sort_files(rename_f(p))
        else:
            if p.suffix.upper()[1:] in known_ext.keys():
                known_ext_list.append(p.suffix.upper()[1:])
                p_type = known_ext[p.suffix.upper()[1:]]
                p_new = rename_f(p)
                try:
                    p_new.rename(global_path / p_type / p_new.name)
                except:
                    print(f'Can\'t move file "{p_new.name}"')
            else:
                unknown_ext_list.append(p.suffix.upper()[1:])

        
# Підготовка набору символів транслітерації
for cyr, lat in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    trans[ord(cyr)] = lat
    trans[ord(cyr.upper())] = lat.upper()

# Підготовка списку відомих розширень файлів
known_ext = {}
for f_type, f_extentions in files_groups.items():
    for f_extention in f_extentions:
        known_ext[f_extention] = f_type

# Формуємо перелік папок для створення
for el in files_groups.keys():
    ignore_list.append(el)

if __name__ == "__main__":
    print('---Script start working---')
    try:     
        path_str = sys.argv[1]
        global_path = Path(path_str)
    except:
        print('Path parametr not found')

    if global_path.exists():
        create_dirs(global_path)
        sort_files(global_path)
        unpack_archives()
        delete_empty_dirs(global_path)
    else:
        print(f'Path not found {path_str}')
    print('---Script stop working---')
