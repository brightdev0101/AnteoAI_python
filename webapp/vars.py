DEV_MODE = True
AUTOMATION_SWITCH = False

# DB
SQL_DB = 'users.db'

# DATA ENTRYPOINT
DATA_ENTRYPOINT = "http://15.161.169.138/custom1593fggj9824515/"
TREND_ENTRYPOINT = "http://15.161.169.138/static/"

# STATS PARAMETERS
STATS_PARAMS = {
    "effective_distance": [0.7, 0.6, 0.5, 0.4, 0.35, 0.3, 0.25, 0.2, 0.15, 0.1, 0.05] ,
    "popular_scale": [5, 20, 50, 100, 200, 300, 400, 500, 700, 800, 1000] , 
    "interactive_scale": [1, 5, 10, 15, 20, 25, 30, 40, 50, 55, 60] , 
    "multimedial_scale": [1, 5, 10, 15, 20, 30, 40, 50, 60, 80, 100] ,
    "trend_scale": [0.2, 0.5, 1, 1.3, 1.4, 1.5, 1.8, 2, 2.5, 2.8, 3],
    "happiness" : [50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100],
    "sadness" : [40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90],
    "anger" : [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70],
    "fear" : [40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90],
    "disgust" : [40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90]
}

# DEFAULT CONFIG
DEFAULT_CT_CONFIG  = {
    "custom_config": {
        "alert_influencers": True, 
        "alert_sentiment": True, 
        "alert_trends": True, 
        "algorithm": 1, 
        "analysis_emoji": True, 
        "analysis_images": True, 
        "analysis_text": True, 
        "georeference": "it", 
        "keywords": "", 
        "language": "it", 
        "main_param": 1, 
        "plot1": "bar_sentiment", 
        "plot2": "bar_sentiment", 
        "plot3": "bar_sentiment", 
        "source_gogl": True, 
        "source_ig": True, 
        "source_tw": True, 
        "timeframe": 7,
        "report": 1}, 
    "custom_trend_id": 3, 
    "key": "Cybersecurity"
}

# ACCOUNT TYPES REFERENCE
ACCOUNT_TYPES = ["Basic", "PRO", "Enterprise"]

# ERROR STRINGS
ERROR_GENERAL = 'API Error'
ERROR_MISSING_PARAMS = 'One or more parameters missing from the request'
ERROR_API = 'API is not available or rate limit has exceeded'

# PATHS
DATA_DIR = 'data/'
CUSTOM_TREND_DIR = 'data/ct/'
IMGS_DIR = 'static/imgs/'
SITEMAP = 'static/sitemap.xml'

# STRINGS
SUCCESS_API = 'API response success'

