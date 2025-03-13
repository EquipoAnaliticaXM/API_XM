"""
Module built to simplify the integration of python with the SIMEM open data API 

Author: Sebastian Montoya

"""

import os
import requests
import logging
import pandas as pd
from dataclasses import dataclass
import datetime as dt
import time 
from itertools import repeat
import json
from pprint import pprint
import plotly.graph_objects as go
import webbrowser

DATASETID = ""
VARIABLE_INVENTORY_ID = "a5a6c4"
CATALOG_ID =  "e007fb"
REFERENCE_DATE = '1990-01-01'
DATE_FORMAT = "%Y-%m-%d"
TODAY = dt.datetime.strftime(dt.datetime.now(), DATE_FORMAT)
BASE_API_URL = "https://www.simem.co/backend-files/api/PublicData?startdate={}&enddate={}"
PATH = '..\list_var.json'
VERSION_DATASET_ID = '24914F'
VERSION_COLUMN_DF_VER = 'Version'

class _Validation:
    
    @staticmethod 
    def log_approve(variable):
        approve_message = f"Variable values validated: {variable}"
        logging.debug(approve_message)

    @staticmethod
    def filter(var_column : str, var_values: str | list) -> None | tuple[str,list]:
        if not var_column and not var_values:
            logging.info("No filter has been chosen.")
            return None
        if not var_column or not var_values:
            logging.info("Check that the column and values are both defined for the filter. No filter has been chosen")
            return None
        if not isinstance(var_column, str):
            raise TypeError("Column filter must be a string")
        if isinstance(var_values, str):
            var_values = [var_values]
        elif not isinstance(var_values, list):
            raise TypeError("Values filter must be a string or a list")
        var_filter = (var_column, var_values)
        _Validation.log_approve(var_filter)
        return var_filter
    
    @staticmethod
    def date(var_date) -> dt.datetime:
        try:  
            if isinstance(var_date, dt.datetime):
                return var_date
            var_date = dt.datetime.strptime(var_date, DATE_FORMAT)
            return var_date
        except ValueError:
            raise ValueError("Incorrect date format, use YYYY-MM-DD")


    @staticmethod
    def datasetid(var_dataset_id: str):
        if not isinstance(var_dataset_id, str):
            raise TypeError("Incorrect data type for ID, must be a string")
        var_dataset_id = var_dataset_id.strip()
        if len(var_dataset_id) > 6:
            raise ValueError("Invalid dataset ID")
        if not var_dataset_id.isalnum():
            raise ValueError("Dataset ID must be alphanumeric")
        _Validation.log_approve(var_dataset_id)
        return var_dataset_id
    
    @staticmethod
    def catalog_type(cat_type: str):
        if not isinstance(cat_type, str):
            raise TypeError("Incorrect data type for catalog type, must be a string")
        cat_type = cat_type.lower()
        if cat_type not in ('datasets', 'variables'):
            raise ValueError("Wrong parameter registered. Write 'Datasets' or 'Variables'.")
        _Validation.log_approve(cat_type)
        return cat_type

                
        
@dataclass
class ReadSIMEM:
    """
    Class to request dataset information and data to SIMEM using API

    Parameters: 
    dataset_id : str
        ID of the dataset to request data.
    start_date : str | dt.datetime 
        The starting date for the data slicing.
    end_date : str | dt.datetime 
        The ending date for the data slicing.
    filter_column (Optional): str 
        The column name to apply the filter on.
    filter_values (Optional): str | list 
        The values to filter the column by.
    
    Attributes:
    url_api : str
        The base URL for the SIMEM API.
    session : requests.Session
        The session for making requests to the API.
    __filter_values : tuple[str, list]
        The filter values for the dataset request.
    __filter_url : str
        The filter URL for the dataset request.
    __dataset_info : dict
        The dataset information.
    __metadata : pd.DataFrame
        The metadata of the dataset.
    __columns : pd.DataFrame
        The columns of the dataset.
    __name : str
        The name of the dataset.
    __granularity : str
        The granularity of the dataset.
    __resolution : int
        The resolution of the dataset.
    __date_filter : str
        The date filter column.

    Methods:

    __init__(self, dataset_id: str, start_date: str | dt.datetime, end_date: str | dt.datetime,
             filter_column: str = None, filter_values: str | list = None):
        Initializes the ReadSIMEM instance with the given parameters making a request to the API to extract
        the dataset metadata for further use.

    set_filter(self, column, values) -> None:
        Sets the filter for the dataset request and the complement for the URL.
        If one of the 2 arguments are not given the filter won't set.
    
    set_dates(self, start_date: str | dt.datetime, end_date: str | dt.datetime) -> None:
        Sets the start and end dates for the dataset request.
    
    main(self, data_format: str = 'csv', save_file: bool = False, filter: bool = False) -> pd.DataFrame | dict:
        Retrieves the dataset data for the given dates.
    """

    def __init__(self, dataset_id: str, start_date: str | dt.datetime, end_date: str| dt.datetime,
                 filter_column: str = None, filter_values: str | list = None):
        t0 = time.time()
        print('*' * 100)
        print('Initializing object')
        self.url_api: str = BASE_API_URL
        self._set_datasetid(dataset_id)
        self.set_dates(start_date, end_date)
        self.set_filter(filter_column, filter_values)
        self._set_dataset_data()
        t1 = time.time()
        logging.info(f'Initiallization complete in: {t1 - t0 : .2f} seconds.')
        print(f'The object has been initialized with the dataset: "{self.__name}"')
        print('*' * 100)


    def set_filter(self, column, values) -> None:
        """
        Sets the filter for the dataset request and the complement for the URL.
        If one of the 2 arguments are not given the filter won't set.
        
        Parameters:
        column : str
            The column name to apply the filter on.
        values : str | list
            The values to filter the column by.
        
        Returns:
        None
        """
        var_filter = _Validation.filter(column, values)
        if var_filter is None:
            var_filter = ''
            self.__filter_url: str = "&columnDestinyName=&values="
            return
        self._filter_values: tuple[str, list] =  var_filter
        self.__filter_url: str = f"&columnDestinyName={column}&values={','.join(var_filter[1])}"
        logging.info("Filter defined")

    def _set_datasetid(self, dataset_id) -> None:
        """
        Sets the dataset ID for the request and complement the basic url for the defined dataset.
        
        Parameters:
        dataset_id : str
            The dataset ID to be set.
        
        Returns:
        None
        """
        dataset_id = _Validation.datasetid(dataset_id)
        self.__dataset_id: str = dataset_id.lower()
        self.url_api = self.url_api + f"&datasetId={dataset_id}"
        logging.info("ID defined")

    def set_dates(self, start_date: str | dt.datetime, 
                  end_date: str | dt.datetime) -> None:
        """
        Sets the start and end dates for the dataset request.
        
        Parameters:
        start_date : str | dt.datetime
            The start date for the dataset request.
        end_date : str | dt.datetime
            The end date for the dataset request.
        
        Returns:
        None
        """
        start_date = _Validation.date(start_date)
        end_date = _Validation.date(end_date)
        if start_date > end_date:
            logging.info("Dataset will be empty - Start date is bigger than end date")
        self.__start_date: dt.datetime = start_date
        self.__end_date: dt.datetime = end_date
        if hasattr(self, '__dataset_info'):
            self.__dataset_info["parameters"]["startDate"] =  dt.datetime.strftime(start_date)
            self.__dataset_info["parameters"]["endDate"] =  dt.datetime.strftime(end_date)
        logging.info("Dates defined")
        
    def _set_dataset_data(self) -> None:
        """
        Internal method to set dataset information and metadata.
        Makes a initial request to the API to extract and organize all the information 
        related to the required dataset inside the object.
        
        Returns:
        None
    
        """
        with requests.Session() as session:
            url = self.url_api.format(REFERENCE_DATE, REFERENCE_DATE)
            response = self._make_request(url, session)
            response["parameters"]["startDate"] = dt.datetime.strftime(self.get_startdate(), DATE_FORMAT)
            response["parameters"]["endDate"] = dt.datetime.strftime(self.get_enddate(), DATE_FORMAT)
            self.__dataset_info = response
            metadata = response["result"]["metadata"]
            self.__columns: pd.DataFrame = pd.DataFrame.from_dict(response["result"]["columns"])
            self.__date_filter: str = response["result"]["filterDate"]
            self.__metadata: pd.DataFrame = pd.DataFrame.from_records([metadata])
            self.__name: str = response["result"]["name"]
            self.__granularity: str = metadata["granularity"]
            self.__resolution: int = self.__check_date_resolution(self.__granularity)
            session.close()
        
    def main(self, output_folder : str = "", filter: bool = False) -> pd.DataFrame:
        """
        Creates a dataframe with the information about the required dataset 
        in the given dates.
        
        Parameters:
        data_format : str 
            The format in which to return the data. Default is 'csv'.
        save_file : bool
            If True, the extracted data will be saved to a file. Default is False.
        filter : bool
            If True, applies a filter to the data extraction process. Default is False.
        
        Returns:
        result: 
            The extracted and formatted data.
        """
        print('Inicio consulta sincronica') 
        
        t0 = time.time()
        resolution: int = self.get_resolution()
        urls: list[str] = self.__create_urls(self.get_startdate(), self.get_enddate(), resolution, filter)
        t1 = time.time()
        print(f'Creacion url: {t1 - t0}')

        with requests.Session() as session:
            records = list(map(self._get_records, urls, repeat(session)))
        
        records = [item for sublist in records for item in sublist if len(sublist) != 0]

        t2 = time.time()
        print(f'Extraccion de registros: {t2 - t1}')

        result = pd.DataFrame.from_records(records)
        if os.path.exists(output_folder):
            new_file = self.__save_dataset(output_folder, result)
            result = pd.read_csv(new_file)
        print('End of data extracting process')
        print('*' * 100)
        
        return result


    def _get_records(self, url: str, session: requests.Session) -> list:
        """
        Makes the request and returns a list of records from the dataset.
        
        Parameters:
        url : str
            The URL for the dataset request.
        session : requests.Session
            The session for making the request.
        
        Returns:
        list
            A list of records from the dataset.
        """
        response = self._make_request(url, session)
        result = response.get('result', {}) 
        records = result.get('records', [])
        if len(records) == 0:
           print(f'For the URL: {url}') 
           print('There are 0 records') 
        logging.info("Records saved: %d rows registered.", len(records))
        
        
        return records


    def __save_dataset(self, output_folder: str, result : pd.DataFrame = None) -> str:
        """
        This method saves the dataset to a file with a default name that includes the dataset ID and the date range.
        The file is saved in CSV format.
        
        Parameters:
            output_folder : str
            The folder where the output file will be saved.

        Returns:
            str
            The path to the saved file.
        
        """
        
        print('The file will be saved with a default name.')
        datasetid = f'{self.get_datasetid().upper()}'
        fechas = f'{self.get_startdate().date()}_{self.get_enddate().date()}'
        file_name = '_'.join([datasetid, fechas])
        file_name = os.path.join(output_folder, file_name + '.csv')

        result.to_csv(file_name, index=False)
        print(f'{file_name} saved into {output_folder}')
        logging.info("%s from %s to %s dataset saved.", self.get_datasetid(), self.get_startdate(), self.get_enddate())
       
        return file_name 
    
    @staticmethod
    def _make_request(url: str, session: requests.Session) -> dict:
        """
        Makes the GET request to the URL inside a session and delivers a dictionary
        with the response.
        
        Parameters:
        url : str
            The URL for the dataset request.
        session : requests.Session
            The session for making the request.
        
        Returns:
        dict
            A dictionary containing the response in json encoded format.
        """
        response = session.get(url)
        logging.info("Response with status: %s", response.status_code)
        response.raise_for_status()
        data = response.json()

        status : str = data.get('success', False)
        api_params = data.get('parameters', None)
        datasetid = api_params.get('idDataset', None)
        if status is not True and datasetid not in [CATALOG_ID, VARIABLE_INVENTORY_ID]: 
            message : str = data.get('message', None)
            print(f'For the URL: {url}')
            print(f'The next message was returned: {message}')

        return data


    @staticmethod
    def __check_date_resolution(granularity: str) -> int:
        """
        Checks if the date range given in the object is allowed in a request to the API.
        
        Parameters:
        granularity : str
            The granularity of the date range (e.g., 'Diaria', 'Horaria', 'Mensual', 'Semanal', 'Anual').
        
        Returns:
        int
            The maximum allowed date range in days.
        """
        if granularity in ['Diaria','Horaria']:
            resolution = 31
        elif granularity in ['Mensual','Semanal']:
            resolution = 731
        elif granularity == 'Anual':
            resolution = 1827
        else:
            resolution = 0
        
        return resolution

    @staticmethod
    def _generate_start_dates(start_date: dt.datetime, end_date: dt.datetime, resolution: int):
        """
        Generator to deliver a list of date ranges.
        
        Parameters:
        start_date : dt.datetime
            The start date of the range.
        end_date : dt.datetime
            The end date of the range.
        resolution : int
            The maximum allowed date range in days.
        
        Yields:
        str
            The start dates in the specified date range formatted as strings.
        """
        intervals = (end_date - start_date)/resolution

        for i in range(0, intervals.days + 1):
            yield (start_date + dt.timedelta(days=resolution)*i).strftime(DATE_FORMAT)
        yield (end_date.strftime(DATE_FORMAT))

    def __create_urls(self, start_date: str, end_date: str, resolution: int, filter: bool= False) -> list[str]:
        """
        Receive the limit dates and deliver the API URLs for the dataset id 
        and different date ranges based on resolution.
        
        Parameters:
        start_date : str
            The start date of the range in 'YYYY-MM-DD' format.
        end_date : str
            The end date of the range in 'YYYY-MM-DD' format.
        resolution : int
            The maximum allowed date range in days.
        filter : bool, optional
            Whether to apply the filter to the dataset request (default is False).
        
        Returns:
        list[str]
            A list of URLs for the dataset requests.
        """
        start_dates: list[str] = list(date for date in self._generate_start_dates(start_date, end_date, resolution))
        end_dates: list[str] = [(dt.datetime.strptime(date,'%Y-%m-%d') - dt.timedelta(days=1)).strftime('%Y-%m-%d') for date in start_dates]
        end_dates[-1] = start_dates[-1]
        start_dates.pop(-1)
        end_dates.pop(0)
        if filter:
            base_url = self.url_api + self.get_filter_url()
        else:
            base_url = self.url_api
        urls: list[str] = list(map(base_url.format, start_dates, end_dates))
            
        logging.info("Urls created between %s and %s for %s", self.get_startdate(), self.get_enddate(), self.get_datasetid())
        return urls

    def get_datasetid(self) -> str:
        """
        Returns the dataset ID.
        
        Returns:
        str
            The dataset ID.
        """
        return self.__dataset_id

    def get_startdate(self) -> dt.datetime:
        """
        Returns the start date of the dataset object.
        
        Returns:
        dt.datetime
            The start date in datetime object.
        """
        return self.__start_date

    def get_enddate(self) -> dt.datetime:
        """
        Returns the end date of the dataset object.
        
        Returns:
        dt.datetime
            The end date in datetime object.
        """
        return self.__end_date

    def get_filter_url(self) -> str | None:
        """
        Returns the filter URL complement for the dataset request.
        
        Returns:
        str
            The filter URL.
        """
        var_filter_url = getattr(self, "_ReadSIMEM__filter_url", None)
        if var_filter_url is None:
            logging.info("No filter assigned.")
        return var_filter_url

    def get_filters(self) -> tuple | None:
        """
        Returns the filter values for the dataset request.
        
        Returns:
        tuple | str
            The filter values.
        """
        var_filter_values = getattr(self, "_filter_values", None)
        if var_filter_values is None:
            logging.info("No filter assigned.")  
        return var_filter_values  

    def get_resolution(self) -> int:
        """
        Returns the resolution of the dataset object.
        
        Returns:
        int
            The resolution in days.
        """
        return self.__resolution

    def get_granularity(self) -> str:
        """
        Returns the granularity of the dataset object.
        
        Returns:
        str
            The granularity (e.g., 'Diaria', 'Horaria', 'Mensual', 'Semanal', 'Anual').
        """
        return self.__granularity

    def get_metadata(self) -> dict:
        """
        Returns the metadata of the dataset.
        
        Returns:
        dict
            The metadata of the dataset.
        """
        return self.__metadata

    def get_columns(self) -> pd.DataFrame:
        """
        Returns the columns of the dataset.
        
        Returns:
        pd.DataFrame
            A DataFrame containing the columns of the dataset.
        """
        return self.__columns  

    def get_name(self) -> str:
        """
        Returns the name of the dataset.
        
        Returns:
        str
            The name of the dataset.
        """
        return self.__name
    
    def get_filter_column(self) -> str:
        """
        Retrieves the assigned column to filter the dates in SIMEM.

        Returns:
        str
            The current column filter.
        """
        return self.__date_filter

    def __get_dataset_info(self) -> dict:
        """
        Returns the dataset information.
        
        Returns:
        dict
            A dictionary containing the dataset information.
        """
        return self.__dataset_info


class CatalogSIMEM(ReadSIMEM):
    """
    Class to interact with the SIMEM catalogs.
    
    Args:
    catalog_type : str
        The type of catalog to extract from the webpage ('Datasets', 'Variables')

    Methods:
    get_data(self) -> pd.DataFrame:
        Retrieves the catalog data stored in the object.

    """
    
    def __init__(self, catalog_type: str):
        
        self.set_dates(REFERENCE_DATE, TODAY)
        self.url_api = BASE_API_URL
        
        catalog_type = _Validation.catalog_type(catalog_type)
        if catalog_type == 'datasets':
            self._set_datasetid(CATALOG_ID)
        elif catalog_type == 'variables':
            self._set_datasetid(VARIABLE_INVENTORY_ID)

        self._set_dataset_data()
        self.url_api = self.url_api.format(self.get_startdate(), self.get_enddate())
        with requests.Session() as session:
            datasets = super()._get_records(self.url_api, session)
            self.__data = pd.DataFrame.from_records(datasets)
        logging.info("Catalog retrieved correctly.")

    def get_data(self) -> pd.DataFrame:
        """
        Retrieves the data stored in the object.

        Returns:
            pd.DataFrame: The data stored in the object.
        """
        return self.__data

class VariableSIMEM:
    """
    Class to view the information of a SIMEM variable.

    Args: 
    cod_variable : str
        Code of the variable.
    start_date : str | dt.datetime 
        The starting date for the data slicing.
    end_date : str | dt.datetime 
        The ending date for the data slicing.
    version (Optional): int | str
        The version of the variable.
    esCalidad (Optional): bool 
        Is the object is for Calidad functions.
    
    Methods:
    get_index_data(self) -> pd.DataFrame:
        Return the data of the variable with indexes.
    
    describe_data(self) -> json:
        Return a json with static information (mean, min, max, std dev, dates, median, etc) of the variable.
    
    time_series_data(self) -> html:
        Return an html file with the time series variable.

    show_info(self) -> json, html:
        Return the static information and the time series of the data.
    """

    def __init__(self, cod_variable, start_date, end_date, version = 0, esCalidad = False):
        self.__json_file = VariableSIMEM._read_json(PATH)
        self.__var = cod_variable # Externo
        self.__user_version = version # Externo - Seria version solicitada o de usuario
        self.__dataset_id = self.__json_file[self.__var]["dataset_id"] # Externo
        self.__variable_column = self.__json_file[self.__var]['var_column']
        self.__date_column = self.__json_file[self.__var]['date_column']
        self.__version_column = self.__json_file[self.__var]['version_column']
        self.__start_date = start_date # Externo
        self.__end_date = end_date # Externo
        self.__esCalidad = esCalidad # Nombre
        self.__data = None
        self.__versions_df = None
        

    @staticmethod
    def _read_json(file_path): # read json
        """
        Read the json configuration file with the features and list of variables in SIMEM.
        
        Parameters:
            file_path : str
                The address path of the json file.
        
        Returns:
            json
                The json configuration to get the variable information.
        """

        path = os.path.join(os.path.dirname(__file__), file_path)

        with open(path, 'r', encoding='utf-8') as archivo:
            json_file = json.load(archivo)
        
        return json_file        


    def _read_dataset_data(self, start_date, end_date):
        """
        Use the ReadSIMEM class to get the dataset with the information of the variable.
        
        Parameters:
            dataset_id : str
                The id of the dataset.
            start_date : str | dt.datetime 
                The starting date for the data slicing.
            end_date : str | dt.datetime 
                The ending date for the data slicing.
        
        Returns:
            pd.DataFrame
                The variable dataset.
        """
        if self.__data is not None:
            return
    
        var_column = self.__variable_column

        dataset = ReadSIMEM(self.__dataset_id, start_date, end_date, var_column, self.__var)

        if len(var_column) == 0:
            self.__granularity = dataset.get_granularity()
            return dataset.main(filter = True)

        return dataset.main()


    def _index_df(self, dataset):
        """
        Indexes the dataset by date and version if it is versioned or only by date if it is not.
        
        Parameters:
            dataset : pd.DataFrame
                The dataset to index.
        
        Returns:
            pd.DataFrame
                The variable dataset indexed.
        """

        date_column = self.__date_column
        version_column = self.__version_column

        if len(version_column) == 0:
            self.__index_data = dataset.set_index([date_column, version_column])
        else:
            self.__index_data = dataset.set_index([date_column])

        return self.__index_data
        
    def _get_index_data(self):
        """
        Returns the indexed data.
        
        Returns:
            pd.DataFrame
                The indexed data.
        """

        self._read_dataset_data(self.__start_date, self.__end_date)
        data = self._index_df(self.__data)

        if len(self.__version_column) == 0:
            data = self._calculate_version(data, self.__user_version)

        return data
    
    def _get_structure_data(self):
        """
        Returns the variable data with an specific structure.
        
        Returns:
            pd.DataFrame
                Contains the data of the variable with a new structure.
        """

        data = self._get_index_data()
        data = data.reset_index()
        data = self.__set_structure(data)
        return data

    def get_data(self):
        """
        Returns the variable data.
        
        Returns:
            pd.DataFrame
                Contains the data of the variable.
        """

        data = self._get_index_data()

        if(self.__esCalidad):
            data = data.reset_index()
            return self.__set_structure(data) # format for qualitycheck
        return data
    
    def __set_structure(self, data):
        """
        Sets an specific structure to the columns of the dataframe.
        
        Returns:
            pd.DataFrame
                Return the dataframe with this columns: 'fecha', 'codigoMaestra', 'codigoVariable', 'maestra' and 'valor'.
        """

        maestra = self.__json_file[self.__var]['maestra_column']
        cod_maestra = self.__json_file[self.__var]['codMaestra_column']
        value_column = self.__json_file[self.__var]['value_column']
        var_column = self.__json_file[self.__var]['var_column']
        date_column = self.__date_column
        maestra_column = 'maestra'
        cod_maestra_column = 'codigoMaestra'
        date = 'fecha'
        value = 'valor'
        var = 'codigoVariable'
        data[maestra_column] = maestra

        if cod_maestra is not None:
            data = data.rename(columns = {cod_maestra: cod_maestra_column, date_column: date, value_column: value, var_column: var})
            
        else:
            data[cod_maestra_column] = maestra
            data = data.rename(columns = {date_column: date, value_column: value, var_column: var})
        
        data = data[[date, cod_maestra_column, var, maestra_column, value]]
            
        return data


    @staticmethod
    def __order_date(dataset, date_column):
        """
        Adds a month column, then sorts the DataFrame by a date and month column, 
        assigns a negative incremental number within each month, and returns the DataFrame sorted by its original index.
        
        Parameters:
            dataset : pd.DataFrame
                The dataset to order.
            date_column : str
                The name of the dataset date column.
        
        Returns:
            pd.DataFrame
             The dataset with a new column with the order by the date column.
        """

        dataset['month'] = dataset.apply(lambda x:pd.to_datetime(x['FechaInicio']).month,axis=1)
        df_sorted = dataset.sort_values(by=[date_column, 'month'], ascending=[False, True])
    
        df_sorted['order'] = -df_sorted.groupby('month').cumcount(ascending=True)
    
        return df_sorted.sort_index()
    
    @staticmethod
    def __filter_by_order(dataset, order_value):
        """
        Filters a DataFrame by a specific value in the 'order' column, returning the rows that match 
        that value within each 'month' group, or the rows with the maximum or minimum value of 'order' 
        if the specified value is not present.
        
        Parameters:
            dataset : pd.DataFrame
                The dataset to filter.
            order_value : int
                The filter value.
        
        Returns:
            pd.DataFrame
             The dataset filtered by the order value.
        """

        order_column = 'order'
        def filter_group(x):
            if order_value in x[order_column].values:
                return x[x[order_column] == order_value]
            elif order_value > x[order_column].max():
                return x[x[order_column] == x[order_column].max()]
            else:
                return x[x[order_column] == x[order_column].min()]
    
        filtered_df = dataset.groupby('month', group_keys=False).apply(filter_group, include_groups=False).reset_index(drop=True)
    
        return filtered_df
    
    @staticmethod
    def __filter_by_version(dataset, version_value):
        """
        Filters a DataFrame by a specific value in the 'version' column, returning the rows that match 
        that value within each 'month' group.
        
        Parameters:
            dataset : pd.DataFrame
                The dataset to filter.
            version_value : string
                The filter value.
        
        Returns:
            pd.DataFrame
             The dataset filtered by the version value.
        """

        version_column = VERSION_COLUMN_DF_VER
        def filter_group(x):
            if version_value in x[version_column].values:
                return x[x[version_column] == version_value]

        filtered_df = dataset.groupby('month', group_keys=False).apply(filter_group, include_groups=False).reset_index(drop=True)
    
        return filtered_df
    
    @staticmethod
    def __versions(start_date, end_date, dataset_id, version):
        """
        Gets a DataFrame of data, sorts it by publish date, and then filters it by a specific version.
        
        Parameters:
            dataset_id : str
                Id of the dataset.
            start_date : str | dt.datetime 
                The starting date for the data slicing.
            end_date : str | dt.datetime 
                The ending date for the data slicing.
            version : int | str 
                The version of the variable.
        
        Returns:
            pd.DataFrame
             The variable dataset filtered by a version.
        """

        first_day = start_date.replace(day=1)
        version_df = ReadSIMEM(dataset_id, first_day, end_date).main()
        df_sorted = VariableSIMEM.__order_date(version_df, 'FechaPublicacion')
        
        if isinstance(version, str):
            df_filtered = VariableSIMEM.__filter_by_version(df_sorted, version)
            print(df_filtered)
        elif isinstance(version, int):
            df_filtered = VariableSIMEM.__filter_by_order(df_sorted, version)
            print(df_filtered)

        return df_filtered

    @staticmethod
    def _filter_date(dataset, dates_df, date_column, version_column):
        """
        Filters a data set based on a date range and a specific version.
        
        Parameters:
            dataset : pd.DateFrame
                Dataset of the variable.
            dates_df : pd.DateFrame
                Dataset that contains the dates to filter.
            date_column : str
                Name of the dataset date column.
            version_column : str 
                Name of the dataset version column.
        
        Returns:
            pd.DataFrame
             The variable dataset filtered by the dates.
        """

        date_temp = 'Fecha'
        dataset.reset_index(inplace=True)
        dataset = dataset.rename(columns={date_column: date_temp})
        print('Dentro de filter date')
        print(version_column)
        print(dataset)
        print(dates_df)
        print('+'* 100)
        dataset = dataset.merge(dates_df, left_on = version_column, right_on = 'Version')
        dataset['FechaFin'] = pd.to_datetime(dataset['FechaFin'])
        dataset = dataset[(dataset[date_temp] >= dataset['FechaInicio']) & (dataset[date_temp] <= dataset['FechaFin']+pd.Timedelta(days=1))]
        dataset = dataset.drop(columns = ['FechaInicio', 'FechaFin', 'FechaPublicacion', 'EsMaximaVersion', 'order'])
        dataset = dataset.rename(columns = {date_temp: date_column})
        dataset.set_index([date_column, version_column], inplace=True)

        return dataset

    def _calculate_version(self, dataset, version):
        """
        Filters and sorts the variable dataset based on a specific version.
        
        Parameters:
            dataset : pd.DateFrame
                Dataset of the variable.
            version : int | str
                Version value.
        
        Returns:
            pd.DataFrame
             The variable dataset filtered by the version.
        """

        df = dataset.copy()
        version_column = self.__version_column
        date_column = self.__date_column
        
        if self.__versions_df is None:
            self.__versions_df = VariableSIMEM.__versions(self.__start_date, self.__end_date, VERSION_DATASET_ID, version)
             
        filtered_df = self.__versions_df

        return VariableSIMEM._filter_date(df, filtered_df, date_column, version_column)
    
    def __calculate_stats(self, dataset, column):
        """
        Calculates the statitic information ('mean', 'median', 'std_dev','min','max','null_count','zero_count',
            'start_date','end_date','granularity') of the dataset.
        
        Parameters:
            dataset : pd.DateFrame
                Dataset of the variable.
            column : str
                Name of the column to calculate the stats.
        
        Returns:
            dic
             Dictionary with the statistics values.
        """

        stats = {
            'mean': float(dataset[column].mean()),
            'median': float(dataset[column].median()),
            'std_dev': float(dataset[column].std()),
            'min': float(dataset[column].min()),
            'max': float(dataset[column].max()),
            'null_count': int(dataset[column].isnull().sum()),
            'zero_count': int((dataset[column] == 0).sum()),
            'start_date': pd.to_datetime(self.__start_date).strftime('%Y-%m-%d'),
            'end_date': pd.to_datetime(self.__end_date).strftime('%Y-%m-%d'),
            'granularity': self.__granularity
            }
        return stats

    def describe_data(self):
        """
        Generates statistics for the variable.
        
        Returns:
            dic
             Dictionary with the statistics values of the variable.
        """

        statistics = {}
        self._read_dataset_data(self.__start_date, self.__end_date)
        data = self._index_df(self.__data)
        column = self.__json_file[self.__var]['value_column']
        name = self.__json_file[self.__var]['name']
        versionado = self.__json_file[self.__var]['esVersionado']
        data[column] = data[column].astype(float)

        if self.__user_version is None and versionado == 1:
            data = self._calculate_version(data, 0)
            statistics[name] = self.__calculate_stats(data, column)

        elif self.__user_version is not None and versionado == 1:
            data = self._calculate_version(data, self.__user_version)
            statistics[name] = self.__calculate_stats(data, column)

        else:
            statistics[name] = self.__calculate_stats(data, column)

        return statistics

    def __plot_time_series(self, dataset, title):
        """
       Generates the time series for the variable.
        
        Parameters:
            dataset : pd.DateFrame
                Dataset of the variable.
            title : str
                Title of the graph.
        
        Returns:
            The time series of the variable.
        """

        date_column = self.__date_column
        value_column = self.__json_file[self.__var]['value_column']
        dataset[value_column] = dataset[value_column].astype(float)

        df_reset = dataset.reset_index()
        df_reset[date_column] = pd.to_datetime(df_reset[date_column])
        df_reset.sort_values(by=date_column, inplace=True)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_reset[date_column], y=df_reset[value_column], mode='lines', name=value_column))

        fig.update_layout(
            title=title,
            xaxis_title='Fecha',
            yaxis_title='Valor',
            xaxis=dict(tickformat='%d-%m-%y'),
            template='plotly_white'
        )

        file_path = 'time_series_plot.html'
        fig.write_html(file_path)
        print(f"Gráfica guardada como '{file_path}'")

        webbrowser.open(file_path)

    def time_series_data(self):
        """
        Graph the dataset time series.
        
        Returns:
            html
             Html file with the time series graph of the variable.
        """

        self._read_dataset_data(self.__start_date, self.__end_date)
        df = self._index_df(self.__data)
        name = self.__json_file[self.__var]['name']
        versionado = self.__json_file[self.__var]['esVersionado']

        if self.__user_version is None and versionado == 1:
            data = self._calculate_version(df, 0)
            self.__plot_time_series(data, f'Serie de Tiempo {name}')
        elif self.__user_version is not None and versionado == 1:
            data = self._calculate_version(df, self.__user_version)
            self.__plot_time_series(data, f'Serie de Tiempo {name}')
        else:
            self.__plot_time_series(df, f'Serie de Tiempo {name}')

    def show_info(self):
        """
        Gets all the information functions of the object.
        
        Returns:
            Dictionary with the statistics values of the variable.
            Html file with the time series graph of the variable.
        """

        pprint(self.describe_data())
        self.time_series_data()

if __name__ == '__main__':

    dataset_id = '6e0197'
    fecha_inicio = '2023-07-28'
    fecha_fin = '2023-08-02'


    simem = ReadSIMEM(dataset_id, fecha_inicio, fecha_fin)
    df = simem.main(output_folder=".", filter=False)
