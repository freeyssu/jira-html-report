
from typing import List, Optional, Dict, Tuple, Any
import logging
import logging.handlers

# external libs
from pandas import DataFrame
import jira
import jira.resources


class JiraDataHandler():
    def __init__(self, server: str = None, username: Optional[str] = None, password: Optional[str] = None,
                 logger: Optional[logging.Logger] = None, debug=False, **kwargs):
        """JiraReport provides generating html report with charts and a table.

        Args:
            server (str, optional): Jira server URL, Defaults to None.
            username (Optional[str]): username for basic auth. Defaults to None.
            password (Optional[str]): password for basic auth. Defaults to None.
            logger (Optional[logging.Logger]): Logger. Defaults to None.
            debug (bool, optional): logger level will be DEBUG. Defaults to False.
            **kwargs (Dict, optional): Use any kwargs for jira.JIRA class
        """
        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger(self.__class__.__name__)
            self.logger_formatter = logging.Formatter(
                '%(asctime)s | %(name)s | %(levelname)s | %(funcName)s | %(message)s')
            self.logger_stream_handler = logging.StreamHandler()
            self.logger_stream_handler.setFormatter(self.logger_formatter)
            self.logger.addHandler(self.logger_stream_handler)
            self.logger.propagate = False
        self.logger.setLevel(logging.DEBUG if debug else logging.INFO)

        if server:
            self.jira_api = jira.JIRA(server=server, basic_auth=(username, password), **kwargs)

    def generate_dataframes_by_jql(self, jql: str, fields: List[str],
                                   jql_search_limit: int = 100, **kwargs) -> Tuple[DataFrame, Dict[str, DataFrame]]:
        """Query Jira by the provided jql then generate pandas.DataFrame dataset

        Args:
            jql (str): Jira Query Language(JQL)
            fields (List[str]): Field ID that you want to get.
            jql_search_limit (int, optional): Query limitation. Defaults to 100.
            **kwargs (Dict, optional): Use kwargs for jira.search_issues if you need.

        Returns:
            Tuple[DataFrame, Dict[str, DataFrame]]: Two groups of DataFrame are returned as Tuple.
                DataFrame all query data included and field name : DataFrame groupby the field.
                (all DataFrame, {field name: DataFrame groupby field name, ...})
        """

        def extract_value(field: Dict[str, Any]):
            if field is None:
                'N/A'
            elif type(field) in [str, int, float]:
                return field
            elif type(field) is dict and field.get('value'):    # jira.resources.CustomFieldOption
                return field['value']
            elif type(field) is dict and field.get('name'):     # common jira.resources
                return field['name']
            elif type(field) is list:
                return ', '.join([extract_value(i) for i in field])
            else:
                raise Exception(f'{field} type of field is not supported. Need to add a logic to extract a value.')

        all_jira_fields = {i['id']: i for i in self.jira_api.fields()}
        df = []
        for issue in self.jira_api.search_issues(jql_str=jql, fields=fields, json_result=True,
                                                 maxResults=jql_search_limit, **kwargs)['issues']:
            df.append({
                all_jira_fields[k]['name']: extract_value(v) for k, v in issue['fields'].items()
            })
        df = DataFrame(df)

        groupby_dfs = {}
        for i in df.columns:
            groupby_dfs[i] = self.generate_groupby_count_dataframe(df=df, groupby=i)

        return (df, groupby_dfs)

    def generate_groupby_count_dataframe(self, df: DataFrame, groupby: str, count_column_name='Count') -> DataFrame:
        """Generate DataFrame which includes two columns - the target field for groupby and size()

        Args:
            df (DataFrame): The DataFrame containing the data.
            groupby (str): Target field name which you want to count rows.
            count_column_name (str, optional): The name of new column for counting rows. Defaults to 'Count'.

        Returns:
            DataFrame
        """

        return df.groupby(groupby).size().reset_index(name=count_column_name)
