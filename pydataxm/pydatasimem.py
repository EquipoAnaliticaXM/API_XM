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
from datetime import timedelta
from itertools import repeat
import time 
from pprint import pprint

global datasetid, variable_inventory_id, catalog_id, reference_date, base_api_url, url_json_variables, today, version_dataset_id, daily_dataset_id, version_column_df_ver, date_format
datasetid = ""
variable_inventory_id = "a5a6c4"
catalog_id =  "e007fb"
reference_date = '1990-01-01'
date_format = "%Y-%m-%d"
today = dt.datetime.strftime(dt.datetime.now(), date_format)
base_api_url = "https://www.simem.co/backend-files/api/PublicData?startdate={}&enddate={}"
url_json_variables = 'https://www.simem.co/backend-datos/vars/listado_variables.json'
version_dataset_id = '24914F'
daily_dataset_id = '7a30a3'
version_column_df_ver = 'Version'

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
            var_date = dt.datetime.strptime(var_date, date_format)
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
    
    @staticmethod
    def cod_variable(cod_variable: str, list_variables: dict, type: str):
        if not isinstance(cod_variable, str):
            raise TypeError(f"Incorrect data type for {cod_variable}, must be a string")
        if cod_variable in list_variables.keys():
            return cod_variable
        else:
            raise ValueError(f"The {type} code '{cod_variable}' is not available, use the function get_collection() to get all the available {type}s.")
        
    @staticmethod
    def dataset(dataset: pd.DataFrame, start_date: str, end_date: str):
        if len(dataset) == 0:
            raise TypeError(f"There is no data for the date range between {start_date} and {end_date}.")
        return dataset

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
                 filter_column: str | None = None, filter_values: str | list | None = None):
        t0 = time.time()
        print('*' * 100)
        print('Initializing object')
        self.url_api: str = base_api_url
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
            self.__dataset_info["parameters"]["startDate"] =  dt.datetime.strftime(start_date, date_format)
            self.__dataset_info["parameters"]["endDate"] =  dt.datetime.strftime(end_date, date_format)
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
            url = self.url_api.format(reference_date, reference_date)
            response = self._make_request(url, session)
            response["parameters"]["startDate"] = dt.datetime.strftime(self.get_startdate(), date_format)
            response["parameters"]["endDate"] = dt.datetime.strftime(self.get_enddate(), date_format)
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

    def __save_dataset(self, output_folder: str, result : pd.DataFrame | None = None) -> str:
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
        if result is not None:
            result.to_csv(file_name, index=False)
            print(f'{file_name} saved into {output_folder}')
        else:
            print(f'{file_name} not saved into {output_folder}')
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
        if status is not True and datasetid not in [catalog_id, variable_inventory_id]: 
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
            resolution = 1
        elif granularity in ['Mensual','Semanal']:
            resolution = 24
        elif granularity == 'Anual':
            resolution = 60
        else:
            resolution = 0
        
        return resolution

    @staticmethod
    def _generate_dates(start_date: dt.datetime, end_date: dt.datetime, resolution: int):
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

        start_dates = pd.date_range(start=start_date.replace(day=1), end=end_date, freq='MS').to_list()

        if start_date not in start_dates:
            start_dates.pop(0)
            start_dates.insert(0, start_date)
        else:
            start_dates[0] = start_date
        
        start_dates = start_dates[::resolution]

        end_dates = [
            (start_dates[i + 1] - dt.timedelta(days=1))
            for i in range(len(start_dates) - 1)
        ]
        end_dates.append(end_date)
        
        start_dates = [d.strftime(date_format) for d in start_dates]
        end_dates = [d.strftime(date_format) for d in end_dates]

        return start_dates, end_dates

    def __create_urls(self, start_date: str , end_date: str , resolution: int, filter: bool= False) -> list[str]:
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

        start_dates, end_dates = self._generate_dates(start_date=start_date, end_date=end_date, resolution=resolution)
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
        
        self.set_dates(reference_date, today)
        self.url_api = base_api_url
        
        catalog_type = _Validation.catalog_type(catalog_type)
        if catalog_type == 'datasets':
            self._set_datasetid(catalog_id)
        elif catalog_type == 'variables':
            self._set_datasetid(variable_inventory_id)

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
    quality_check (Optional): bool 
        If the object is for Calidad functions.
    
    Methods:
    get_collection() -> pd.DataFrame:
        Return a dataframe with the list of available variables.

    get_data(self) -> pd.DataFrame:
        Return the data of the variable with indexes.
    
    describe_data(self) -> json:
        Return a json with static information (mean, min, max, std dev, dates, median, etc) of the variable.
    """

    def __init__(self, cod_variable: str, start_date: str, end_date: str, version : int|str = 0, quality_check: bool = False):
        self._json_file = VariableSIMEM._read_json()
        self._json_file = self._json_file['variable']
        self._var = _Validation.cod_variable(cod_variable=cod_variable, list_variables=self._json_file, type='variable')
        self.__user_version = version 
        self._dataset_id = self._json_file[self._var]["dataset_id"]
        self._variable_column = self._json_file[self._var]['var_column']
        self._date_column = self._json_file[self._var]['date_column']
        self._version_column = self._json_file[self._var]['version_column']
        self._value_column = self._json_file[self._var]['value_column']
        self._dimensions = self._json_file[self._var]['dimensions']
        self.__esTX2 = self._json_file[self._var]['esTX2PrimeraVersion']
        self._start_date = _Validation.date(start_date)
        self._end_date = _Validation.date(end_date)
        self._quality_check = quality_check
        self._data = None
        self.__versions_df = None

    @staticmethod
    def _read_json() -> dict:
        """
        Read the json configuration file with the features and list of variables in SIMEM.
        
        Parameters:
            file_path : str
                The address path of the json file.
        
        Returns:
            json
                The json configuration to get the variable information.
        """

        response = requests.get(url_json_variables)
        response.raise_for_status()
        json_file = response.json()
        return json_file

    @staticmethod
    def get_collection() -> pd.DataFrame:
        """
        Return a dataframe with the list of available variables.
        
        Returns:
            pd.DataFrame
                Contains the list of available variables.
        """
        
        json_file = VariableSIMEM._read_json()
        df =  pd.DataFrame.from_dict(json_file['variable'], orient='index', columns=['name', 'dimensions', 'version_column', 'date_column']).reset_index().rename(
            columns={'index': 'CodigoVariable', 'name': 'Nombre', 'dimensions': 'Dimensiones'})
        
        dimensions = df[['version_column', 'date_column']].apply(lambda x: list(x.dropna()), axis=1)

        df['Dimensiones'] = df['Dimensiones'] + dimensions
        df = df.drop(['version_column', 'date_column'], axis=1)
        
        return df

    def _read_dataset_data(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Use the ReadSIMEM class to get the dataset with the information of the variable.
        
        Parameters:
            start_date : str | dt.datetime 
                The starting date for the data slicing.
            end_date : str | dt.datetime 
                The ending date for the data slicing.
        
        Returns:
            pd.DataFrame
                The variable dataset.
        """
        if self._data is not None:
            return
    
        var_column = self._variable_column

        dataset = ReadSIMEM(self._dataset_id, start_date, end_date, var_column, self._var)
        check_filter = False
        if var_column is not None:
            self.__granularity = dataset.get_granularity()
            check_filter = True

        data = dataset.main(filter = check_filter)
        self._data = _Validation.dataset(data, start_date, end_date)
        return self._data


    def _index_df(self, dataset: pd.DataFrame) -> pd.DataFrame:
        """
        Indexes the dataset by date and version if it is versioned or only by date if it is not.
        
        Parameters:
            dataset : pd.DataFrame
                The dataset to index.
        
        Returns:
            pd.DataFrame
                The variable dataset indexed.
        """

        date_column = self._date_column
        version_column = self._version_column

        if version_column is not None:
            self.__index_data = dataset.set_index([date_column, version_column] + self._dimensions)
        else:
            self.__index_data = dataset.set_index([date_column] + self._dimensions)

        return self.__index_data
        
    def _get_index_data(self) -> pd.DataFrame:
        """
        Returns the indexed data.
        
        Returns:
            pd.DataFrame
                The indexed data.
        """

        self._read_dataset_data(start_date=self._start_date, end_date=self._end_date)
        data = self._index_df(dataset=self._data)

        if self._version_column is not None:
            data = self._calculate_version(dataset=data, version=self.__user_version)

        return data

    def get_data(self) -> pd.DataFrame:
        """
        Returns the variable data.
        
        Returns:
            pd.DataFrame
                Contains the data of the variable.
        """

        data = self._get_index_data()
        value_column = self._json_file[self._var]['value_column']
        var_column = self._json_file[self._var]['var_column']

        if self._quality_check:
            data = data.reset_index()
            return self.__set_format_for_qualitycheck(dataset=data)
        data = data.rename(columns = {value_column: "Valor"}) if var_column is not None else data
        return data
    
    def __set_format_for_qualitycheck(self, dataset: pd.DataFrame) -> pd.DataFrame:
        """
        Sets an specific structure to the columns of the dataframe.
        
        Returns:
            pd.DataFrame
                Return the dataframe with this columns: 'fecha', 'codigoMaestra', 'codigoVariable', 'maestra' and 'valor'.
        """

        maestra = self._json_file[self._var]['maestra_column']
        cod_maestra = self._json_file[self._var]['codMaestra_column']
        value_column = self._json_file[self._var]['value_column']
        var_column = self._json_file[self._var]['var_column']
        date_column = self._date_column
        maestra_column = 'maestra'
        cod_maestra_column = 'codigoMaestra'
        date = 'fecha'
        value = 'valor'
        var = 'codigoVariable'
        dataset[maestra_column] = maestra

        if cod_maestra is not None:
            dataset = dataset.rename(columns = {cod_maestra: cod_maestra_column, date_column: date, value_column: value, var_column: var})
            
        else:
            dataset[cod_maestra_column] = maestra
            dataset = dataset.rename(columns = {date_column: date, value_column: value, var_column: var})
        
        dataset = dataset[[date, cod_maestra_column, var, maestra_column, value]]
            
        return dataset

    @staticmethod
    def _order_date(dataset: pd.DataFrame, date_column: str) -> pd.DataFrame:
        """
        Adds a month column, then sorts the DataFrame by a date and month column, 
        assigns a negative incremental number within each month, and returns the DataFrame sorted by its original index.
        
        Parameters:
            dataset : pd.DataFrame
                The dataset to order.
            date_column : str
                The name of the dataset date column to order.
        
        Returns:
            pd.DataFrame
             The dataset with a new column with the order by the date column.
        """

        dataset['month'] = dataset.apply(lambda x:pd.to_datetime(x['FechaInicio']).month,axis=1)
        df_sorted = dataset.sort_values(by=[date_column, 'month'], ascending=[False, True])
    
        df_sorted['order'] = -df_sorted.groupby('FechaInicio').cumcount(ascending=True)
    
        return df_sorted.sort_index()
    
    @staticmethod
    def _filter_by_order(dataset: pd.DataFrame, order_value: int, start_date: str, end_date: str, esTX2: bool) -> pd.DataFrame:
        """
        
        Groups a data set by months and applies filtering to them by a order value.
        
        Parameters:
            dataset : pd.DataFrame
                The dataset to filter.
            order_value : int
                The filter value.
            esTX2 | bool
                The value is 1 if the first version is TX2 and 0 if it is TX1.
        
        Returns:
            pd.DataFrame
             The dataset filtered by the order value.
        """

        dataset = VariableSIMEM._generate_missing_months(dataset=dataset, start_date=start_date, end_date=end_date)
        version_column = version_column_df_ver
        order_column = 'order'
        filtered_df = dataset.groupby('month', group_keys=False).apply(lambda month_data: VariableSIMEM._filter_group_by_order(
            month_data, version_column, order_column, order_value, esTX2), include_groups=False).reset_index(drop=True)
    
        return filtered_df
    
    @staticmethod
    def _filter_group_by_order(month_data: pd.DataFrame, version_column: str, order_column: str, order_value: int, esTX2: bool) -> pd.DataFrame:
        """
        Filters a DataFrame by a specific value in the 'order' column, returning the rows that match 
        that value within each 'month' group, or the rows with the maximum or minimum value of 'order' 
        if the specified value is not present.
        
        Parameters:
            month_data : pd.DataFrame
                The dataset of a specific month.
            version_column : str
                The name of the column that contain the version.
            order_column : str
                The name of the column that contain the order.
            order_value : int
                The filter value.
            esTX2 | bool
                The value is 1 if the first version is TX2 and 0 if it is TX1.
        
        Returns:
            pd.DataFrame
             The dataset filtered by the order value.
        """

        if esTX2 == 1 and {'TX1', 'TX2'}.intersection(month_data[version_column].values):
            return month_data[month_data[version_column] == 'TX2']
        elif order_value in month_data[order_column].values:
            return month_data[month_data[order_column] == order_value]
        elif order_value > month_data[order_column].max():
            return month_data[month_data[order_column] == month_data[order_column].max()]
        elif order_value < month_data[order_column].min() and not {'TX1', 'TX2'}.intersection(month_data[version_column].values):
            last_registry = VariableSIMEM._get_last_registry(month_data)
            if order_value == month_data[order_column].min()-1 or esTX2 == 1:
                month_data = VariableSIMEM._set_order_version(dataset=month_data, registry=last_registry, orders=month_data[order_column], version='TX2')
            else: 
                month_data = VariableSIMEM._set_order_version(dataset=month_data, registry=last_registry, orders=month_data[order_column], version='TX1')
        return month_data[month_data[order_column] == month_data[order_column].min()]
    
    @staticmethod
    def _get_last_registry(dataset: pd.DataFrame) -> pd.Series:
        """
        Get the last registry of a dataset
        
        Parameters:
            dataset : pd.DataFrame
                Dataset from which you want to obtain the last record.
        
        Returns:
            pd.Series
             The last record of the dataset.
        """
        return dataset.tail(1).squeeze()
    
    @staticmethod
    def _set_order_version(dataset: pd.DataFrame, registry: pd.Series, orders: pd.Series, version: str) -> pd.DataFrame:
        """
        Calculates the logic for the data that have TXR version, to set the TX1 and TX2 versions.
        
        Parameters:
            dataset : pd.DataFrame
                The dataset with the versions.
            registry: pd.Series
                List that contains a version registry.
            orders : pd.Series
                The versions list.
            version : str
                The required version to order the dataset.
        
        Returns:
            pd.DataFrame
             The dataset with a new version registry, can be TX1 or TX2, it depends on the required version.
        """

        registry = registry.to_frame().T
        registry['FechaPublicacion'] = pd.to_datetime(registry['FechaPublicacion'])

        if version == 'TX2':
            date = registry['FechaPublicacion'] - pd.Timedelta(days=1)
            order = orders.min()-1
        elif version == 'TX1':
            date = registry['FechaPublicacion'] - pd.Timedelta(days=2)
            order = orders.min()-2

        new_registry = {
            'Version' : version,
            'FechaInicio' : registry['FechaInicio'].values[0],
            'FechaFin' : registry['FechaFin'].values[0],
            'FechaPublicacion' : pd.to_datetime(date.values[0]).date(),
            'EsMaximaVersion' : 0,
            'order' : order
        }

        new_registry_df = pd.DataFrame([new_registry])
        dataset = pd.concat([dataset, new_registry_df], ignore_index=True)

        return dataset

    @staticmethod
    def _filter_by_version(dataset: pd.DataFrame, version_value: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Groups a data set by months and applies filtering to them by a version value.
        
        Parameters:
            dataset : pd.DataFrame
                The dataset to filter.
            version_value : str
                The filter value.
        
        Returns:
            pd.DataFrame
             The dataset filtered by the version value.
        """

        dataset = VariableSIMEM._generate_missing_months(dataset=dataset, start_date=start_date, end_date=end_date)
        version_column = version_column_df_ver
        order_column = 'order'
        filtered_df = dataset.groupby('month', group_keys=False).apply(lambda month_data: VariableSIMEM._filter_group_by_version(
            month_data, version_column, order_column, version_value), include_groups=False).reset_index(drop=True)
    
        return filtered_df
    
    @staticmethod
    def _filter_group_by_version(month_data: pd.DataFrame, version_column: str, order_column: str, version_value: str):
        """
        Filters a DataFrame by a specific value in the 'version' column, returning the rows that match 
        that value within each 'month' group.
        
        Parameters:
            month_data : pd.DataFrame
                The dataset of a specific month.
            version_column : str
                The name of the column that contain the version.
            order_column : str
                The name of the column that contain the order.
            order_value : str
                The filter value.
        
        Returns:
            pd.DataFrame
             The dataset filtered by the version value.
        """

        if not {'TX1', 'TX2'}.intersection(month_data[version_column].values):
            last_registry = VariableSIMEM._get_last_registry(month_data)
            if version_value == 'TX2':
                month_data = VariableSIMEM._set_order_version(dataset=month_data, registry=last_registry, orders=month_data[order_column], version='TX2')
            elif version_value == 'TX1':
                month_data = VariableSIMEM._set_order_version(dataset=month_data, registry=last_registry, orders=month_data[order_column], version='TX1')

        return month_data[month_data[version_column] == version_value]

    @staticmethod
    def _generate_missing_months(dataset: pd.DataFrame, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Calculate the missing data for the months within the version dataset.
        
        Parameters:
            dataset : pd.DataFrame
                The dataset with the versions.
            start_date: str | dt.datetime
                Start date of the dataset.
            end_date : str | dt.datetime
                End date of the dataset.
        
        Returns:
            pd.DataFrame
             The full version dataset with missing data.
        """

        all_months = set(pd.date_range(start=start_date, end=end_date, freq='MS').strftime("%Y-%m-%d"))
        existing_months = set(dataset['FechaInicio'])
        missing_months = list(all_months - existing_months)
        
        if missing_months:
            missing_data = pd.concat(list(map(VariableSIMEM._process_month, missing_months)), ignore_index=True)
            dataset = pd.concat([dataset, missing_data], ignore_index=True)
        
        return dataset
    
    @staticmethod
    def _process_month(month: str) ->pd.Series:
        """
        Reads data for a specific month and sorts it by publication date.
        
        Parameters:
            month : str
                The start date of a month.
        
        Returns:
            pd.series
             The data of the month sorted.
        """

        first_day_of_month = pd.to_datetime(month)
        last_day_of_month = first_day_of_month + pd.offsets.MonthEnd(0)
        daily_df = ReadSIMEM(daily_dataset_id, first_day_of_month.strftime("%Y-%m-%d"), last_day_of_month.strftime("%Y-%m-%d")).main()
        daily_df = VariableSIMEM._order_date(dataset=daily_df, date_column='FechaPublicacion')

        return daily_df
    
    @staticmethod
    def _versions(start_date: str, end_date: str, dataset_id: str, version: str | int, esTX2: bool) -> pd.DataFrame:
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
            esTX2 | bool
                The value is 1 if the first version is TX2 and 0 if it is TX1.
        
        Returns:
            pd.DataFrame
             The variable dataset filtered by a version.
        """

        first_day = start_date.replace(day=1)
        version_df = ReadSIMEM(dataset_id, first_day, end_date).main()
        version_df = VariableSIMEM._validate_version_df(version_df=version_df, first_date=first_day)
        df_sorted = VariableSIMEM._order_date(dataset=version_df, date_column='FechaPublicacion')
        
        if isinstance(version, str):
            df_filtered = VariableSIMEM._filter_by_version(dataset=df_sorted, version_value=version, start_date=first_day, end_date=end_date)
        elif isinstance(version, int):
            df_filtered = VariableSIMEM._filter_by_order(dataset=df_sorted, order_value=version, start_date=first_day, end_date=end_date, esTX2=esTX2)

        return df_filtered

    @staticmethod
    def _validate_version_df(version_df: pd.DataFrame, first_date: str) -> pd.DataFrame:
        """
        Validates if the version dataset is empty.
        
        Parameters:
            version_df : pd.DateFrame
                Version dataset.
            first_date : str | dt.datetime
                First day of the month sought.
        
        Returns:
            pd.DataFrame
             Returns the original dataset if it is not empty, otherwise it returns a dummy record from the previous month.
        """

        if len(version_df) == 0:
            last_month = (first_date.replace(day=1) - timedelta(days=1)).replace(day=1)
            new_registry = {
                'Version' : '0',
                'FechaInicio' : last_month.strftime("%Y-%m-%d"),
                'FechaFin' : last_month.strftime("%Y-%m-%d"),
                'FechaPublicacion' : last_month.strftime("%Y-%m-%d"),
                'EsMaximaVersion' : 0
            }
            new_registry_df = pd.DataFrame([new_registry])
            version_df = pd.concat([version_df, new_registry_df], ignore_index=True)
        return version_df
    
    @staticmethod
    def _filter_date(dataset: pd.DataFrame, dates_df: pd.DataFrame, date_column: str, version_column: str) -> pd.DataFrame:
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
        index_names = dataset.index.names
        dataset.reset_index(inplace=True)
        dataset = dataset.rename(columns={date_column: date_temp})
        dataset = dataset.merge(dates_df, left_on = version_column, right_on = 'Version')
        dataset['FechaFin'] = pd.to_datetime(dataset['FechaFin'])
        dataset = dataset[(dataset[date_temp] >= dataset['FechaInicio']) & (dataset[date_temp] < dataset['FechaFin']+pd.Timedelta(days=1))]
        dataset = dataset.drop(columns = ['FechaInicio', 'FechaFin', 'FechaPublicacion', 'EsMaximaVersion', 'order'])
        dataset = dataset.rename(columns = {date_temp: date_column})
        dataset.set_index(index_names, inplace=True)

        return dataset

    def _calculate_version(self, dataset: pd.DataFrame, version: int | str) -> pd.DataFrame:
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
        version_column = self._version_column
        date_column = self._date_column
        
        if self.__versions_df is None:
            self.__versions_df = VariableSIMEM._versions(start_date=self._start_date, end_date=self._end_date, 
                                                          dataset_id=version_dataset_id, version=version, esTX2 = self.__esTX2)
        filtered_df = self.__versions_df

        return VariableSIMEM._filter_date(df, filtered_df, date_column, version_column)
    
    def __calculate_stats(self, dataset: pd.DataFrame, column: str) -> dict:
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
            'start_date': pd.to_datetime(self._start_date).strftime('%Y-%m-%d'),
            'end_date': pd.to_datetime(self._end_date).strftime('%Y-%m-%d'),
            'granularity': self.__granularity
            }
        return stats

    def describe_data(self) -> dict:
        """
        Generates statistics for the variable.
        
        Returns:
            dic
             Dictionary with the statistics values of the variable.
        """

        statistics = {}
        self._read_dataset_data(start_date=self._start_date, end_date=self._end_date)
        data = self._index_df(dataset=self._data)
        column = self._value_column
        name = self._json_file[self._var]['name']
        data[column] = data[column].astype(float)

        if self._version_column is not None:
            data = self._calculate_version(dataset=data, version=self.__user_version)
            data = data[[column]]
            data = data.groupby([self._date_column, self._version_column]).sum()
        statistics[name] = self.__calculate_stats(dataset=data, column=column)

        return statistics

class MaestraSIMEM(VariableSIMEM):
    """
    Class to view the information of a SIMEM maestra.

    Args: 
    maestra : str
        Code of the maestra.
    start_date : str | dt.datetime 
        The starting date for the data slicing.
    end_date : str | dt.datetime 
        The ending date for the data slicing.
    
    Methods:
    get_collection() -> pd.DataFrame:
        Return a dataframe with the list of available maestras.
    """

    def __init__(self, maestra: str, start_date: str, end_date: str):
        self._json_file = VariableSIMEM._read_json()
        self._json_file = self._json_file['maestra']
        self._var = _Validation.cod_variable(cod_variable=maestra, list_variables=self._json_file, type='maestra')
        self._dataset_id = self._json_file[self._var]["dataset_id"]
        self._variable_column = self._json_file[self._var]['var_column']
        self._date_column = self._json_file[self._var]['date_column']
        self._version_column = self._json_file[self._var]['version_column']
        self._value_column = self._json_file[self._var]['value_column']
        self._dimensions = self._json_file[self._var]['dimensions']
        self._start_date = _Validation.date(start_date)
        self._end_date = _Validation.date(end_date)
        self._quality_check = None
        self._data = None
    
    @staticmethod
    def get_collection() -> pd.DataFrame:
        """
        Return a dataframe with the list of available maestras.
        
        Returns:
            pd.DataFrame
                Contains the list of available maestras.
        """
        
        json_file = VariableSIMEM._read_json()
        df =  pd.DataFrame.from_dict(json_file['maestra'], orient='index', columns=['name', 'dimensions']).reset_index().rename(
            columns={'index': 'Maestra', 'name': 'Descripción', 'dimensions': 'Cruces'})
 
        return df
#%%
if __name__ == '__main__':

    dataset_id = 'c41fe8'
    fecha_inicio = '2025-02-01'
    fecha_fin = '2025-02-10'
    variables = VariableSIMEM.get_collection()
    pb_nal_tx1 = VariableSIMEM(cod_variable="PB_Nal", start_date=fecha_inicio, end_date=fecha_fin, version='TXF')
    pb_nal_tx2 = VariableSIMEM(cod_variable="PB_Nal", start_date=fecha_inicio, end_date=fecha_fin, version='TX2')

#%%
    pb_nal_tx1.get_data()
    pb_nal_tx1.describe_data()

#%%
    pb_nal_tx2.get_data()
    pb_nal_tx2.describe_data()

#%%
    simem = ReadSIMEM(dataset_id, fecha_inicio, fecha_fin, 'CodigoVariable', 'GReal')
    df = simem.main(output_folder="", filter=False)