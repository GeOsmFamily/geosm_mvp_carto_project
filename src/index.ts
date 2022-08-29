import express from 'express';
import { addLayerOsm, addOtherLayer } from './functions/add_layer';
import { create_gpkg } from './functions/create_gpkg';
import db from '../env.json';
import fs from 'fs';

const app = express();
import bodyParser from 'body-parser';
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
const port = 3000;
app.get('/', (_req, res) => {
  res.send(__dirname);
});

app.post('/addlayerosm', (req, res) => {
  let qgis_project_name = req.body.qgis_project_name;
  let path_qgis = req.body.path_qgis;
  let gpkg_path = req.body.gpkg_path;
  let geometry = req.body.geometry;
  let identifiant = req.body.identifiant;
  let path_logo = req.body.path_logo;
  let color = req.body.color;
  let path_qml = req.body.path_qml;
  addLayerOsm(
    qgis_project_name,
    path_qgis,
    gpkg_path,
    geometry,
    identifiant,

    function (err, result) {
      if (err) {
        res.send({
          status: false,
          message: "echec de l'ajout de la couche",
          error: err
        });
      } else {
        fs.unlink(gpkg_path, (err1) => {
          if (err1) {
            res.send({
              status: false,
              message: 'echec de suppression de la source',
              error: err1
            });
          } else {
            res.send({
              status: true,
              message: 'couche ajoutée',
              layer: JSON.parse(result[0])
            });
          }
        });
      }
    },
    path_logo,
    color,
    path_qml
  );

});

app.post('/addotherlayer', (req, res) => {
  let qgis_project_name = req.body.qgis_project_name;
  let path_qgis = req.body.path_qgis;
  let path_data = req.body.path_data;
  let geometry = req.body.geometry;
  let identifiant = req.body.identifiant;
  let path_logo = req.body.path_logo;
  let color = req.body.color;
  let path_qml = req.body.path_qml;
  addOtherLayer(
    qgis_project_name,
    path_qgis,
    path_data,
    geometry,
    identifiant,

    function (err, result) {
      if (err) {
        res.send({
          status: false,
          message: "echec de l'ajout de la couche",
          error: err
        });
      } else {
        res.send({
          status: true,
          message: 'couche ajoutée',
          layer: JSON.parse(result[0])
        });
      }
    },
    path_logo,
    color,
    path_qml
  );
});

app.post('/creategpkg', (req, res) => {
  let sql = req.body.sql;
  let instance = req.body.instance;
  let couche_name = req.body.couche_name;
  let couche_id = req.body.couche_id;

 let qgis_project_name = req.body.qgis_project_name;
 let path_qgis = req.body.path_qgis;
 let geometry = req.body.geometry;
 let identifiant = req.body.identifiant;
 let path_logo = req.body.path_logo;
 let color = req.body.color;
 let path_qml = req.body.path_qml;

  create_gpkg(sql, instance, couche_name, couche_id, function (err, _data) {
    if (err) {
      console.log(err);
      res.send({ "status": false, "message": "echec de la création du gpkg", "error": err });
    } else {
       let save_path =
         '/var/www/html/src' +
         db.qgis['path'] +
         '/' +
         instance +
         '/' +
         couche_name +
         couche_id +
         '.gpkg';
      addLayerOsm(
        qgis_project_name,
        path_qgis,
        save_path,
        geometry,
        identifiant,

        function (err1, result) {
          if (err1) {
            console.log(err1);
            res.send({
              status: false,
              message: "echec de l'ajout de la couche",
              error: err1
            });
          } else {
            res.send({
              status: true,
              message: 'couche ajoutée',
              layer: JSON.parse(result[0])
            });
          }
        },
        path_logo,
        color,
        path_qml
      );
    }
  }
  );
});


app.listen(port, () => {
  return console.log(`server is listening on ${port}`);
});
