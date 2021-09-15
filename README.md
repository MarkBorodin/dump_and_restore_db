# INSTALL

### Setup

clone repository:
```
git clone git@github.com:MarkBorodin/dump_and_restore_db.git
```
move to folder:
```
cd dump_and_restore_db
```

install requirements:

```
pip install -r requirements.txt
```

To run the mautik, you need to run:
```
docker-compose up
```
After the initial setup and work in mautik, you can do a dump:
```
python get_dump.py
```
(file "dump.sql" and folder "files" will be created)
After that, on the new software, you need to do:
```
docker-compose up
python mautic_config.py
python restore.py
```
(file "dump.sql" and folder "files" must be in the directory with executable files)

### Finish
