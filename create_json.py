# No change this file!
import json
import numpy as np
def create_json(fname):

    inp = {
    


    "integrator":{

        "atol": 10**(-10),
        "rtol": 10**(-6),
        "method": "DOP853",

    },


    "Solve Sitnikov problem for one or any data":{
        
        "common_parameters":{
            
            "run" : False,
            "tmax": 2*np.pi*10,
            "step": 0.1,
            "result_dir": None,

        },
            
        "hand_data":{

            "h": 1.0,
            "e": 0.0,

        },

        "from_file":{
            "data_file" : None,
            "skip_rows" : 0,
            "delimiter" : None,
        },
    },



    "Creates and plots Poincare map":{

        "common_parameters":{

            "solve":{
                "run" : False,
                "h1"  : 0.0,
                "h2"  : 2.5,
                "step": 0.1,
                "n_rot": 300,
                "save_dir": 'map_data',
            },

            "plot":{
                "run": False,
                "dir_ima": None, 
                "color": "red",
                "xlim": (-3,3),
                "ylim": (-2,2),
            },
        },
        
        "hand_data":{
            "e"   : 0.1,
        },
    
        "from_file":{
            "inp_file": None,        
            "skip_rows" : 0,
            "delimiter" : None,
        },
    
    },
    

    
    }

    with open(fname, 'w') as f:
        string = json.dumps(inp, sort_keys=False, indent=4)
        f.write(string)
if __name__ == '__main__':
    create_json('default.json')

    
    with open('default.json') as json_file:
        data = json.load(json_file)
