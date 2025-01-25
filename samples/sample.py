import pandas as pd
from jira_html_report import HTMLReport

jira_report = HTMLReport()

# We assume this is a dataset from JiraReport.generate_dataframes_by_jql
queried_jira_data = [
    {
        "Server Name": "Server-6",
        "Component": "RAM",
        "Failure Times": 7,
        "Vendor": "Intel",
    },
    {
        "Server Name": "Server-10",
        "Component": "Storage",
        "Failure Times": 2,
        "Vendor": "Kingston",
    },
    {
        "Server Name": "Server-3",
        "Component": "CPU",
        "Failure Times": 8,
        "Vendor": "Seagate",
    },
    {
        "Server Name": "Server-3",
        "Component": "CPU",
        "Failure Times": 4,
        "Vendor": "G.Skill",
    },
    {
        "Server Name": "Server-6",
        "Component": "Storage",
        "Failure Times": 2,
        "Vendor": "Seagate",
    },
    {
        "Server Name": "Server-10",
        "Component": "Storage",
        "Failure Times": 3,
        "Vendor": "Corsair",
    },
    {
        "Server Name": "Server-7",
        "Component": "CPU",
        "Failure Times": 7,
        "Vendor": "Corsair",
    },
    {
        "Server Name": "Server-2",
        "Component": "CPU",
        "Failure Times": 2,
        "Vendor": "Crucial",
    },
    {
        "Server Name": "Server-10",
        "Component": "CPU",
        "Failure Times": 6,
        "Vendor": "Kingston",
    },
    {
        "Server Name": "Server-9",
        "Component": "CPU",
        "Failure Times": 5,
        "Vendor": "Kingston",
    },
    {
        "Server Name": "Server-8",
        "Component": "CPU",
        "Failure Times": 8,
        "Vendor": "Western Digital",
    },
    {
        "Server Name": "Server-9",
        "Component": "Storage",
        "Failure Times": 10,
        "Vendor": "G.Skill",
    },
    {
        "Server Name": "Server-6",
        "Component": "RAM",
        "Failure Times": 2,
        "Vendor": "Corsair",
    },
    {
        "Server Name": "Server-7",
        "Component": "RAM",
        "Failure Times": 10,
        "Vendor": "Samsung",
    },
    {
        "Server Name": "Server-2",
        "Component": "RAM",
        "Failure Times": 0,
        "Vendor": "Seagate",
    },
    {
        "Server Name": "Server-10",
        "Component": "CPU",
        "Failure Times": 1,
        "Vendor": "Western Digital",
    },
    {
        "Server Name": "Server-10",
        "Component": "RAM",
        "Failure Times": 6,
        "Vendor": "Toshiba",
    },
    {
        "Server Name": "Server-1",
        "Component": "RAM",
        "Failure Times": 8,
        "Vendor": "Samsung",
    },
    {
        "Server Name": "Server-7",
        "Component": "Storage",
        "Failure Times": 10,
        "Vendor": "Corsair",
    },
    {
        "Server Name": "Server-8",
        "Component": "Storage",
        "Failure Times": 10,
        "Vendor": "Crucial",
    },
    {
        "Server Name": "Server-1",
        "Component": "Storage",
        "Failure Times": 5,
        "Vendor": "Western Digital",
    },
    {
        "Server Name": "Server-10",
        "Component": "RAM",
        "Failure Times": 4,
        "Vendor": "Intel",
    },
    {
        "Server Name": "Server-1",
        "Component": "RAM",
        "Failure Times": 1,
        "Vendor": "Crucial",
    },
    {
        "Server Name": "Server-2",
        "Component": "RAM",
        "Failure Times": 2,
        "Vendor": "Seagate",
    },
    {
        "Server Name": "Server-5",
        "Component": "Storage",
        "Failure Times": 10,
        "Vendor": "G.Skill",
    },
    {
        "Server Name": "Server-6",
        "Component": "CPU",
        "Failure Times": 7,
        "Vendor": "Crucial",
    },
    {
        "Server Name": "Server-3",
        "Component": "Storage",
        "Failure Times": 9,
        "Vendor": "Intel",
    },
    {
        "Server Name": "Server-1",
        "Component": "CPU",
        "Failure Times": 9,
        "Vendor": "Western Digital",
    },
    {
        "Server Name": "Server-2",
        "Component": "RAM",
        "Failure Times": 0,
        "Vendor": "Crucial",
    },
    {
        "Server Name": "Server-5",
        "Component": "Storage",
        "Failure Times": 5,
        "Vendor": "Samsung",
    },
    {
        "Server Name": "Server-7",
        "Component": "Storage",
        "Failure Times": 6,
        "Vendor": "Western Digital",
    },
    {
        "Server Name": "Server-1",
        "Component": "CPU",
        "Failure Times": 5,
        "Vendor": "Intel",
    },
    {
        "Server Name": "Server-7",
        "Component": "RAM",
        "Failure Times": 7,
        "Vendor": "Seagate",
    },
    {
        "Server Name": "Server-10",
        "Component": "CPU",
        "Failure Times": 4,
        "Vendor": "Crucial",
    },
    {
        "Server Name": "Server-4",
        "Component": "CPU",
        "Failure Times": 3,
        "Vendor": "G.Skill",
    },
    {
        "Server Name": "Server-1",
        "Component": "RAM",
        "Failure Times": 1,
        "Vendor": "Western Digital",
    },
    {
        "Server Name": "Server-10",
        "Component": "CPU",
        "Failure Times": 0,
        "Vendor": "Kingston",
    },
    {
        "Server Name": "Server-8",
        "Component": "Storage",
        "Failure Times": 4,
        "Vendor": "Crucial",
    },
    {
        "Server Name": "Server-10",
        "Component": "RAM",
        "Failure Times": 10,
        "Vendor": "Western Digital",
    },
    {
        "Server Name": "Server-9",
        "Component": "CPU",
        "Failure Times": 5,
        "Vendor": "Samsung",
    },
    {
        "Server Name": "Server-3",
        "Component": "RAM",
        "Failure Times": 3,
        "Vendor": "Samsung",
    },
    {
        "Server Name": "Server-8",
        "Component": "Storage",
        "Failure Times": 4,
        "Vendor": "AMD",
    },
    {
        "Server Name": "Server-5",
        "Component": "RAM",
        "Failure Times": 8,
        "Vendor": "Western Digital",
    },
    {
        "Server Name": "Server-7",
        "Component": "Storage",
        "Failure Times": 6,
        "Vendor": "Corsair",
    },
    {
        "Server Name": "Server-3",
        "Component": "CPU",
        "Failure Times": 3,
        "Vendor": "Seagate",
    },
    {
        "Server Name": "Server-4",
        "Component": "RAM",
        "Failure Times": 9,
        "Vendor": "Crucial",
    },
    {
        "Server Name": "Server-6",
        "Component": "RAM",
        "Failure Times": 10,
        "Vendor": "Seagate",
    },
    {
        "Server Name": "Server-2",
        "Component": "CPU",
        "Failure Times": 6,
        "Vendor": "AMD",
    },
    {
        "Server Name": "Server-5",
        "Component": "CPU",
        "Failure Times": 5,
        "Vendor": "Kingston",
    },
    {
        "Server Name": "Server-5",
        "Component": "CPU",
        "Failure Times": 1,
        "Vendor": "Intel",
    },
]
chart_df = pd.DataFrame(queried_jira_data)
chart_sub_dfs = {}
for i in chart_df.columns:
    chart_sub_dfs[i] = jira_report.generate_groupby_count_dataframe(df=chart_df, groupby=i)
table_df = pd.DataFrame(queried_jira_data)

########################################################
# do something here to update the main or sub dataframes
# e.g. update column name in table_df
########################################################

figures = {}
for field_name, sub_df in chart_sub_dfs.items():
    figures[field_name] = jira_report.generate_chart_figure(
        df=sub_df,
        chart_type='bar',
        chart_title=f'{sub_df.columns[0]} Status',
        x=sub_df.columns[0],
        y=sub_df.columns[1])

########################################################
# do something here to update chart properties
# figures['customfield_1000'].update_layout(...)
# figures['assignee'].update_traces(...)
# figures['field_x'] ...
########################################################

# generate HTML code block for charts
html_charts = {}
for field_name, figure in figures.items():
    # used static_chart=True to display HTML on Jupyter notebook
    html_charts[field_name] = jira_report.generate_html_chart(
        figure=figure, html_template_path='../jira_report/html_templates/chart_template.j2')

# generate HTML code block for table
html_table = jira_report.generate_html_table(
    df=table_df, table_template_path='../jira_report/html_templates/table_template.j2',)

# generate report and save it to file
html_report = jira_report.generate_html_report(
    report_template_path='../jira_report/html_templates/report_template.j2', html_charts=html_charts,
    html_table=html_table)
with open('sample.html', 'wb') as f:
    f.write(html_report.encode())
