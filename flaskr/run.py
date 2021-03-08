import os                                                                       
from multiprocessing import Pool   
import initdb                                             
                                                                                
                                                                                
processes = ('monitorapp.py', 'sensor.py')                                    
                                                  
                                                                                
def run_process(process):                                                             
    os.system('python flaskr/{}'.format(process))                                       
                                                                                
                                                                                
pool = Pool(processes=2)                                                        
pool.map(run_process, processes)   

