import os


# db container name (I used database via Docker)
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
dump_name = 'dump.sql'

# path to the folder with the script + '/files/.'
dump_path = os.path.dirname(os.path.abspath(__file__)) + '/files/.'


# this function takes the specified parameters and generates a command to download the dump
def restore(db_container_name, db_name, user, password, dump_name):
    script = f'docker exec -i {db_container_name} mysql -u{user} -p{password} {db_name} < {dump_name}'
    os.system(script)


def load_media(dump_path, container_name):
    script = f'docker cp {dump_path} {container_name}:/var/www/html/media/files/'
    os.system(script)


def remove_tmp(container_name):
    rm_tmp = f'docker exec {container_name} rm -rf /var/www/html/media/files/tmp'
    os.system(rm_tmp)


if __name__ == '__main__':
    restore(db_container_name, db_name, user, password, dump_name)
    load_media(dump_path, container_name)
    remove_tmp(container_name)
    print('restore: completed successfully')
