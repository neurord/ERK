===========
**Model files for simulating the ERK signaling pathway during L_LTP induction in the hippocampus**
===========

ERK signaling pathway include:

1. Calcium:

   * Calcium activation of RasGRF followed by RasGTP production
   * CamKII modulation of SynGap followed by increase RasGTP and Rap1GTP lifetime
   
2. cAMP

   * cAMP activation of Epac activation followed Rap1GTP
   * PKA phorylation of Src family kinase leading to Rap1GTP production
   * Gβγ recruitment of Src family kinase followed by activation of RasGTP
   
.. figure:: C:\Users\nminingo\OneDrive - George Mason University\Desktop/ERK_diagram.jpg
    :alt: alternate text
    :figclass: align-center

    ERK signaling pathwway diagram

The repository contains several types of simulation files (in Experiment) and python scripts for analysis of output (in Analysis).  All output files were first processed using nrdh5_analv2 in https://github.com/neurord/NeuroRDanal

Model_ERK-stimdxxx.xml contain the entire model specification, which combines Reaction file (*Rxn_ERK_xxx.xml*), Morphology file (*Morph.xml*), initial conditions file (*IC_ERK_xxx.xml*), output file (*Out_ERK_xxx.xml*) and stimulation (*Stim_ERK_xxx.xml*).  To run simulations, use NeuroRDv3.2.4 as follow:

``java -jar /path/to/neurord-3.2.3-all-deps.jar /path/to/Model_ERK-stimd_xxx.xml``

-------------
**Subfolders**
-------------
1. **Experiment/Initialization/**:

* To match the in *vitro* data on basal concentration, the model for about an hour to obtain steady-state concentrations for all molecules
* To copy basal quantities of molecules, run:
         ``ARGS="IC_filename,h5_filename ,sstart ssend"`` then ``execfile('path/to/file/UpdateIC_basal.py')``


2. **Experiment/simulation/**:

* Reaction files and Morphology files used in all simulation.
* IC files used in all simulation except robustness random and factor simulations (set of molecules was changed by + or - 10%)

3. **Experiment/simulation/Single_pulse**:simulation of singly and combination pathway using either differnt duration (same amplitude) or different amplitude (same duration)

* Model_ERK-stimd-xxx.xml and Stim_ERKxxx.xml for each pathway 
* C* indicate concentration, d* indicates duration
				    
4. **Experiment/simulation/LTP_train/**: simulation of singly and combination pathway using 4 train of 100 Hz with different inter-train interval (L_LTP stimulation protocol)

 *Model_ERK-stimd-xxx.xml* and *Stim_ERK_xxx.xml* for each pathway

5. **Experiment/simulation/LFS_ISO_HFS/**: simulation in response to synaptic input (activation during LTP induction 

*Model_ERK-stimd-.xml* and *Stim_ERK_xxx.xml*, LTP paradigms in response to glutamate input from published model (*Jȩdrzejewska-Szmek, J., Luczak, V., Abel, T., Blackwell, K.T., 2017. β-adrenergic signaling broadly contributes to LTP induction. PLOS Computational Biology 13, e1005657.*) 

6. **Experiment/simulation/Robustness/**: simulation to ensure the robustness of results to variation in parameter value

*Model_ERK-stimd-xxx.xml* and *Stim_ERK_xxx.xml* and *IC_ERK_xxx.xml* (Experiment/simulation/Robustness/analysis) of modify rate or quantity to assess effect on ERK

7. **Experiment/Analysis/**:

statistical files for robustness analysis
