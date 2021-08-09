#!/usr/bin/python
import logging, os, traceback
from subprocess import Popen, PIPE
import pysftp, json




local_content_path = '/opt/content/rsync/'

logging.basicConfig(filename='/opt/scripts/sync_content/inc_sync.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

if os.path.exists("/tmp/inc_sync_content_py_flag"):
    logging.debug('sync already running')
    exit(0)

os.mknod("/tmp/inc_sync_content_py_flag")

with open('marketplace.json', 'r', encoding='utf-8') as fh:
    projects = json.load(fh)

logging.debug('-' * 20)


def to_remove():
    logging.debug("Removing synced files...")
    f = open('/tmp/prepare_for_del', 'r')
    for file in f:
        try:
            logging.debug("deleting file: %s" % file)
            os.remove(file)
        except:
            logging.debug("Couldn't delete %s" % file)
            traceback.print_exc()

def sync_func(local_content_path, ip, remote_content_path, mp3_full, id_marketplace, project):
    source_path = os.path.join(local_content_path, str(id_marketplace))

    try:
        list_files = os.listdir(source_path)  #Записываем Список файлов перед синхрой, что бы не удалить файлы
        #чудом попавшие в момент синхронизации Далее синхронизация
        sftp = pysftp.Connection(ip, username='root', private_key='/root/.ssh/id_rsa')
        sftp.put_r(source_path, remote_content_path, preserve_mtime=True)
        sftp.close()
        f = open('/tmp/prepare_for_del', 'w') # открываем файл и записываем в файл список файлов на удаление
        for each in list_files:
            f.write(each + '\n')
        f.close()

    except:
        logging.debug('Error syncing files')
        traceback.print_exc()


to_remove() # Вызов Функции удаление вначале скрипта. Удалит файлы которые синкнулись. Что бы еще раз на них не вызавать синк.

for project in projects:
    if projects[project]['enabled']:
        logging.debug('-' * 20)
        logging.debug('Project: %s' % project)
        print('Project: %s' % project)
        sync_func(local_content_path,
                  projects[project]['ip'],
                  projects[project]['remote_content_path'],
                  projects[project]['mp3_full'],
                  projects[project]['id_marketplace'],
                  project
                  )

to_remove()
os.remove("/tmp/inc_sync_content_py_flag")