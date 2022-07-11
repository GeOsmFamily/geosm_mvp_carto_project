import { PythonShell } from 'python-shell';
var result: any;
function addLayerOsm(
  qgis_project_name: string,
  path_qgis: string,
  gpkg_path: string,
  geometry: string,
  identifiant: string,
  path_logo: string = null,
  color: string = null,
  path_qml: string = null,
  cb: (err:any, result: any) => void
) {
  if (color !== null) {
    PythonShell.run(
      'add_layer.py',
      {
        mode: 'text',
        pythonPath: 'python3',
        pythonOptions: ['-u'],
        scriptPath: 'src/scripts',
        args: [
          qgis_project_name,
          path_qgis,
          gpkg_path,
          geometry,
          identifiant,
          path_logo,
          color
        ]
      },
      cb
    );
  } else {
    PythonShell.run(
      'add_layer.py',
      {
        mode: 'text',
        pythonPath: 'python3',
        pythonOptions: ['-u'],
        scriptPath: 'src/scripts',
        args: [
          qgis_project_name,
          path_qgis,
          gpkg_path,
          geometry,
          identifiant,
          path_qml
        ]
      },
      cb
    );
  }
}

function addOtherLayer(
  qgis_project_name: string,
  path_qgis: string,
  path_data: string,
  geometry: string,
  identifiant: string,
  path_logo: string = null,
  color: string = null,
  path_qml: string = null,
  cb: (err:any, result: any) => void
) {
  if (color !== null) {
    PythonShell.run(
      'add_layer.py',
      {
        mode: 'text',
        pythonPath: 'python3',
        pythonOptions: ['-u'],
        scriptPath: 'src/scripts',
        args: [
          qgis_project_name,
          path_qgis,
          path_data,
          geometry,
          identifiant,
          path_logo,
          color
        ]
      },
      cb
    );
  } else {
    PythonShell.run(
      'add_layer.py',
      {
        mode: 'text',
        pythonPath: 'python3',
        pythonOptions: ['-u'],
        scriptPath: 'src/scripts',
        args: [
          qgis_project_name,
          path_qgis,
          path_data,
          geometry,
          identifiant,
          path_qml
        ]
      },
      cb
    );
  }
}

export { addLayerOsm, addOtherLayer };
