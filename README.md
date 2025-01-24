# Jira HTML Report

`jira-html-report` is a Python script designed to generate reports from Jira. This script allows you to fetch and process data from your Jira projects, providing insights and summaries that can help you manage your projects more effectively.

## Features
- HTML report with charts and table sheet
- Fetch data from Jira projects
- Generate summary reports
- Customizable report formats
- Easy to use and configure

## Sample charts and table
<img src="https://github.com/freeyssu/jira-html-report/raw/main/chart.png" alt="Charts" width="1000" style="border: 1px solid black;"/>
<br>
<img src="https://github.com/freeyssu/jira-html-report/raw/main/table.png" alt="Table" style="border: 1px solid black;"/>

## Requirements

- Python 3.x
- Python external packages
```
jira
plotly
pandas
jinja2
```

## Installation

- Clone the repository:
    ```sh
    git clone https://github.com/freeyssu/jira-html-report.git
    cd jira-html-report
    pip install -r requirements.txt
    ```

- Pypi package management:
    ```sh
    pip install jira-html-report
    ```


## Directory and files
```
.
├── jira_html_report/
│   ├── html_templates/
│   │   ├── chart_templates.j2
│   │   ├── report_templates.j2
│   │   └── table_templates.j2
│   ├── data.py
│   └── report.py
└── samples/
    ├── sample.html
    ├── sample.ipynb
    └── sa,ple.py
```


## Usage

1. Initialize HTMLReport instance
```python
from jira_html_report import HTMLReport
html_report = HTMLReport(server='https://YOUR_JIRA_SERVER', username=USERNAME password=PASSWORD)
```

2. Query Jira items by `JQL` then generate Pandas `DataFrame`
```python
jql = 'Project = TEST AND created > -7d'

# define fields what you extract from the queried Jira items
fields_for_charts = [
    'customfield_1000',     # custom fields
    'customfield_2000',     # what you want to get
    'customfield_3000',     # you should put field-id
    'status',
    'assignee',
    'reporter',
    'priority',
    'components'
]
fields_for_table = [
    'customfield_4000',     # you can add/remove any field for chart or table
    'status',
    'assignee'
]

# generate main DataFrame and sub DataFrames for chart.
# sub DataFrames are grouped by the selected fields and counted the rows. it has two columns (field name and Count)
chart_df, chart_sub_dfs = html_report.generate_dataframes_by_jql(jql=jql, fields=fields_for_charts, jql_search_limit=100)
table_df, table_sub_dfs = html_report.generate_dataframes_by_jql(jql=jql, fields=fields_for_table, jql_search_limit=100)

########################################################
# do something here to update the main or sub dataframes
# e.g. update column name
########################################################
```

3. Draw charts
```python
figures = {}
for field_name, sub_df in sub_dfs.items():
    figures[field_name] = html_report.generate_chart_figure(
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
```

4. Generate HTML code blocks for chart and table sheet
```python
# generate HTML code block for charts
html_charts = {}
for field_name, figure in figures.items():
    html_charts[field_name] = html_report.generate_html_chart(figure=figure, static_chart=True)

# generate HTML code block for table
html_table = html_report.generate_html_table(df=table_df)
```

5. Generate HTML report
```python
html_report = html_report.generate_html_report(html_charts=html_charts, html_table=html_table)
with open('jira_report.html', 'wb') as f:
    f.write(html_report.encode())
```

## HTML template modification
There are three Jinja2 templates under `html_templates` dir to generate a HTML report. You can modify or add any HTML properties/Python vars.

1. Add/update vars or properties in Jinja2 template
```html
<!-- add <h2> tag to html_templates/report_template.j2 -->
<h2> {{ new_h2_string_in_report }} </h2>
```

2. Populate the vars
```python
html_report = html_report.generate_html_report(html_charts=html_charts, html_table=html_table, new_h2_string_in_report="ADDED NEW H2 STRING")
```