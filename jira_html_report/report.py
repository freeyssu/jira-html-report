
from typing import List, Optional
import logging
import logging.handlers
import base64
from io import BytesIO

# external libs
from pandas import DataFrame
import plotly.express as px
from plotly.graph_objs import Figure
from jinja2 import Template

# package libs
from jira_html_report.data import JiraDataHandler


class HTMLReport(JiraDataHandler):
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
        super().__init__(server=server, username=username, password=password, logger=logger, debug=debug, **kwargs)

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

    def generate_html_chart(self, figure: Figure, html_template_path: str, div_class_name: str = 'chart',
                            static_chart: bool = False) -> str:
        """Generate HTML page with the provided Figure object

        Args:
            figure (Figure): plotly.graph_objs.Figure object.
            div_class_name (str, optional): <div> class name includes chart for CSS style. Defaults to 'chart'.
            static_chart (bool, optional): If True, generate static image instead of jQury chart. Defaults to False.

        Returns:
            str: Rendered HTML codes
        """

        with open(html_template_path, 'r') as f:
            chart_template = Template(f.read())
        if static_chart:
            figure_buf = BytesIO()
            figure.write_image(figure_buf, format='jpeg')
            figure_buf.seek(0)
            base64_img = base64.b64encode(figure_buf.read()).decode()
            return chart_template.render(div_class_name=div_class_name, base64_img=base64_img)
        else:
            return chart_template.render(div_class_name=div_class_name, figure=figure)

    def generate_html_table(self, df: DataFrame, table_template_path: str, div_class_name: str = 'table') -> str:
        """Generates an HTML table from a DataFrame using a Jinja2 template.

        Args:
            df (DataFrame): The DataFrame containing the data to be rendered in the HTML table.
            div_class_name (str, optional): The CSS class name to be applied to the div containing the table. \
                Defaults to 'table'.

        Returns:
            str: Rendered HTML codes
        """

        with open(table_template_path, 'r') as f:
            table_template = Template(f.read())
        return table_template.render(df=df, div_class_name=div_class_name)

    def generate_html_report(self, report_template_path: str, html_charts: Optional[List[str]] = None,
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

        with open(report_template_path, 'r') as f:
            report_template = Template(f.read())
        return report_template.render(html_charts=html_charts, html_tables=html_tables, **kwargs)

