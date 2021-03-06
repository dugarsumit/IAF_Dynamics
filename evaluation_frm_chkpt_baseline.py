import tensorflow as tf
import numpy as np

import time
import matplotlib.pyplot as plt
import seaborn as sns

import cPickle as pickle

from IPython import display

from iaf_dynamics import DVBFNoKL
from baseline import DVBF
from world import PendulumFullObs
import utils
import os


X, U, R, S = pickle.load(open("data/training_set.p", "rb"))

chkpoint_file = 'chkpt/2017_10_18_07_15_checkpoint999.ckpt'
m = DVBF(3, 1, 6, 10, chkpoint_file=chkpoint_file)


timestamp=utils.get_timestamp()

_RESULT_PATH = 'results/'
if not os.path.exists(_RESULT_PATH):
    os.makedirs(_RESULT_PATH)


X_temp, U_temp, R_temp, S_temp = pickle.load(open("data/test_set.p", "rb"))

x_gen, x_obs, rec_loss_val = m.sess.run((m.gen_x_mean, m.px_mean, m.rec_loss), feed_dict={m.x: X_temp, m.u:U_temp})
rec_diff = np.mean(np.abs(X_temp - x_obs))
gen_diff = np.mean(np.abs(X_temp - x_gen))

result_details_path = _RESULT_PATH + 'evaluation_details.txt'
result_details_file = open(result_details_path, 'a+')
result_details_file.write(str(timestamp) + ':  rec_diff_baseline: ' + str(rec_diff) + ';  gen_diff_baseline: ' + str(gen_diff) + ';  rec_loss: ' + str(rec_loss_val) + '\n')
result_details_file.close()

# Plot the position and reward of low dim pendulum
e = int(np.random.rand() * 100)
e = 100
plt.close()
f, axarr = plt.subplots(1, 2, figsize=(15, 6))
axarr[0].plot(x_gen[:, e, 0])
axarr[0].plot(x_gen[:, e, 1])
axarr[0].plot(x_gen[:, e, 2])
axarr[0].set_ylim(-1.1, 1.1)
axarr[1].plot(X_temp[:, e, 0])
axarr[1].plot(X_temp[:, e, 1])
axarr[1].plot(X_temp[:, e, 2])
axarr[1].set_ylim(-1.1, 1.1)
axarr[0].set_title('Generated Trajectory from Baseline Checkpoint: ')
axarr[1].set_title('Generated Trajectory from Ground Truth: ')
plt.savefig(_RESULT_PATH + '%s' % timestamp + '_PositionPlotBaselineGen.png')
# plt.show()

plt.close()
f, axarr = plt.subplots(1, 2, figsize=(15, 6))
axarr[0].plot(np.arctan2(x_gen[:, e, 1], x_gen[:, e, 0]))
axarr[1].plot(np.arctan2(X_temp[:, e, 1], X_temp[:, e, 0]))
axarr[0].set_title('Generated Trajectory from Baseline Checkpoint: ')
axarr[1].set_title('Generated Trajectory from Ground Truth: ')
plt.savefig(_RESULT_PATH + '%s' % timestamp + '_ArcTanPlotBaselineGen.png')

plt.close()
f, axarr = plt.subplots(1, 2, figsize=(15, 6))
axarr[0].plot(x_obs[:, e, 0])
axarr[0].plot(x_obs[:, e, 1])
axarr[0].plot(x_obs[:, e, 2])
axarr[0].set_ylim(-1.1, 1.1)
axarr[1].plot(X_temp[:, e, 0])
axarr[1].plot(X_temp[:, e, 1])
axarr[1].plot(X_temp[:, e, 2])
axarr[1].set_ylim(-1.1, 1.1)
axarr[0].set_title('Generated Trajectory from Baseline Checkpoint: ' + chkpoint_file)
axarr[1].set_title('Generated Trajectory from Ground Truth: ')
plt.savefig(_RESULT_PATH + '%s' % timestamp + '_PositionPlotBaselineObs.png')
# plt.show()

plt.close()
f, axarr = plt.subplots(1, 2, figsize=(15, 6))
axarr[0].plot(np.arctan2(x_obs[:, e, 1], x_obs[:, e, 0]))
axarr[1].plot(np.arctan2(X_temp[:, e, 1], X_temp[:, e, 0]))
axarr[0].set_title('Generated Trajectory from Baseline Checkpoint: ' + chkpoint_file)
axarr[1].set_title('Generated Trajectory from Ground Truth: ')
plt.savefig(_RESULT_PATH + '%s' % timestamp + '_ArcTanPlotBaselineObs.png')
# plt.show()