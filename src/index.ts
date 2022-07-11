import express from 'express';
import { addLayerOsm, addOtherLayer } from './functions/add_layer';
import { create_gpkg } from './functions/create_gpkg';

const app = express();
import bodyParser from 'body-parser';
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
const port = 3000;
app.get('/', (req, res) => {
  res.send('Welcome To My Qgis Project');
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
        res.send({ "status": true, "message": "couche ajoutée", "layer": result[0] });
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
        res.send({ status: true, message: 'couche ajoutée', layer: result[0] });
      }
    }
  );
});

app.post('/creategpkg', (req, res) => {
  var sql = req.body.sql;
  var instance = req.body.instance;
  var thematique_name = req.body.thematique_name;
  var thematique_id = req.body.thematique_id;

  create_gpkg(sql, instance, thematique_name, thematique_id, function (err, data) {
    if (err) {
      res.send({ "status": false, "message": "echec de la création du gpkg", "error": err });
    } else {
      res.send({ "status": true, "message": "gpkg créé", "gpkg": data });
    }
  }
  );
});


app.listen(port, () => {
  return console.log(`server is listening on ${port}`);
});
