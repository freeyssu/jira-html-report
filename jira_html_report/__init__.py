import importlib.metadata
from jira_html_report.report import HTMLReport
from jira_html_report.data import JiraDataHandler

try:
    __version__ = importlib.metadata.version("jira_html_report")
except Exception:
    __version__ = "unknown"


__all__ = (
    'HTMLReport',
    'JiraDataHandler'
)
