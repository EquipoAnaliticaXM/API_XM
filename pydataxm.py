#!/usr/bin/venv python
# -*- coding: utf-8 -*-

"""
Created on Thu Ene 1 16:15:13 2020

@author: Equipo de Analitica XM
"""

import requests
import json
import pandas as pd
import datetime as dt
from pandas.io.json import json_normalize


class ReadDB:
    def __init__(self):
        self.url = "http://servapibi.xm.com.co/hourly"
        self.connection = None
        self.request = ''
        self.inventario_metricas = {'Gene': [(0, 'Generacion Real', 'Sistema', 'Horaria'),
                                             (1, 'Generacion Real por Recurso', 'Recurso', 'Horaria'),
                                             (2, 'Generacion por tipo de despacho', 'Renovabilidad', 'Horaria')]
            , 'DemaCome': [(0, 'Demanda Comercial', 'Sistema', 'Horaria'),
                           (1, 'Demanda Comercial por Agente', 'Agente', 'Horaria')]
            , 'AporEner': [(0, 'Aportes Energia', 'Sistema', 'Diaria')]
            , 'PrecEscaAct': [(0, 'Precio de Escasez de Activacion', 'Sistema', 'Diaria')]
            , 'ConsCombustibleMBTU': [
                (0, 'Consumo Combustible Recursos pertenecientes al Despacho Central', 'Recurso', 'Horaria')]
            , 'PrecOferDesp': [(0, 'Precio de Oferta del Despacho', 'Recurso', 'Horaria')]
            , 'PrecBolsNaci': [(0, 'Precio de Bolsa Nacional', 'Sistema', 'Horaria')]
            , 'MaxPrecOferNal': [(0, 'Máximo Precio de Oferta Nacional', 'Sistema', 'Horaria')]
            , 'RestAliv': [(0, 'Restricciones Aliviadas', 'Sistema', 'Horaria')]
            , 'GeneIdea': [(0, 'Generacion Ideal', 'Sistema', 'Horaria'),
                           (1, 'Generacion Ideal', 'Recurso', 'Horaria')]
            , 'VoluUtilDiarEner': [(0, 'Volumen Util Diario', 'Sistema', 'Diaria')]
            , 'RemuRealIndiv': [(0, 'RRID', 'Sistema', 'Diaria')]
            , 'CapEfecNeta': [(0, 'Listado de recursos térmicos con su respectiva Capacidad Efectiva Neta por mes',
                               'Sistema', 'Anual')]
            ,'VentContEner':[(0,'Ventas en Contratos Energía','Sistema','Horaria'),
                             (1,'Ventas en Contratos Energía por Agente','Agente','Horaria')]
            ,'CompContEner':[(0,'Compras en Contrato Energía','Sistema','Horaria')
                             ,(1,'Compras en Contrato Energía por Agente','Agente','Horaria')]
            ,'CompBolsNaciEner':[(0,'Compras en Bolsa Nacional Energía','Sistema','Horaria')
                                ,(1,'Compras en Bolsa Nacional Energía por Agente','Agente','Horaria')]
            ,'PrecPromContRegu':[(0,'Precio Promedio Contratos Regulado','Sistema','Diaria')]
            ,'PrecPromContNoRegu':[(0,'Precio Promedio Contratos No Regulado','Sistema','Diaria')]}

    def get_collections(self, coleccion):

        return self.inventario_metricas[coleccion]

    def request_data(self, coleccion, metrica, start_date, end_date):
        """ request public server data from XM by the API

        Args:
            variable: one of this variables "DemaCome", "Gene", "GeneIdea", "PrecBolsNaci", "RestAliv"
            start_date: start date consult data
            end_date: end date consult data

        Returns: DataFrame with the raw Data

        """
        if coleccion not in self.inventario_metricas.keys():
            print('No existe la colección {}'.format(coleccion))
            return None
        if metrica > len(self.inventario_metricas[coleccion]):
            print('No existe la metrica')
            return None

        if self.inventario_metricas[coleccion][metrica][3] == 'Horaria':

            end = end_date
            condition = True
            aux = True
            data = None
            while condition:
                if (start_date - end_date).days < 30:
                    end = start_date + dt.timedelta(29)
                if end > end_date:
                    end = end_date
                self.request = {"MetricId": coleccion,
                                "StartDate": "{}".format(str(start_date)),
                                "EndDate": "{}".format(str(end)),
                                'Entity': self.inventario_metricas[coleccion][metrica][2]}

                self.connection = requests.post("http://servapibi.xm.com.co/hourly", json=self.request)
                
                data_json = json.loads(self.connection.content)
            
                temporal_data = json_normalize(data_json['Items'], 'HourlyEntities', 'Date', sep='_')
                
                if data is None:
                    data = temporal_data.copy()
                else:
                    data = data.append(temporal_data, ignore_index=True)
                start_date = start_date + dt.timedelta(30)

                if end == end_date:
                    aux = False
                condition = ((end - start_date).days > 30 | (end - end_date).days != 0) | aux

        elif self.inventario_metricas[coleccion][metrica][3] == 'Diaria':

            end = end_date
            condition = True
            aux = True
            data = None
            while condition:
                if (start_date - end_date).days < 30:
                    end = start_date + dt.timedelta(29)
                if end > end_date:
                    end = end_date

                self.request = {"MetricId": coleccion,
                                "StartDate": "{}".format(str(start_date)),
                                "EndDate": "{}".format(str(end)),
                                'Entity': self.inventario_metricas[coleccion][metrica][2]}
                self.connection = requests.post("http://servapibi.xm.com.co/daily", json=self.request)
                data_json = json.loads(self.connection.content)
                temporal_data = json_normalize(data_json['Items'], 'DailyEntities', 'Date', sep='_')
                if data is None:
                    data = temporal_data.copy()
                else:
                    data = data.append(temporal_data, ignore_index=True)

                start_date = start_date + dt.timedelta(30)
                if end == end_date:
                    aux = False
                condition = ((end - start_date).days > 29 | (end - end_date).days != 0) | aux

        elif self.inventario_metricas[coleccion][metrica][3] == 'Anual':

            end = end_date
            condition = True
            aux = True
            data = None
            while condition:
                if (start_date - end_date).days < 366:
                    end = start_date + dt.timedelta(365)
                if end > end_date:
                    end = end_date

                self.request = {"MetricId": coleccion,
                                "StartDate": "{}".format(str(start_date)),
                                "EndDate": "{}".format(str(end)),
                                'Entity': self.inventario_metricas[coleccion][metrica][2]}
                self.connection = requests.post("http://servapibi.xm.com.co/annual", json=self.request)
                data_json = json.loads(self.connection.content)
                temporal_data = json_normalize(data_json['Items'], 'AnnualEntities', 'Code', sep='_')
                if data is None:
                    data = temporal_data.copy()
                else:
                    data = data.append(temporal_data, ignore_index=True)

                start_date = start_date + dt.timedelta(366)
                if end == end_date:
                    aux = False
                condition = ((end - start_date).days > 365 | (end - end_date).days != 0) | aux

        return data


if __name__ == "__main__":
    consult = ReadDB()
    df = consult.request_data("PrecPromContNoRegu", 0, dt.date(2015, 1, 1), dt.date(2015, 2, 28))
    df.to_excel('ResultadoAPI.xlsx', sheet_name='Hoja1')
