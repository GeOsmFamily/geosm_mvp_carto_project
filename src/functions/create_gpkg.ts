import db from '../../env.json'
import ogr2ogr from 'ogr2ogr';

function create_gpkg(
  sql: string,
  instance: string,
  couche_name: string,
    couche_id: string,
  cb: (err: any, data: any) => void
) {
  let save_path =
    '/var/www/html/src' +
    db.qgis['path'] +
    '/' +
    instance +
    '/' +
    couche_name +
    couche_id +
    '.gpkg';

   ogr2ogr(
     'PG:host=' +
       //@ts-ignore
       db[instance].database_osm['host'] +
       ' port=' +
       //@ts-ignore
       db[instance].database_osm['port'] +
       ' dbname=' +
       //@ts-ignore
       db[instance].database_osm['dbname'] +
       ' user=' +
       //@ts-ignore
       db[instance].database_osm['user'] +
       ' password=' +
       //@ts-ignore
       db[instance].database_osm['password'],
     {
       format: 'GPKG',
       destination: save_path,
       timeout: 1800000,
       options: [
         '--config',
         'CPL_DEBUG',
         'ON',
         '-sql',
         sql,
         '-t_srs',
         'EPSG:4326'
       ]
     }
   ).exec(cb);
}

export { create_gpkg };