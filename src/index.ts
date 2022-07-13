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
app.get('/', (req, res) => {
  res.send(__dirname);
});

app.post('/addlayerosm', (req, res) => {
  var qgis_project_name = req.body.qgis_project_name;
  var path_qgis = req.body.path_qgis;
  var gpkg_path = req.body.gpkg_path;
  var geometry = req.body.geometry;
  var identifiant = req.body.identifiant;
  var path_logo = req.body.path_logo;
  var color = req.body.color;
  var path_qml = req.body.path_qml;
  addLayerOsm(
    qgis_project_name,
    path_qgis,
    gpkg_path,
    geometry,
    identifiant,
    path_logo,
    color,
    path_qml,
    function (err, result) {
      if (err) {
        res.send({ "status": false, "message": "echec de l'ajout de la couche", "error": err });
      } else {
        fs.unlink(gpkg_path, (err) => {
          if (err) {
            res.send({ "status": false, "message": "echec de suppression de la source", "error": err });
          } else {
             res.send({
               status: true,
               message: 'couche ajoutée',
               layer: JSON.parse(result[0])
             });
          }
        })
       
      }
    }
  );

});

app.post('/addotherlayer', (req, res) => {
  var qgis_project_name = req.body.qgis_project_name;
  var path_qgis = req.body.path_qgis;
  var path_data = req.body.path_data;
  var geometry = req.body.geometry;
  var identifiant = req.body.identifiant;
  var path_logo = req.body.path_logo;
  var color = req.body.color;
  var path_qml = req.body.path_qml;
  addOtherLayer(
    qgis_project_name,
    path_qgis,
    path_data,
    geometry,
    identifiant,
    path_logo,
    color,
    path_qml,
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
    }
  );
});

app.post('/creategpkg', (req, res) => {
  var sql = req.body.sql;
  var instance = req.body.instance;
  var couche_name = req.body.couche_name;
  var couche_id = req.body.couche_id;

 var qgis_project_name = req.body.qgis_project_name;
 var path_qgis = req.body.path_qgis;
 var geometry = req.body.geometry;
 var identifiant = req.body.identifiant;
 var path_logo = req.body.path_logo;
 var color = req.body.color;
 var path_qml = req.body.path_qml;

  create_gpkg(sql, instance, couche_name, couche_id, function (err, data) {
    if (err) {
      console.log(err);
      res.send({ "status": false, "message": "echec de la création du gpkg", "error": err });
    } else {
       var save_path =
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
        path_logo,
        color,
        path_qml,
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
        }
      );
    }
  }
  );
});


app.listen(port, () => {
  return console.log(`server is listening on ${port}`);
});
