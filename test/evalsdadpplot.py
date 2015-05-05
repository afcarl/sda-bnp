import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['ps.useafm'] = True
matplotlib.rcParams['pdf.use14corefonts'] = True
matplotlib.rcParams['text.usetex'] = True
font = {'family' : 'normal',
        'size' : 24}
matplotlib.rc('font', **font)



#create the plot output directory
basename = 'sdadpmix'
outdir = 'plots'
if not os.path.exists(outdir):
    os.makedirs(outdir)

#get the mcmc run/nthr tags
mcmc_run_tags = []
nthr_tags = []
for f in os.listdir('.'):
    if f[:6] == 'model-':
        mcmc_run_tags.append(f[6:-4])
for f in os.listdir('.'):
    if f[:14] == basename+'-nThr_' and f[-7:] == '-ab.log':
        for tag in mcmc_run_tags:
            if len(tag) < len(f[14:-7]) and f[-7-len(tag):-7] == tag:
                nthr_tags.append(f[14:-7-len(tag)-1])
mcmc_run_tags = sorted(mcmc_run_tags)
nthr_tags = sorted(list(set(nthr_tags)))


#Plot 1: data and model for each mcmc run
for mtag in mcmc_run_tags:
    model = np.genfromtxt('model-'+mtag+'.log')
    train_data = np.genfromtxt('train-'+mtag+'.log')
    test_data = np.genfromtxt('test-'+mtag+'.log')

    D = int((-1 + np.sqrt(1-4*(1-model.shape[1])))/2)

    plt.figure()
    plt.scatter(train_data[:, 0], train_data[:, 1], c='b')
    plt.scatter(test_data[:, 0], test_data[:, 1], c='g')
    for k in range(model.shape[0]):
        mu = model[k, 0:D]
        sig = np.zeros((D, D))
        for j in range(D):
            sig[j, :] = model[k, (j+1)*D:(j+2)*D]
        wt = model[k, -1]
        xy  = mu[:, np.newaxis] + np.dot(np.linalg.cholesky(sig), np.vstack((np.cos(np.linspace(0, 2*np.pi, 100)), np.sin(np.linspace(0, 2*np.pi, 100)))))
        plt.plot(xy[0, :], xy[1, :], lw=5, alpha=np.sqrt(wt), c='r')
    plt.axes().set_aspect('equal')
    plt.xlim((-100, 100))
    plt.ylim((-100, 100))
    plt.savefig(outdir+'/model-'+mtag+'.pdf')


#collect traces/final statistics/etc
final_cpu_times = np.zeros((len(nthr_tags), len(mcmc_run_tags)))
final_testlls = np.zeros((len(nthr_tags), len(mcmc_run_tags)))
final_nclus = np.zeros((len(nthr_tags), len(mcmc_run_tags)))
final_nmatch = np.zeros((len(nthr_tags), len(mcmc_run_tags)))
for i in range(len(nthr_tags)):
    ntag = nthr_tags[i]
    for j in range(len(mcmc_run_tags)):
        mtag = mcmc_run_tags[j]
        gt = np.genfromtxt(basename+'-nThr_'+ntag+'-'+mtag+'-globaltrace.log')
        final_cpu_times[i, j] = gt[-1, 0]
        final_testlls[i, j] = gt[-1, 1]
        final_nclus[i, j] = gt[-1, 2]
        final_nmatch[i, j] = gt[-1, 3]


#Plot 2: bar graph across all mcmc runs, x axis nThr, y axis model quality and cpu time with merge time stacked onto it
plt.figure()
axl = plt.axes()
axr = axl.twinx()
barwidth = .35
axl.bar(barwidth/2.0+np.arange(final_cpu_times.shape[0]), np.mean(final_cpu_times, axis=1), barwidth, color='b', yerr=np.std(final_cpu_times, axis=1), alpha=0.4)
axr.errorbar(barwidth+np.arange(final_testlls.shape[0]), np.mean(final_testlls, axis=1), fmt='o', ms=10, color='r', yerr=np.std(final_testlls, axis=1), alpha=0.4)
axr.set_xticks(barwidth+np.arange(final_testlls.shape[0]))
axr.set_xticklabels( map(str, map(int, nthr_tags)) )
axl.set_xlabel(r'\# Threads')
axl.set_ylabel(r'CPU Time (s)')
axr.set_ylabel(r'Test Log Likelihood')
axr.set_ylim((-10, -4))
plt.savefig(outdir+'/cput-testll-bars.pdf')


#Plot 3: Number of clusters (one line for each nThr) & number of matchings solved vs # merged minibatch posteriors
plt.figure()
ax = plt.axes()
ax.bar(np.arange(final_nclus.shape[0]), np.mean(final_nclus, axis=1), barwidth, color='b', yerr=np.std(final_nclus, axis=1), alpha=0.4)
ax.bar(barwidth+np.arange(final_nmatch.shape[0]), np.mean(final_nmatch, axis=1), barwidth, color='r', yerr=np.std(final_nmatch, axis=1), alpha=0.4)
ax.set_xlabel(r'\# Threads')
ax.set_ylabel(r'Count')
axr.set_xticks(barwidth+np.arange(final_nclus.shape[0]))
ax.set_xticklabels( map(str, map(int, nthr_tags)) )
plt.legend([r'\# Clusters', r'\# Matchings'])
plt.savefig(outdir+'/nclusmatch-bars.pdf')



#Plot 4: Trace of number of clusters/matchings vs number of merged minibatch posteriors for 32 threads
nclus_traces = []
nmatch_traces = []
ntag = nthr_tags[-1]
for j in range(len(mcmc_run_tags)):
    mtag = mcmc_run_tags[j]
    gt = np.genfromtxt(basename+'-nThr_'+ntag+'-'+mtag+'-globaltrace.log')
    nclus_traces.append(gt[:, 2])
    nmatch_traces.append(gt[:, 3])

plt.figure()
ctrace_mean = np.mean(np.array(nclus_traces), axis=0)
ctrace_std = np.std(np.array(nclus_traces), axis=0)
mtrace_mean = np.mean(np.array(nmatch_traces), axis=0)
mtrace_std = np.std(np.array(nmatch_traces), axis=0)

p1, = plt.plot( 1+np.arange(ctrace_mean.shape[0]), ctrace_mean, c='b', lw=2)
plt.plot( 1+np.arange(ctrace_mean.shape[0]), ctrace_mean+ctrace_std, 'b--', lw=2)
plt.plot( 1+np.arange(ctrace_mean.shape[0]), ctrace_mean-ctrace_std, 'b--', lw=2)
plt.fill_between( 1+np.arange(ctrace_mean.shape[0]), ctrace_mean-ctrace_std, ctrace_mean + ctrace_std, facecolor='b', alpha=0.3)

p2, =plt.plot( 1+np.arange(mtrace_mean.shape[0]), mtrace_mean, c='r', lw=2)
plt.plot( 1+np.arange(mtrace_mean.shape[0]), mtrace_mean+mtrace_std, 'r--', lw=2)
plt.plot( 1+np.arange(mtrace_mean.shape[0]), mtrace_mean-mtrace_std, 'r--', lw=2)
plt.fill_between( 1+np.arange(mtrace_mean.shape[0]), mtrace_mean-mtrace_std, mtrace_mean + mtrace_std, facecolor='r', alpha=0.3)

plt.legend([p1, p2], [r'\# Clusters', r'\# Matchings'])
plt.xlabel(r'\# Minibatches Merged')
plt.ylabel(r'Count')
plt.savefig(outdir+'/nclusmatch-lines.pdf')


#Plot 5: Global/minibatch likelihood traces for a single MCMC run
#use the 32thread / 1st mcmc run (totally fine to change these)
ntag = nthr_tags[-1]
mtag = mcmc_run_tags[-1]
gt = np.genfromtxt(basename+'-nThr_'+ntag+'-'+mtag+'-globaltrace.log')
global_times = gt[:, 0]
global_testlls = gt[:, 1]
lt = np.genfromtxt(basename+'-nThr_'+ntag+'-'+mtag+'-localtimes.log')
local_start_times = lt[:, 0]
local_testlls = []
local_times = []
for i in range(lt.shape[0]):
    lt = np.genfromtxt(basename+'-nThr_'+ntag+'-'+mtag+'-localtrace-'+str(i)+'.log')
    local_testlls.append(lt[:,2])
    local_times.append(lt[:,0])

plt.figure()
plt.plot(global_times, global_testlls, 'b', lw=2)
for  i in range(len(local_times)):
    plt.plot(local_start_times[i]+local_times[i], local_testlls[i], 'c', lw=1)
plt.xlabel('Time (s)')
plt.ylabel('Test Log Likelihood')
plt.savefig(outdir+'/testll-trace.pdf')
plt.show()
