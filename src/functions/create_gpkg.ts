import db from '../../env.json'
import ogr2ogr from 'ogr2ogr';

function create_gpkg(
  sql: string,
  instance: string,
  thematique_name: string,
    thematique_id: string,
  cb: (err: any, data: any) => void
) {
  var save_path =
    '/var/www/html/src' +
    db.qgis['path'] +
    '/' +
    instance +
    '/' +
    thematique_name +
    thematique_id +
    '.gpkg';

   ogr2ogr(
    'PG:host=' +
      db.database_osm['host'] +
      ' port=' +
      db.database_osm['port'] +
      ' dbname=' +
      db.database_osm['dbname'] +
      ' user=' +
      db.database_osm['user'] +
      ' password=' +
      db.database_osm['password'],
    {
        format: 'GPKG',
        destination: save_path,
      timeout: 1800000,
      options: [
        "--config",
        "CPL_DEBUG",
        "ON",
        "-sql",
        sql ,
        "-t_srs",
          'EPSG:4326',
      ]
    }
  ).exec(cb);
}

export { create_gpkg };