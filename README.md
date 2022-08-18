# GeOsm Carto

## Installation

```
$ git clone https://github.com/GeOsmFamily/geosm_mvp_carto_project.git
$ cd geosm_mvp_carto_project
$ docker-compose up -d
$ docker exec -it geosm_carto_mvp bash
$ cp env.example.json env.json
```

- Edit env.json to your needs
- Change host database to your Docker host
- To see your Docker host run

```
$ /sbin/ip route|awk '/default/ { print $3 }'
```

- Save env.json and continue

```
$ a2dissite 000-default.conf
$ a2ensite service.conf
$ service apache2 reload

$ chown www-data:www-data /var/www/html
$ chmod -R 777 /var/www/html/

$ cd /var/www/html/dist/src && forever start  -a --minUptime 5000  --spinSleepTime 5000 -l process.log -o out.log -e err.log index.js
```
