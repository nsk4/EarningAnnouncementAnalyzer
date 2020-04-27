import csv
import statistics
import numpy as np
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

import constants
import utilities


def run_machine_learning(x_data, y_data, trades, simulation_year=constants.ML_SIMULATOR_YEAR):
    if not constants.USE_CACHED_DATA:
        # 1) Define data encoding - OneHotEncoder
        if constants.VERBOSE:
            print("Defining categories")
        binary = [0, 1]
        triary = [-1, 0, 1]
        days = list(range(1, 32))
        months = list(range(1, 13))
        years = list(range(2014, 2020))
        all_tickers = ["A", "AAL", "AAP", "AAPL", "ABBV", "ABC", "ABMD", "ABT", "ACN", "ADBE", "ADI", "ADM", "ADP",
                       "ADS",
                       "ADSK", "AEE", "AEP", "AES", "AFL", "AGN", "AIG", "AIV", "AIZ", "AJG", "AKAM", "ALB", "ALGN",
                       "ALK",
                       "ALL", "ALLE", "ALXN", "AMAT", "AMD", "AME", "AMG", "AMGN", "AMP", "AMT", "AMZN", "ANET", "ANSS",
                       "ANTM", "AON", "AOS", "APA", "APC", "APD", "APH", "APTV", "ARE", "ARNC", "ATVI", "AVB", "AVGO",
                       "AVY", "AWK", "AXP", "AZO", "BA", "BAC", "BAX", "BBT", "BBY", "BDX", "BEN", "BF-B", "BHF",
                       "BHGE",
                       "BIIB", "BK", "BKNG", "BLK", "BLL", "BMY", "BR", "BRK-B", "BSX", "BWA", "BXP", "C", "CAG", "CAH",
                       "CAT", "CB", "CBOE", "CBRE", "CBS", "CCI", "CCL", "CDNS", "CE", "CELG", "CERN", "CF", "CFG",
                       "CHD",
                       "CHRW", "CHTR", "CI", "CINF", "CL", "CLX", "CMA", "CMCSA", "CME", "CMG", "CMI", "CMS", "CNC",
                       "CNP",
                       "COF", "COG", "COO", "COP", "COST", "COTY", "CPB", "CPRI", "CPRT", "CRM", "CSCO", "CSX", "CTAS",
                       "CTL", "CTSH", "CTXS", "CVS", "CVX", "CXO", "D", "DAL", "DE", "DFS", "DG", "DGX", "DHI", "DHR",
                       "DIS", "DISCA", "DISCK", "DISH", "DLR", "DLTR", "DOV", "DRE", "DRI", "DTE", "DUK", "DVA", "DVN",
                       "DWDP", "DXC", "EA", "EBAY", "ECL", "ED", "EFX", "EIX", "EL", "EMN", "EMR", "EOG", "EQIX", "EQR",
                       "ES", "ESS", "ETFC", "ETN", "ETR", "EVRG", "EW", "EXC", "EXPD", "EXPE", "EXR", "F", "FANG",
                       "FAST",
                       "FB", "FBHS", "FCX", "FDX", "FE", "FFIV", "FIS", "FISV", "FITB", "FL", "FLIR", "FLR", "FLS",
                       "FLT",
                       "FMC", "FOX", "FOXA", "FRC", "FRT", "FTI", "FTNT", "FTV", "GD", "GE", "GILD", "GIS", "GLW", "GM",
                       "GOOG", "GOOGL", "GPC", "GPN", "GPS", "GRMN", "GS", "GT", "GWW", "HAL", "HAS", "HBAN", "HBI",
                       "HCA",
                       "HCP", "HD", "HES", "HFC", "HIG", "HII", "HLT", "HOG", "HOLX", "HON", "HP", "HPE", "HPQ", "HRB",
                       "HRL", "HRS", "HSIC", "HST", "HSY", "HUM", "IBM", "ICE", "IDXX", "IFF", "ILMN", "INCY", "INFO",
                       "INTC", "INTU", "IP", "IPG", "IPGP", "IQV", "IR", "IRM", "ISRG", "IT", "ITW", "IVZ", "JBHT",
                       "JCI",
                       "JEC", "JEF", "JKHY", "JNJ", "JNPR", "JPM", "JWN", "K", "KEY", "KEYS", "KHC", "KIM", "KLAC",
                       "KMB",
                       "KMI", "KMX", "KO", "KR", "KSS", "KSU", "L", "LB", "LEG", "LEN", "LH", "LIN", "LKQ", "LLL",
                       "LLY",
                       "LMT", "LNC", "LNT", "LOW", "LRCX", "LUV", "LW", "LYB", "M", "MA", "MAA", "MAC", "MAR", "MAS",
                       "MAT",
                       "MCD", "MCHP", "MCK", "MCO", "MDLZ", "MDT", "MET", "MGM", "MHK", "MKC", "MLM", "MMC", "MMM",
                       "MNST",
                       "MO", "MOS", "MPC", "MRK", "MRO", "MS", "MSCI", "MSFT", "MSI", "MTB", "MTD", "MU", "MXIM", "MYL",
                       "NBL", "NCLH", "NDAQ", "NEE", "NEM", "NFLX", "NFX", "NI", "NKE", "NKTR", "NLSN", "NOC", "NOV",
                       "NRG",
                       "NSC", "NTAP", "NTRS", "NUE", "NVDA", "NWL", "NWS", "NWSA", "O", "OKE", "OMC", "ORCL", "ORLY",
                       "OXY",
                       "PAYX", "PBCT", "PCAR", "PEG", "PEP", "PFE", "PFG", "PG", "PGR", "PH", "PHM", "PKG", "PKI",
                       "PLD",
                       "PM", "PNC", "PNR", "PNW", "PPG", "PPL", "PRGO", "PRU", "PSA", "PSX", "PVH", "PWR", "PXD",
                       "PYPL",
                       "QCOM", "QRVO", "RCL", "RE", "REG", "REGN", "RF", "RHI", "RHT", "RJF", "RL", "RMD", "ROK", "ROL",
                       "ROP", "ROST", "RSG", "RTN", "SBAC", "SBUX", "SCHW", "SEE", "SHW", "SIVB", "SJM", "SLB", "SLG",
                       "SNA", "SNPS", "SO", "SPG", "SPGI", "SRE", "STI", "STT", "STX", "STZ", "SWK", "SWKS", "SYF",
                       "SYK",
                       "SYMC", "SYY", "T", "TAP", "TDG", "TEL", "TFX", "TGT", "TIF", "TJX", "TMK", "TMO", "TPR", "TRIP",
                       "TROW", "TRV", "TSCO", "TSN", "TSS", "TTWO", "TWTR", "TXN", "TXT", "UA", "UAA", "UAL", "UDR",
                       "UHS",
                       "ULTA", "UNH", "UNM", "UNP", "UPS", "URI", "USB", "UTX", "V", "VAR", "VFC", "VIAB", "VLO", "VMC",
                       "VNO", "VRSK", "VRSN", "VRTX", "VTR", "VZ", "WAT", "WBA", "WCG", "WDC", "WEC", "WELL", "WFC",
                       "WHR",
                       "WLTW", "WM", "WMB", "WMT", "WRK", "WU", "WY", "WYNN", "XEC", "XEL", "XLNX", "XOM", "XRAY",
                       "XRX",
                       "XYL", "YUM", "ZBH", "ZION", "ZTS", "Q", "EVHC", "UA-C", "AYI", "CSRA", "CMCSK", "SIG", "CPGX",
                       "BXLT", "ENDP", "LVLT", "MNK", "NAVI", "GMCR", "GGP", "KORS", "RIG", "PCG", "SCG", "ESRX", "COL",
                       "AET", "SRCL", "EQT", "CA", "ANDV", "XL", "DPS", "TWX", "RRC", "MON", "WYN", "PDCO", "CHK",
                       "SNI",
                       "BCR", "SPLS", "DD", "WFM", "AN", "BBBY", "MUR", "RAI", "YHOO", "TDC", "R", "MJN", "TGNA", "DNB",
                       "SWN", "URBN", "FTR", "FSLR", "HAR", "LLTC", "PBI", "SE", "STJ", "OI", "LM", "DO", "HOT", "EMC",
                       "GAS", "TE", "CVC", "CCE", "ARG", "TWC", "SNDK", "ADT", "GME", "THC", "CAM", "POM", "ESV", "CNX",
                       "PCL", "PCP", "BRCM", "FOSL", "ALTR", "CSC", "SIAL", "GNW", "HCBK", "JOY", "HSP", "PLL", "DTV",
                       "NE",
                       "FDO", "KRFT", "ATI", "TEG", "QEP", "LO", "WIN", "DNR", "NBR", "AVP", "CFN", "PETM", "SWY",
                       "COV",
                       "BMS", "JBL", "BTU", "GHC", "RDC", "X", "FRX", "IGT", "LSI", "BEAM", "SLM", "CLF", "WPX", "LIFE",
                       "ANF", "JDSU", "TER", "MOLX", "JCP", "NYX", "DELL", "SAI", "BMC", "S", "APOL", "FHN", "HNZ",
                       "DF",
                       "CVH", "PCS", "BIG"]

        # Encode train values
        if constants.VERBOSE:
            print("Encoding data")
        encoded_x = []
        for i in range(len(x_data)):
            # if i > 1000: continue
            bin_1 = x_data[i][:4]
            num_1 = x_data[i][4:6]
            bin_2 = x_data[i][6]
            num_2 = x_data[i][7]
            # mix_1 = x_data[i][8:14]
            mix_1 = x_data[i][8:13]
            num_3 = x_data[i][14]
            mix_2 = x_data[i][15:18]
            num_4 = x_data[i][18:26]

            encoded_x.append(list(
                preprocessing.OneHotEncoder(categories=[binary, binary, binary, binary]).fit_transform(
                    [bin_1]).toarray()[
                    0]) + list(num_1) +
                             list(preprocessing.OneHotEncoder(categories=[binary]).fit_transform([[bin_2]]).toarray()[
                                      0]) + list([num_2]) +
                             list(preprocessing.OneHotEncoder(
                                 # categories=[binary, binary, days, months, years, all_tickers]).fit_transform(
                                 categories=[binary, binary, days, months, years]).fit_transform(
                                 [mix_1]).toarray()[0]) + list([num_3]) +
                             list(
                                 preprocessing.OneHotEncoder(categories=[triary, triary, constants.DISCRETE_JUMPS]).fit_transform(
                                     [mix_2]).toarray()[0]) + list(num_4))
        if constants.STORE_CACHE:
            with open("models/ml_x_encoded.csv", "w", newline='') as my_csv:
                writer = csv.writer(my_csv)
                writer.writerows(encoded_x)
    else:
        if constants.VERBOSE:
            if constants.VERBOSE:
                print("Reading cached data")
        encoded_x = []
        with open('models/ml_x_encoded.csv', 'r') as data:
            reader = csv.reader(data)
            for row in reader:
                encoded_x.append([float(i) for i in row])

    # 2) Create model from data
    if constants.VERBOSE:
        print("Creating model")
    X_table = list()
    Y_table = list()

    for i in range(len(x_data)):
        # if i > 1000: continue
        if x_data[i][constants.YEAR_FEATURE] != simulation_year:
            X_table.append(encoded_x[i])  # append encoded values, not the original ones
            Y_table.append(y_data[i][0])

    clf = LogisticRegression(random_state=None, solver='liblinear', penalty='l1', C=10, multi_class='ovr').fit(
        np.asarray(X_table),
        np.asarray(Y_table))

    # 3) Run analysis of trades
    if constants.VERBOSE:
        print("Running analysis")
    income = 0
    income_percentage = 0
    prediction_results = []
    real_results = []

    always_sell = 0
    always_sell_percentage = 0
    always_buy = 0
    always_buy_percentage = 0
    discrete_trades = [0] * len(constants.DISCRETE_JUMPS)
    discrete_won_trades = [0] * len(constants.DISCRETE_JUMPS)
    for i in range(len(x_data)):
        # if i > 1000: continue
        if x_data[i][constants.YEAR_FEATURE] != simulation_year:
            continue

        res_array = clf.predict_proba(np.asarray([encoded_x[i]]))[0]
        res_value = clf.predict(np.asarray([encoded_x[i]]))[0]

        if constants.CLASSIFY_RESULTS:
            if constants.CERTAINTY_BASED_TRADES:
                action = np.sign(constants.DISCRETE_JUMPS[res_value])
                coef = np.abs(constants.DISCRETE_JUMPS[res_value])  # Multiply by 10 to ensure that numbers are not too small
            else:
                coef = 1
                if constants.DISCRETE_JUMPS[res_value] > 0:
                    action = constants.ORDER_BUY
                elif constants.DISCRETE_JUMPS[res_value] < 0:
                    action = constants.ORDER_SELL
                else:
                    action = constants.ORDER_NONE

        else:
            if constants.PREDICTION_THRESHOLD != 0:
                # If highest class is for at least threshold better than other classes then select it otherwise dont perform trade
                if res_array[1] > res_array[0] and res_array[1] > res_array[2]:
                    action = constants.ORDER_NONE
                elif abs(res_array[0] - res_array[2]) > constants.PREDICTION_THRESHOLD:
                    if res_array[0] > res_array[2]:
                        action = constants.ORDER_SELL
                    else:
                        action = constants.ORDER_BUY
                else:
                    action = constants.ORDER_NONE
            else:
                # use result
                action = res_value

            if constants.CERTAINTY_BASED_TRADES:
                coef = max(res_array)*10  # Multiply by 10 to ensure that numbers are not too small
            else:
                # Do a full trade
                coef = 1

        income += action * trades[i][0] * coef
        trade_income_percentage = action * trades[i][1] * coef
        income_percentage += trade_income_percentage

        prediction_results.append(res_value)
        real_results.append(y_data[i][0])

        always_sell += -1 * trades[i][0]
        always_sell_percentage += -1 * trades[i][1]
        always_buy += trades[i][0]
        always_buy_percentage += trades[i][1]

        discrete_trades[utilities.get_closest_index(constants.DISCRETE_JUMPS, trades[i][1])] += 1
        if trade_income_percentage > 0:
            discrete_won_trades[utilities.get_closest_index(constants.DISCRETE_JUMPS, trades[i][1])] += 1
        elif trade_income_percentage < 0:
            discrete_won_trades[utilities.get_closest_index(constants.DISCRETE_JUMPS, trades[i][1])] -= 1

    if constants.VERBOSE:
        print("Done running")

    print("Year:", simulation_year, "Income:", round(income, 3),
          "Percentage (factor):", round(income_percentage, 3),
          "ML Score:", round(accuracy_score(np.asarray(real_results), np.asarray(prediction_results)), 3),
          "Always sell:", round(always_sell, 3),
          "Always sell percentage (factor):", round(always_sell_percentage, 3),
          "Always buy:", round(always_buy, 3),
          "Always buy percentage (factor):", round(always_buy_percentage, 3),
          "Total trades:", sum(discrete_trades),
          "Discrete trades count:", discrete_trades,
          "Trades ratio:", discrete_won_trades)

    if constants.VERBOSE:
        print("Predictions:", prediction_results)
        print("Real results:", real_results)
