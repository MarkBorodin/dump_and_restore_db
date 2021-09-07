import os

import mysql.connector


class MauticConfig(object):

    """Class for initial configuration of mautic
        - The data will be taken from the local.php file, which must be filled in and located from the current directory.
        - local.php will be copied to app / config.
        - Mautic will be installed
        - An admin will be created with the password "madmin" and an email from local.php as a login"""

    d = dict()
    cursor = ''
    cnx = ''
    container_name = 'automationmonkey_latest'
    path = os.path.dirname(os.path.abspath(__file__))

    def copy_local_file(self):
        """remove old file local.php, copy new local.php and rights to the new file local.php"""

        # remove old file "local.php" removed from app/config
        os.system(f'docker exec {self.container_name} rm /var/www/html/app/config/local.php')
        print('old file "local.php" removed from app/config')

        # copy new file "local.php" to app/config
        os.system(f'docker cp {self.path}/local.php {self.container_name}:/var/www/html/app/config/local.php')
        print('new file "local.php" copied to app/config')

        # all rights to the new file "local.php"
        os.system(f'docker exec {self.container_name} bash -c "chmod 777 app/config/local.php"')
        print('all rights to the new file "local.php" are granted')

    def mautic_install_data(self):
        """install default mautic data"""
        print('start data installation...')
        os.system(f'docker exec {self.container_name} bash -c "php bin/console mautic:install:data --force"')

    def get_data_from_local_file(self):
        """get data from local.php file. File should be in the current directory"""
        with open('local.php', 'r') as f:
            text = f.readlines()[2:-1]
            for i in text:
                try:
                    key, value = i.strip()[:-1].replace("'", "").split(' => ')
                    if key == 'mailer_from_name':
                        self.d["username"] = value
                        self.d["first_name"] = value.split(' ')[0]
                        self.d["last_name"] = value.split(' ')[1]
                    self.d[key] = value if value != 'null' else ''
                except Exception as e:
                    print(e)
                    continue

    def connect_db(self):
        """connect to database"""
        self.cnx = mysql.connector.connect(
            user=self.d["db_user"], password=self.d["db_password"],
            host=self.d["db_host"], database=self.d["db_name"], port=3308
        )
        self.cursor = self.cnx.cursor()

    def execute_queries(self, query_list: list):
        """execute queries"""
        for query in query_list:
            try:
                if type(query) == str:
                    self.cursor.execute(query)
                elif type(query) == tuple:
                    self.cursor.execute(query[0], query[1])
            except Exception as e:  # noqa
                print(e)
                continue

    def commit(self):
        """commit"""
        self.cnx.commit()

    def close_db(self):
        """close database"""
        self.cursor.close()
        self.cnx.close()


if __name__ == '__main__':
    # create object
    mautic_config = MauticConfig()
    # remove old local.php file and copy new
    mautic_config.copy_local_file()
    # install data
    mautic_config.mautic_install_data()

    """if you need to add something to the database, you can run next code"""

    """get data from local.php"""
    # mautic_config.get_data_from_local_file()
    # data = mautic_config.d

    """add sql query to the queries list. Queries list should be a list with:
    - sql command (type: string)
    or
    - sql command and parameters to it (type: list)"""
    # queries_list = [
    #     """DELETE FROM `users` WHERE `users`.`id` = 1""",
    #
    #     """DELETE FROM `users` WHERE `users`.`id` = 2""",
    #
    #     ("""INSERT INTO `users` (`id`, `role_id`, `is_published`, `date_added`, `created_by`, `created_by_user`,
    #     `date_modified`, `modified_by`, `modified_by_user`, `checked_out`, `checked_out_by`, `checked_out_by_user`,
    #      `username`, `password`, `first_name`, `last_name`, `email`, `position`, `timezone`, `locale`, `last_login`,
    #      `last_active`, `preferences`, `signature`)
    #     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
    #
    #      [1, 1, 1, None, None, None, None, None, None, None, None, None, data['username'],
    #      '$2y$13$VkE7UjFetqAM13oT4v/VYOfRCGrJ4hbr0zuwRZo6KVfDnNb16WFwy', data['first_name'], data['last_name'],
    #      data['mailer_user'], None, None, None, None, None, 'a:0:{''}', None])
    # ]

    """connect to db, run queries, commit and close db"""
    # mautic_config.connect_db()
    # mautic_config.execute_queries(queries_list)
    # mautic_config.commit()
    # mautic_config.close_db()
