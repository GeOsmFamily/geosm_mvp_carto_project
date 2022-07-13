#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 17:02:01 2022

@author: ntt
"""

from qgis.core import *
import os
import sys
import zipfile
import shutil
import os.path
import json
from osgeo import ogr
import base64
from PyQt5 import QtGui
from qgis.core import QgsVectorFileWriter
from PIL import ImageColor


def create_directory(parent_dir, directory):
    path = os.path.join(parent_dir, directory)


def getLayerGeometry(layer, feature_name):

    features = layer.getFeatures()

    for feature in features:

        # retrieve every feature with its geometry and attributes

        #print("Feature ID: ", feature.id())

        # fetch geometry

        # show some information about the feature geometry

        geom = feature.geometry()

        geomSingleType = QgsWkbTypes.isSingleType(geom.wkbType())

        if geom.type() == QgsWkbTypes.PointGeometry:

            # the geometry type can be of single or multi type

            if geomSingleType:

                x = geom.asPoint()

                return "Point"

            else:
                x = geom.asMultiPoint()

                return "MultiPoint"
            break

        elif geom.type() == QgsWkbTypes.LineGeometry:

            if geomSingleType:

                x = geom.asPolyline()

                #print("Line: ", x, "length: ", geom.length())
                return "Line"

            else:

                x = geom.asMultiPolyline()

                #print("MultiLine: ", x, "length: ", geom.length())
                return "MultiLine"
            break

        elif geom.type() == QgsWkbTypes.PolygonGeometry:

            if geomSingleType:

                x = geom.asPolygon()

                return "Polygon"
            else:

                x = geom.asMultiPolygon()

                return "MultiPolygon"
            break

        else:

            print("Unknown or invalid geometry")

            # fetch attributes

            attrs = feature.attributes()

            # attrs is a list. It contains all the attribute values of this feature

            print(attrs)

            # for this test only print the first feature

            break

# Point symbology


def setPointSymbology(layer, icone, couleur_remplissage):
    symbolLayer = QgsSvgMarkerSymbolLayer(icone, 10)

    # symbol = QgsSymbol.defaultSymbol(vlayer.geometryType())
    # symbol.changeSymbolLayer(0, symbolLayer)

    # class QgsPointClusterRenderer

    color = QtGui.QColor(couleur_remplissage)
    # create svg marker symbol for the input layer
    svgStyle = {
        "name": icone,
        "outline": "#000000",
        "size": "6",
    }
    svgLayer = QgsSvgMarkerSymbolLayer.create(svgStyle)
    svgSymbol = QgsMarkerSymbol()
    #svgSymbol.changeSymbolLayer(0, symbolLayer )
    svgSymbol.defaultSymbol(layer.geometryType())
    svgSymbol.setColor(color)
    svgSymbol.setSize(10)
    svgSymbol.appendSymbolLayer(svgLayer)

    #layer.renderer().symbol().changeSymbolLayer(0, symbolLayer )

    # instanciate a cluster rendering for input layer
    renderer = QgsPointClusterRenderer()
    # renderer.setOrderByEnabled(True)

    # set layer symboly
    layout_symbology = QgsSingleSymbolRenderer(svgSymbol)
    renderer.setEmbeddedRenderer(layout_symbology)

    # set @cluster_size variable for displaying cluster size
    exp = '@cluster_size'

    # get default layer symbology
    symbol = renderer.clusterSymbol().defaultSymbol(layer.geometryType())
    # set defaut layer symbology color
    symbol.setColor(color)
    # set defaut layer symbology size
    symbol.setSize(10)

    # set cluster symbology
    symbol_layer = QgsFontMarkerSymbolLayer()
    symbol_layer.setColor(QtGui.QColor('white'))

    symbol_layer.setFillColor(QtGui.QColor(color))
    symbol_layer.setFontStyle('Book')
    symbol_layer.setFontFamily('Book')
    symbol_layer.setSizeUnit(QgsUnitTypes.RenderPixels)
    symbol_layer.setEnabled(True)
    # active clusters size
    symbol_layer.setDataDefinedProperty(
        QgsSymbolLayer.PropertyCharacter, QgsProperty.fromExpression(exp, True))
    symbol_layer.setSize(10)
    # place all symbology together

    # 2cc0b1
    symbol_layer_inner = QgsSimpleMarkerSymbolLayer()
    color = QtGui.QColor('#2cc0b1')
    symbol_layer_inner.setColor(color)
    symbol_layer_inner.setSize(5.6)

    symbol.appendSymbolLayer(symbol_layer_inner)
    symbol.appendSymbolLayer(symbol_layer)
    # set the global layer symbology
    renderer.setClusterSymbol(symbol)
    # apply global symbology to layer
    layer.setRenderer(renderer)

    return layer


def addlayer_with_icone(layer, type_couche, project, icone, couleur_remplissage):

    if not layer.isValid():
        print("Layer failed to load!")
    else:
        layer = setPointSymbology(layer, icone, couleur_remplissage)
        if(project.mapLayersByName(layer.name())):
            print("couche existente dans le projet")
        else:
            project.addMapLayer(layer)

            WFSLayers = project.readListEntry('WFSLayers', '')
            b = list(WFSLayers)[0]

            if layer.isValid():
                b.append(u'%s' % layer.id())
                project.writeEntry('WFSLayers', '',  b)
        return layer


def addlayer(layer, type_couche, project, qml_file):
    if not layer.isValid():
        print("Layer failed to load!")
    else:
        layer.loadNamedStyle(qml_file)

        if(project.mapLayersByName(layer.name())):
            print("couche existente dans le projet")
        else:
            project.addMapLayer(layer)

            WFSLayers = project.readListEntry('WFSLayers', '')
            b = list(WFSLayers)[0]

            if layer.isValid():
                b.append(u'%s' % layer.id())
                project.writeEntry('WFSLayers', '',  b)
        return layer


def add_layer_to_project(path_project, repertoire_sauvegarde, couche_path, layer_name, type_couche):

    # get arguments

    #layername = sys.argv[4]
    filename = os.path.basename(couche_path)

    if(not os.path.exists(repertoire_sauvegarde+"/styles/")):

        os.mkdir(repertoire_sauvegarde+"/styles/")

    if(not os.path.exists(repertoire_sauvegarde+"/shapefile/")):

        os.mkdir(repertoire_sauvegarde+"/shapefile")

    if(not os.path.exists(repertoire_sauvegarde+"/kml/")):

        os.mkdir(repertoire_sauvegarde+"/kml/")

    if(not os.path.exists(repertoire_sauvegarde+"/geojson/")):

        os.mkdir(repertoire_sauvegarde+"/geojson/")

    if(not os.path.exists(repertoire_sauvegarde+"/gpkg/")):

        os.mkdir(repertoire_sauvegarde+"/gpkg/")

    if(not os.path.exists(repertoire_sauvegarde+"/"+path_project+".qgs")):

        open(repertoire_sauvegarde+"/"+path_project+".qgs", "w")

    couche_prefix, couche_suffix = os.path.splitext(couche_path)

    os.environ["QT_QPA_PLATFORM"] = "offscreen"
    QgsApplication.setPrefixPath("/usr", True)
    qgs = QgsApplication([], False)
    qgs.initQgis()
    project = QgsProject()
    project.read(repertoire_sauvegarde+"/"+path_project+".qgs")
    layer = ""
    if(couche_path.endswith(".zip")):

        layers = []
        with zipfile.ZipFile(couche_path) as z:
            for filename in z.namelist():

                if(filename.endswith('.shp')):
                    uri = couche_path

                    layer_load = QgsVectorLayer(uri, layer_name, "ogr")

                    # set layer icons

                    if len(sys.argv) == 8:
                        layer = addlayer_with_icone(
                            layer_load, type_couche, project, icone, couleur_remplissage)
                    else:
                        layer = addlayer(
                            layer_load, type_couche, project, qml_file)
                    filename = os.path.basename(couche_path)

                    shutil.copy(couche_path, repertoire_sauvegarde +
                                "/shapefile/"+filename)
                    layer.saveNamedStyle(
                        repertoire_sauvegarde+"/styles/"+layer_name+".qml")

    elif(couche_path.endswith(".geojson")):
        layer = QgsVectorLayer(couche_path, layer_name, "ogr")
        if len(sys.argv) == 8:
            layer = addlayer_with_icone(
                layer, type_couche, project, icone, couleur_remplissage)
        else:
            layer = addlayer(layer, type_couche, project, qml_file)

        filename = os.path.basename(couche_path)
        shutil.copy(couche_path, repertoire_sauvegarde+"/geojson/"+filename)

        layer.saveNamedStyle(repertoire_sauvegarde +
                             "/styles/"+layer_name+".qml")

    elif(couche_path.endswith(".kml")):

        layer_load = QgsVectorLayer(couche_path, couche_prefix, "ogr")
        subLayers = layer_load.dataProvider().subLayers()
        for subLayer in subLayers:
            name = subLayer.split('!!::!!')[1]
            uri = couche + "|layername="+layer_name
            # Create layer
            layer = QgsVectorLayer(uri, layer_name, 'ogr')
        # Add layer to map
            if len(sys.argv) == 8:
                layer = addlayer_with_icone(
                    layer, type_couche, project, icone, couleur_remplissage)
            else:
                layer = addlayer(layer, type_couche, project, qml_file)

            filename = os.path.basename(couche_path)
            shutil.copy(couche_path, repertoire_sauvegarde+"/kml/"+filename)

            layer.saveNamedStyle(repertoire_sauvegarde +
                                 "/styles/"+layer_name+".qml")

    elif(couche_path.endswith(".gpkg")):
        gpkg_directory = create_directory(repertoire_sauvegarde, "gpkg")
        gpkg_layers = [l.GetName() for l in ogr.Open(couche_path)]
        # append the layername part
        for item in gpkg_layers:

            layer1 = couche_path + "|layername="+item

            # e.g. gpkg_places_layer = "/usr/share/qgis/resources/data/world_map.gpkg|layername=countries"

            layer = QgsVectorLayer(layer1, layer_name, "ogr")
            if len(sys.argv) == 8:
                layer = addlayer_with_icone(
                    layer, type_couche, project, icone, couleur_remplissage)
            else:
                layer = addlayer(layer, type_couche, project, qml_file)

            shutil.copy(couche_path, repertoire_sauvegarde+"/gpkg/"+filename)
            layer.saveNamedStyle(repertoire_sauvegarde +
                                 "/styles/"+layer_name+".qml")

    else:
        return json.dumps({"error": "format de fichier non géré"})

   # if(type_couche == "point"):
    extend = []
    extent = layer.extent()
    extend.append(extent.xMinimum())
    extend.append(extent.yMinimum())
    extend.append(extent.xMaximum())
    extend.append(extent.yMaximum())
    response = {"path_project": repertoire_sauvegarde+"/"+path_project+".qgs",
                "features": layer.featureCount(), "scr": layer.crs().authid(), "bbox": extend}
  #  else:
  #      response={"chemin_projet":repertoire_sauvegarde+"/"+path_project+".qgs","features":layer.featureCount(),"scr":layer.crs().description()}
    project.write()
    # Serializing json
   # json_object = json.dumps(response, indent=4)

    # print(response)
    return json.dumps(response)


project = sys.argv[1]
repertoire_sauvegarde = sys.argv[2]
couche = sys.argv[3]
type_couche = sys.argv[4]
layer_name = sys.argv[5]
if(len(sys.argv) == 8):

    icone = sys.argv[6]
    couleur_remplissage = sys.argv[7]

    print(add_layer_to_project(project, repertoire_sauvegarde,
                               couche, layer_name, type_couche))


elif(len(sys.argv) == 7):
    qml_file = sys.argv[6]
    print(add_layer_to_project(project, repertoire_sauvegarde,
                               couche, layer_name, type_couche))

else:
    print(json.dumps({"error": "nombre d'arguments incorrect"}))
