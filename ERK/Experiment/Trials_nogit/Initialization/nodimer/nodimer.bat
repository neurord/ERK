#run to get basal 
#java -jar /home/nadia/neurord-3.2.4-all-deps.jar -t 3600000 Model_ERK-nodimer.xml


#copy new IC 
#python3.6 /home/nadia/ERK/ERK/Update_IC.py


#run with stim file
java -jar /home/nadia/neurord-3.2.4-all-deps.jar -t 3600000 Model_ERK-stimnodimer.xml Model_ERK-stimnodimer-bhalla

#stimulate C500
java -jar /home/nadia/neurord-3.2.4-all-deps.jar -t 3600000 Model_ERK-stimd-C500-d1.xml  Model_ERKCa-stimnodimer-C500-d1&
java -jar /home/nadia/neurord-3.2.4-all-deps.jar -t 3600000 Model_ERK-stimd-C500-d2.xml  Model_ERKCa-stimnodimer-C500-d2&
java -jar /home/nadia/neurord-3.2.4-all-deps.jar -t 3600000 Model_ERK-stimd-C500-d4.xml  Model_ERKCa-stimnodimer-C500-d4&
java -jar /home/nadia/neurord-3.2.4-all-deps.jar -t 3600000 Model_ERK-stimd-C500-d6.xml  Model_ERKCa-stimnodimer-C500-d6&
java -jar /home/nadia/neurord-3.2.4-all-deps.jar -t 3600000 Model_ERK-stimd-C500-d8.xml  Model_ERKCa-stimnodimer-C500-d8&
java -jar /home/nadia/neurord-3.2.4-all-deps.jar -t 3600000 Model_ERK-stimd-C500-d10.xml Model_ERKCa-stimnodimer-C500-d10

#stimulate C1000
java -jar /home/nadia/neurord-3.2.4-all-deps.jar -t 3600000 Model_ERK-stimd-C1000-d1.xml  Model_ERKCa-stimnodimer-C1000-d1&
java -jar /home/nadia/neurord-3.2.4-all-deps.jar -t 3600000 Model_ERK-stimd-C1000-d2.xml  Model_ERKCa-stimnodimer-C1000-d2&
java -jar /home/nadia/neurord-3.2.4-all-deps.jar -t 3600000 Model_ERK-stimd-C1000-d4.xml  Model_ERKCa-stimnodimer-C1000-d4&
java -jar /home/nadia/neurord-3.2.4-all-deps.jar -t 3600000 Model_ERK-stimd-C1000-d6.xml  Model_ERKCa-stimnodimer-C1000-d6&
java -jar /home/nadia/neurord-3.2.4-all-deps.jar -t 3600000 Model_ERK-stimd-C1000-d8.xml  Model_ERKCa-stimnodimer-C1000-d8&
java -jar /home/nadia/neurord-3.2.4-all-deps.jar -t 3600000 Model_ERK-stimd-C1000-d10.xml Model_ERKCa-stimnodimer-C1000-d10



