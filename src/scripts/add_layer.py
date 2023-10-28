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
   # symbol_layer.setFontStyle('Book')
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


def addlayer_with_icone(layer,project, icone, couleur_remplissage):

    if not layer.isValid():
        print(json.dumps({"error": "Invalid Layer"}))
    else:
        layer = setPointSymbology(layer, icone, couleur_remplissage)
        if(project.mapLayersByName(layer.name())):
            print(json.dumps({"error": "Couche existante dans le projet"}))
        else:
            project.addMapLayer(layer)

            WFSLayers = project.readListEntry('WFSLayers', '')
            b = list(WFSLayers)[0]

            if layer.isValid():
                b.append(u'%s' % layer.id())
                project.writeEntry('WFSLayers', '',  b)
        return layer


def addlayer(layer,project,qml_file):
    if not layer.isValid():
        print(json.dumps({"error": "Erreur de chargement de la couche"}))
    else:
        layer.loadNamedStyle(qml_file)

        if(project.mapLayersByName(layer.name())):
            print(json.dumps({"error": "Couche existante dans le projet"}))
        else:
            project.addMapLayer(layer)

            WFSLayers = project.readListEntry('WFSLayers', '')
            b = list(WFSLayers)[0]

            if layer.isValid():
                b.append(u'%s' % layer.id())
                project.writeEntry('WFSLayers', '',  b)
        return layer

def path_icone(repertoire_sauvegarde,icone):
   
    filename = os.path.basename(icone)
    icone_path = repertoire_sauvegarde+"/icons/"+filename
    return icone_path

def add_layer_to_project(path_project, repertoire_sauvegarde, couche_path, layer_name, type_couche,icone=""):

    # get arguments

    #layername = sys.argv[4]
    filename = os.path.basename(couche_path)

    if(not os.path.exists(repertoire_sauvegarde+"/icons/")):

        os.mkdir(repertoire_sauvegarde+"/icons/")

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
    icone_path=""

   
    if icone != "":
        shutil.move(icone,repertoire_sauvegarde +"/icons/")

    if(couche_path.endswith(".zip")):

        shutil.move(couche_path, repertoire_sauvegarde +
                    "/shapefile/")
        filename = os.path.basename(couche_path)
        couche_path = repertoire_sauvegarde + "/shapefile/"+filename
        layers = []
        with zipfile.ZipFile(couche_path) as z:
            for filename in z.namelist():

                if(filename.endswith('.shp')):
                    uri = couche_path

                    layer_load = QgsVectorLayer(uri, layer_name, "ogr")

                    # set layer icons

                    if len(sys.argv) == 8:
                        
                        icone_path =  path_icone(repertoire_sauvegarde,icone)
                        layer = addlayer_with_icone(
                            layer_load, type_couche, project, icone_path, couleur_remplissage)
                    else:
                        layer = addlayer(
                            layer_load,project, qml_file)

                    layer.saveNamedStyle(
                        repertoire_sauvegarde+"/styles/"+layer_name+".qml")

    elif(couche_path.endswith(".geojson")):
        shutil.move(couche_path, repertoire_sauvegarde + "/geojson/")
        filename = os.path.basename(couche_path)
        couche_path = repertoire_sauvegarde + "/geojson/"+filename

        layer = QgsVectorLayer(couche_path, layer_name, "ogr")
        if len(sys.argv) == 8:
            icone_path =  path_icone(repertoire_sauvegarde,icone)
            layer = addlayer_with_icone(
                layer, project, icone_path, couleur_remplissage)
        else:
            layer = addlayer(layer, project, qml_file)
        filename = os.path.basename(couche_path)

        layer.saveNamedStyle(repertoire_sauvegarde +
                             "/styles/"+layer_name+".qml")

    elif(couche_path.endswith(".kml")):

        shutil.move(couche_path, repertoire_sauvegarde + "/kml/")
        filename = os.path.basename(couche_path)
        couche_path = repertoire_sauvegarde + "/kml/"+filename

        layer_load = QgsVectorLayer(couche_path, couche_prefix, "ogr")
        subLayers = layer_load.dataProvider().subLayers()
        for subLayer in subLayers:
            name = subLayer.split('!!::!!')[1]
            uri = couche + "|layername="+layer_name
            # Create layer
            layer = QgsVectorLayer(uri, layer_name, 'ogr')
        # Add layer to map
            if len(sys.argv) == 8:
                icone_path =  path_icone(repertoire_sauvegarde,icone)
                layer = addlayer_with_icone(
                    layer, type_couche, project, icone_path, couleur_remplissage)
            else:
                layer = addlayer(layer, project, qml_file)

            filename = os.path.basename(couche_path)

            layer.saveNamedStyle(repertoire_sauvegarde +
                                 "/styles/"+layer_name+".qml")

    elif(couche_path.endswith(".gpkg")):
        shutil.move(couche_path, repertoire_sauvegarde + "/gpkg/")
        filename = os.path.basename(couche_path)
        couche_path = repertoire_sauvegarde + "/gpkg/"+filename

        gpkg_layers = [l.GetName() for l in ogr.Open(couche_path)]
        # append the layername part
        for item in gpkg_layers:

            layer1 = couche_path + "|layername="+item

            # e.g. gpkg_places_layer = "/usr/share/qgis/resources/data/world_map.gpkg|layername=countries"

            layer = QgsVectorLayer(layer1, layer_name, "ogr")
            if len(sys.argv) == 8:
                icone_path =  path_icone(repertoire_sauvegarde,icone)
                layer = addlayer_with_icone(
                    layer, type_couche, project, icone_path, couleur_remplissage)
            else:
                layer = addlayer(layer, project, qml_file)

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
                               couche, layer_name, type_couche,icone))


elif(len(sys.argv) == 7):
    qml_file = sys.argv[6]
    print(add_layer_to_project(project, repertoire_sauvegarde,
                               couche, layer_name, type_couche))

else:
    print(json.dumps({"error": "nombre d'arguments incorrect"}))
