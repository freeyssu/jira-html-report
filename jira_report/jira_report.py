
from typing import List, Optional, Dict, Tuple, Any
import logging
import logging.handlers
import base64
from io import BytesIO

# external libs
from pandas import DataFrame
import plotly.express as px
from plotly.graph_objs import Figure
import jira
import jira.resources
from jinja2 import Environment, FileSystemLoader


class JiraReport():
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
        self.jinja_env = Environment(loader=FileSystemLoader('html_templates'))

    def generate_chart_figure(self, df: DataFrame, chart_type: str = 'bar', chart_title: Optional[str] = None,
                              **kwargs) -> Figure:
        """Draw chart by the provided DataFrame

        Args:
            df (DataFrame): pandas.DataFrame object for dataset.
            chart_type (str, optional): Chart type - https://plotly.com/python-api-reference/plotly.express.html. \
                Defaults to 'bar'.
            chart_title (Optional[str], optional): Chart title. Defaults to None.
            **kwargs (Dict, optional): Use any kwargs for each type of plotly.express.[] chart instance. \
                Especially, some args like x, y in bar chart are essential.
                Refer to the specific chart API and requried args from \
                https://plotly.com/python-api-reference/plotly.express.html

        Returns:
            Figure: plotly.graph_objs.Figure object. \
                https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html
        """

        assert chart_type in dir(px._chart_types), f'chart_type {chart_type} is not supported.'
        func = getattr(px, chart_type)
        return func(data_frame=df, title=chart_title, color=df.columns[0], **kwargs)

    def generate_html_chart(self, figure: Figure, div_class_name: str = 'chart', static_chart: bool = False) -> str:
        """Generate HTML page with the provided Figure object

        Args:
            figure (Figure): plotly.graph_objs.Figure object.
            div_class_name (str, optional): <div> class name includes chart for CSS style. Defaults to 'chart'.
            static_chart (bool, optional): If True, generate static image instead of jQury chart. Defaults to False.

        Returns:
            str: Rendered HTML codes
        """

        chart_template = self.jinja_env.get_template('chart_template.j2')
        if static_chart:
            figure_buf = BytesIO()
            figure.write_image(figure_buf, format='jpeg')
            figure_buf.seek(0)
            base64_img = base64.b64encode(figure_buf.read()).decode()
            return chart_template.render(div_class_name=div_class_name, base64_img=base64_img)
        else:
            return chart_template.render(div_class_name=div_class_name, figure=figure)

    def generate_html_table(self, df: DataFrame, div_class_name: str = 'table', **kwargs) -> str:
        """Generates an HTML table from a DataFrame using a Jinja2 template.

        Args:
            df (DataFrame): The DataFrame containing the data to be rendered in the HTML table.
            div_class_name (str, optional): The CSS class name to be applied to the div containing the table. \
                Defaults to 'table'.

        Returns:
            str: Rendered HTML codes
        """

        table_template = self.jinja_env.get_template('table_template.j2')
        return table_template.render(df=df, div_class_name=div_class_name)

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

    def generate_html_report(self, html_charts: Optional[List[str]] = None,
                             html_tables: Optional[List[str]] = None,
                             **kwargs) -> str:
        """Generates an HTML report using the provided charts and tables.
        Args:
            html_charts (Optional[List[str]]): A list of HTML strings representing charts to be included in the report.
            html_tables (Optional[List[str]]): A list of HTML strings representing tables to be included in the report.
            **kwargs: Additional keyword arguments to be passed to the template renderer.
        Returns:
            str: The rendered HTML report as a string.
        """

        report_template = self.jinja_env.get_template('report_template.j2')
        return report_template.render(html_charts=html_charts, html_tables=html_tables, **kwargs)
