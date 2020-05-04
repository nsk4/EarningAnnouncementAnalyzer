# Earning announcements
ANNOUNCEMENT_TIME = 0
ANNOUNCEMENT_EST_EPS = 1
ANNOUNCEMENT_EPS = 2
ANNOUNCEMENT_SURPRISE = 3

# Stock prices
VOLUME = 0
HIGH = 1
LOW = 2
OPEN = 3
CLOSE = 4
ADJ_CLOSE = 5

# Dividend announcements
EXDATE = 0
CASH_AMOUNT = 1
DECLARATION_DATE = 2
RECORD_DATE = 3
PAYMENT_DATE = 4

# Simulator enum
ORDER_SELL = -1
ORDER_NONE = 0
ORDER_BUY = 1


JUMP_THRESHOLD = 0.01  # used for price jump in features
EARNING_THRESHOLD = 0  # if absolute result is below threshold then it is considered as 0

# For multiple day trade
JUMP_START = 0  # 0 is the open price on the day after the announcement
JUMP_END = 0  # 0 is the close price on the day after the announcement
# JUMP_START == JUMP_END -> open->close on the same day
# JUMP_START != JUMP_END -> JUMP_START open -> JUMP_END close
# time = 0 -> day after event, time = 1 -> 2 days after event

# Used for simulation
SIMULATOR_YEAR_START = 2018
SIMULATOR_YEAR_END = 2019


# Data loading and processing
PROCESS_TWEETS = False
PROCESS_GOOGLE_TRENDS = False
PROCESS_HISTORICAL_PRICES = True
PROCESS_DIVIDEND_ANNOUNCEMENTS = False
PROCESS_EARNING_ANNOUNCEMENTS = False  # can be set to false if using cached ML data

USE_CACHED_TWEETS_DATA = False
USE_CACHED_GOOGLE_TRENDS = False
USE_CACHED_MACHINE_LEARNING_DATA = not PROCESS_EARNING_ANNOUNCEMENTS  # read previously calculated ML tables - TODO: set to False for run reset - must do when changing CLASSIFY_RESULTS

STORE_DATA = True  # store calculated tables

# Used by machine_learning.py
CLASSIFY_RESULTS = False  # if set to true then try and predict the actual discrete earning jump. If set to false then Y table will contain [-1,0,1] values
DISCRETE_JUMPS = [-0.5, -0.35, -0.25, -0.15, -0.07, -0.03, -0.01, 0, 0.01, 0.03, 0.07, 0.15, 0.25, 0.35, 0.5]  # used with CLASSIFY_RESULTS

CERTAINTY_BASED_TRADES = True  # if set to true then more certain trades will contain higher profit/loss factor - for CLASSIFY_RESULTS use DISCRETE_JUMPS and for others use prediction probability
PREDICTION_THRESHOLD = 0.0  # Only used for CLASSIFY_RESULTS=False, if ML difference between buy and sell (excluding NONE) is smaller than threshold then do no not take the trade.

YEAR_FEATURE = 12
VERBOSE = True

# Run simulation or machine learning
RUN_SIMULATION = False
RUN_MACHINE_LEARNING = True




