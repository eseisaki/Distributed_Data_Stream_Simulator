# Distributed_Data_Stream_Simulator


A python module for tracking network cost of simulated distributed algorithms.

Using this module, one can implement distributed algorithms at a high level and
simulate them while tracking communication activity.

---

### Requirements
- implemented with *python: version 3.6 (or higher)*
- it is suggested to create a virtual environment by doing the following:
        
        python3 -m venv venv
        source venv/bin/activate
        
- some not built-in python modules are required. To install run:
       
       pip install -r requirements.txt
       
---

### Run code

In order to run an example algorithm , simply run:

    python basic_gm.py

---

### Testing
For testing **pytest** module was used.To run all test do the following:

    pytest -v
    
In order to run a specific group of tests you have to run the following:

    pytest -k {keyword} -v
---


### Documentation

For the documentation **Sphinx 2.3.1.** software was used.

To create documentation just run:

    cd docs
    make clean html
    
Then open the *index.html* with a browser. 


