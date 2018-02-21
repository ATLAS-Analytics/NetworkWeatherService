# Network Weather Service

This repository serves multiple purposes:

* Collects LHCOPN data from AMQ at CERN, enriches it with data obtained from AGIS, indexes it in Elasticsearch at University of Chicago.
* Collects ESNet data and stores it at UC
* Contains code that derives additional data
* Contains all the analytics services
*   anomaly detection
*   
* Traceroute inspector web site.
    To start it on a kubernetes cluster do: kubectl create -f kube/traceroute-site.yaml
    To access it visit: ...
* jupyterlab with analytics notebooks.
    To start it up do: kubectl create -f kube/juputerlab.yaml
    To access it visit: ...


## TO DO

* create dockerHub 
* configure Apache.
* move in code from uct3-lx2
