import pandas as pd 
import numpy as np 
#import matplotlib.pylab as plt
#from matplotlib.pylab import rcParams 
#rcParams['figure.figsize'] = 15, 6
import time
import sys
from threading import Timer
import subprocess as sub

class CCAR(object):
    def __init__(self, db, sid):
        self.started_at=time.time()
        self.mev_approval_needed_by=self.started_at+10
        self.db = db
        self.sid = sid
    
    def check_mev_approvals(self):
        from forecast.mevs.check_approvals import check_mev_approval
        pending_approvals=check_mev_approval(self.db)
        return pending_approvals

    def insert_run(self, exercise, scenario, sid):
        self.run_id = self.db.insert_ccar_runs(exercise, scenario, sid)
        print("Last Run ID: {}".format(self.run_id))
        
    def send_reminder(self, approval_l):
        for approval in approval_l:
            print("Sending reminder for: {}".format(approval))
            print('Requesting approval for {} from {}'.format(approval[1], approval[2]))
            sub.call(['/home/pi/Documents/pyspace/email/sendMevApprovalNotification.sh', approval[1], str(self.run_id), approval[5], 'bandev3@gmail.com'])

    def run(self, exercise='CCAR2017', scenario='baseline'):
        #insert into runs with IN PROGRESS status
        self.insert_run(exercise, scenario, self.sid)

        pending_approvals = self.check_mev_approvals()
        if pending_approvals:
            self.send_reminder(pending_approvals)

        return pending_approvals

            
'''
data = pd.read_csv('/home/pi/Documents/data/AirPassengers.csv')
print(data.head())
print('\n Data Types:')
print(data.dtypes)

dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m')
data = pd.read_csv('/home/pi/Documents/data/AirPassengers.csv', parse_dates='Month', index_col='Month',date_parser=dateparse)
print data.head()

ts = data['#Passengers'] 
ts.head(10)

#1. Specific the index as a string constant:
#ts['1949-01-01']

#2. Import the datetime library and use 'datetime' function:
#from datetime import datetime
#ts[datetime(1949,1,1)]

#1. Specify the entire range:
#ts['1949-01-01':'1949-05-01']

#2. Use ':' if one of the indices is at ends:
#ts[:'1949-05-01']

plt.plot(ts)

from statsmodels.tsa.stattools import adfuller
def test_stationarity(timeseries):
    
    #Determing rolling statistics
    rolmean = pd.rolling_mean(timeseries, window=12)
    rolstd = pd.rolling_std(timeseries, window=12)

    #Plot rolling statistics:
    orig = plt.plot(timeseries, color='blue',label='Original')
    mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    std = plt.plot(rolstd, color='black', label = 'Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show(block=False)
    
    #Perform Dickey-Fuller test:
    print 'Results of Dickey-Fuller Test:'
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print dfoutput


#time.sleep(15)
test_stationarity(ts)

#time.sleep(15)
ts_log = np.log(ts)
plt.plot(ts_log)

moving_avg = pd.rolling_mean(ts_log,12)
#time.sleep(15)

plt.plot(ts_log)
#time.sleep(15)
plt.plot(moving_avg, color='red')

ts_log_moving_avg_diff = ts_log - moving_avg
ts_log_moving_avg_diff.head(12)

ts_log_moving_avg_diff.dropna(inplace=True)
test_stationarity(ts_log_moving_avg_diff)

expwighted_avg = pd.ewma(ts_log, halflife=12)
#time.sleep(15)
plt.plot(ts_log)
#time.sleep(15)
plt.plot(expwighted_avg, color='red')


ts_log_ewma_diff = ts_log - expwighted_avg
test_stationarity(ts_log_ewma_diff)

ts_log_diff = ts_log - ts_log.shift()
#time.sleep(15)
plt.plot(ts_log_diff)



ts_log_diff.dropna(inplace=True)
test_stationarity(ts_log_diff)

from statsmodels.tsa.seasonal import seasonal_decompose
decomposition = seasonal_decompose(ts_log)

trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

#time.sleep(15)
plt.subplot(411)
plt.plot(ts_log, label='Original')
plt.legend(loc='best')
plt.subplot(412)
plt.plot(trend, label='Trend')
plt.legend(loc='best')
plt.subplot(413)
plt.plot(seasonal,label='Seasonality')
plt.legend(loc='best')
plt.subplot(414)
plt.plot(residual, label='Residuals')
plt.legend(loc='best')
plt.tight_layout()

ts_log_decompose = residual
ts_log_decompose.dropna(inplace=True)
test_stationarity(ts_log_decompose)

#ACF and PACF plots:
from statsmodels.tsa.stattools import acf, pacf

lag_acf = acf(ts_log_diff, nlags=20)
lag_pacf = pacf(ts_log_diff, nlags=20, method='ols')

#Plot ACF: 
plt.subplot(121) 
plt.plot(lag_acf)
plt.axhline(y=0,linestyle='--',color='gray')
plt.axhline(y=-1.96/np.sqrt(len(ts_log_diff)),linestyle='--',color='gray')
plt.axhline(y=1.96/np.sqrt(len(ts_log_diff)),linestyle='--',color='gray')
plt.title('Autocorrelation Function')


#Plot PACF:
plt.subplot(122)
plt.plot(lag_pacf)
plt.axhline(y=0,linestyle='--',color='gray')
plt.axhline(y=-1.96/np.sqrt(len(ts_log_diff)),linestyle='--',color='gray')
plt.axhline(y=1.96/np.sqrt(len(ts_log_diff)),linestyle='--',color='gray')
plt.title('Partial Autocorrelation Function')
plt.tight_layout()

from statsmodels.tsa.arima_model import ARIMA

model = ARIMA(ts_log, order=(2, 1, 0))  
results_AR = model.fit(disp=-1)  
plt.plot(ts_log_diff)
plt.plot(results_AR.fittedvalues, color='red')
plt.title('RSS: %.4f'% sum((results_AR.fittedvalues-ts_log_diff)**2))


model = ARIMA(ts_log, order=(0, 1, 2))  
results_MA = model.fit(disp=-1)  
plt.plot(ts_log_diff)
plt.plot(results_MA.fittedvalues, color='red')
plt.title('RSS: %.4f'% sum((results_MA.fittedvalues-ts_log_diff)**2))

model = ARIMA(ts_log, order=(2, 1, 2))  
results_ARIMA = model.fit(disp=-1)  
plt.plot(ts_log_diff)
plt.plot(results_ARIMA.fittedvalues, color='red')
plt.title('RSS: %.4f'% sum((results_ARIMA.fittedvalues-ts_log_diff)**2))

predictions_ARIMA_diff = pd.Series(results_ARIMA.fittedvalues, copy=True)
print predictions_ARIMA_diff.head()

predictions_ARIMA_diff_cumsum = predictions_ARIMA_diff.cumsum()
print predictions_ARIMA_diff_cumsum.head()


predictions_ARIMA_log = pd.Series(ts_log.ix[0], index=ts_log.index)
predictions_ARIMA_log = predictions_ARIMA_log.add(predictions_ARIMA_diff_cumsum,fill_value=0)
predictions_ARIMA_log.head()



predictions_ARIMA = np.exp(predictions_ARIMA_log)
plt.plot(ts)
plt.plot(predictions_ARIMA)
plt.title('RMSE: %.4f'% np.sqrt(sum((predictions_ARIMA-ts)**2)/len(ts)))

time.sleep(10)
'''
