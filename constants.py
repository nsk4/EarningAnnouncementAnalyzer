NAME = 0
FISCAL_YEAR = 1
CAP = 2
EST_EPS = 3
NUN_EPS = 4
EPS = 5

VOLUME = 0
HIGH = 1
LOW = 2
OPEN = 3
CLOSE = 4
ADJ_CLOSE = 5

EXDATE = 0
CASH_AMOUNT = 1
DECLARATION_DATE = 2
RECORD_DATE = 3
PAYMENT_DATE = 4

ORDER_SELL = -1
ORDER_NONE = 0
ORDER_BUY = 1


JUMP_THRESHOLD = 0.01  # used for previous jumps
EARNING_THRESHOLD = 0  # if absolute result is below threshold then it is considered as 0
CLASSIFY_RESULTS = False  # if set to true then try and predict the actual discrete earning jump. If set to false then Y table will contain [-1,0,1] values
CERTAINTY_BASED_TRADES = True  # if set to true then more certain trades will contain higher profit/loss factor
PREDICTION_THRESHOLD = 0.0  # Only used for CLASSIFY_RESULTS=False, if ML difference between buy and sell (excluding NONE) is smaller than threshold then do no not take the trade. TODO: change for analysis
JUMP_START = 0  # 0 is the open price on the day after the announcement
JUMP_END = 0  # 0 is the close price on the day after the announcement
# JUMP_START == JUMP_END -> open->close on the same day
# JUMP_START != JUMP_END -> JUMP_START open -> JUMP_END close
# time = 0 -> day after event, time = 1 -> 2 days after event

DISCRETE_JUMPS = [-0.5, -0.35, -0.25, -0.15, -0.07, -0.03, -0.01, 0, 0.01, 0.03, 0.07, 0.15, 0.25, 0.35, 0.5]


SIMULATOR_YEAR_START = 2018
SIMULATOR_YEAR_END = 2019

YEAR_FEATURE = 12
ML_SIMULATOR_YEAR = 2018

VERBOSE = False

# Used by machine_learning.py
STORE_CACHE = True  # store calculated ML tables
USE_CACHED_DATA = True  # read previously calculated ML tables - TODO: set to False for run reset

# Used by main.py
PROCESS_EARNING_ANNOUNCEMENTS = False
PROCESS_DIVIDEND_ANNOUNCEMENTS = False
PROCESS_TWEETS = False
USE_CACHED_TWEETS_DATA = False
RUN_SIMULATION = False
PROCESS_GOOGLE_TRENDS = False
RUN_MACHINE_LEARNING = True

DO_BASIC_PROCESSING = False  # reads company data - TODO: set to True for run reset
READ_DATA = True  # use precalculated ML tables - TODO: set to False for run reset
STORE_DATA = True  # store calculated tables
