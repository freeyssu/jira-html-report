import importlib.metadata
from jira_report.report import HTMLReport
from jira_report.data import JiraDataHandler

try:
    __version__ = importlib.metadata.version("jira_report")
except Exception:
    __version__ = "unknown"


__all__ = (
    'HTMLReport',
    'JiraDataHandler'
)
