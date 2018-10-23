#How to use :doc:`ajustador` to fit a NeuroRD model to experimental data
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''This demonstration fits a single reaction model (Model_Cam_RasGRF) to data.
exec(open('neurord_fit_GRF.py').read())
'''

import ajustador as aju
import numpy as np
from ajustador import drawing,loadconc,nrd_fitness
from ajustador.helpers import save_params,converge
import os

#model is the xml file that contains the neuroRD model to simulate and adjust parameters
dirname='./'  #where data and model are stored.  Multiple datafiles allowed
model_set='Model_Cam_RasGRF'
exp_name='Jin_JBC_2014' #name of data file selected from dirname; each file may contain several molecules
mol=['CamCa4'] #which molecule(s) to match in optimization
tmpdir='/tmp/camgrf'

# number of iterations, use 1 for testing
# default popsize=8, use 3 for testing
iterations=1#25
popsize=3#8
test_size=0#25
seed=123

os.chdir(dirname)
exp=loadconc.CSV_conc_set(exp_name)

P = aju.xml.XMLParam
#list of parameters to change/optimize
params = aju.optimize.ParamSet(P('phos_fwd_rate',1e-9 , min=0, max=1e-6, xpath='//Reaction[@id="RasGRF+CamCa4 -- CamCa4RasGRF"]/forwardRate'),
                               P('phos_rev_rate',1e-9 , min=0, max=1e-6, xpath='//Reaction[@id="CamCa4RasGRF -- RasGRF+CamCa4"]/reverseRate'))

###################### END CUSTOMIZATION #######################################

fitness = nrd_fitness.specie_concentration_fitness(species_list=mol)

############ Test fitness function
#sim = aju.xml.NeurordSimulation('/tmp', model=model, params=params)
#cp /tmp/???/model.h5 modelname.split('.')[0]+'.h5'
#sim2=aju.xml.NeurordResult('Model_syngap_ras.h5')
#print(fitness(sim2, exp))
################

fit = aju.optimize.Fit(tmpdir, exp, model_set, None, fitness, params,
                       _make_simulation=aju.xml.NeurordSimulation.make,
                       _result_constructor=aju.xml.NeurordResult)
fit.load()
fit.do_fit(iterations, popsize=popsize,sigma=1.0,seed=seed)
mean_dict,std_dict,CV=converge.iterate_fit(fit,test_size,popsize)

########################################### Done with fitting

#to look at centroid [0] or stdev [6] of cloud of good results:
for i,p in enumerate(fit.params.unscale(fit.optimizer.result()[0])):
    print(fit.param_names()[i],'=',p, '+/-', fit.params.unscale(fit.optimizer.result()[6])[i])

#to look at fit history
aju.drawing.plot_history(fit,fit.measurement)

startgood=0
threshold=20
save_params.save_params(fit, startgood, threshold)


