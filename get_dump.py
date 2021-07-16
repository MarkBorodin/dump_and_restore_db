#!/usr/bin/python
import os

# db container_name
db_container_name = 'mauticdb_test'

# container_name
container_name = 'automationmonkey_latest'

# database name
db_name = 'mautic'

# user name
user = 'root'

# password
password = 'mysecret'

# path to the folder with the script
path = os.path.dirname(os.path.abspath(__file__))

# dump file name
dump_name = '/dump.sql'


# this function takes the specified parameters and generates a dump command
def get_dump(db_container_name, db_name, user, password, path, dump_name):
    script = f'docker exec -i {db_container_name} mysqldump -u{user} -p{password} --databases {db_name} --skip-comments > {path}{dump_name}'  # noqa
    os.system(script)


def get_media(container_name, path):
    script = f'docker cp {container_name}:/var/www/html/media/files/ {path}'
    # script = f'docker cp {container_name}:/var/www/html/media/ {path}'
    os.system(script)


if __name__ == '__main__':
    get_dump(db_container_name, db_name, user, password, path, dump_name)
    get_media(container_name, path)
