from datetime import datetime

current_date = datetime.now()

APP_NAME = 'WhatsApp Chat Analyzer'

TRAFFIC_FILE_PATH = 'traffic.txt'

FEEDBACK_FILE_PATH = 'feedbacks.txt'

DATETIME_FORMATS = [
    'Date Format',
    f"{current_date.strftime('%m/%d/%y')} (M/D/Y)",
    f"{current_date.strftime('%d/%m/%Y')} (D/M/Y)",
]

DATETIME_FORMATS_PREPROCESS = [
    '',
    '%m/%d/%y, %H:%M - ',
    '%d/%m/%Y, %H:%M - ',
]

TOP_NAV_HEADERS = [
    "Top Users",
    "Activity",
    "Timeline",
    "Feedback",
]

TOP_NAV_ICONS = ["star", "bar-chart", "graph-up", "person"]