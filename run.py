from create_json import create_json
from my_sitnikov import *

def SSp_sol(common, hand_data, from_file, integrator):

    # Integrator params
    atol        = integrator["atol"]
    rtol        = integrator["rtol"]
    method      = integrator["method"]

    # Common params
    run  = common["run"]
    tmax = common["tmax"]
    step = common["step"]
    result_dir = common["result_dir"]

    if not run:
        print("Solves Sitnikov problem for one or any data --- off")
        return

    # load data
    h_arr = np.array([])
    e_arr = np.array([])
    t_maxs = np.array([])
    steps = np.array([])

    data_file = from_file["data_file"]
    skip_rows = int(from_file["skip_rows"])
    delimiter = from_file["delimiter"]

    if data_file is None:        
        try:
            h = float(hand_data["h"])
            e = float(hand_data["e"])
            tmax = float(common["tmax"])
            step = float(common["step"])
            h_arr = np.append(h_arr, h)
            e_arr = np.append(e_arr, e)
            t_maxs = np.append(t_maxs, tmax)
            steps = np.append(steps, step)
        except:
            print("Wrong hand params! Must be float!")
            return
    else:
        with open(data_file, 'r') as inp:
            for line in inp.readlines()[skip_rows :]:
                if delimiter is None:
                    h, e = map(float, line.split())
                else:
                    h, e = map(float, line.split(delimiter))

                tmax = float(common["tmax"])
                step = float(common["step"])
                h_arr = np.append(h_arr, h)
                e_arr = np.append(e_arr, e)
                t_maxs = np.append(t_maxs, tmax)
                steps = np.append(steps, step)                
  
    # Set out dir
    file_ext = '.dat' 
    if result_dir is None:
        result_dir = '.'
    else:
        if os.path.exists(result_dir):
            pass
        else:
            key = True
            while key:
                ans = input("No path %s. Do you want to create path? (y/n) \n" %result_dir)

                if (ans == "y"):
                    subprocess.run("mkdir -p %s" %result_dir, shell=True)  
                    key = not(key)
                elif (ans == "n"):
                    print("Exit...")
                    key = not(key)
                    return

    # def Sitnikov class
    for h, e, t_max, step in zip(h_arr, e_arr, t_maxs, steps):
        problem = Sitnikov(e, h, atol=atol, rtol=rtol, method=method)
        t, Z, dZ = problem.solve(t_max, step)
        with open(Path(result_dir,'e'+str(e)+'_h'+str(h)+file_ext),'w') as out:
            print('%10s %10s %10s' %('t', 'Z', 'dZ'), file=out)
            for ti, Zi, dZi in zip(t, Z, dZ):
                print('%10.2f %10.2f %10.2f'  %(ti, Zi, dZi), file=out)

    return
#---------------------------------------------------------------------------------------


def CPPm(common, hand_data, from_file, integrator):

    # Integrator params
    atol        = integrator["atol"]
    rtol        = integrator["rtol"]
    method      = integrator["method"]

    solve = common["solve"]
    plot  = common["plot"] 
    
    
    if not (solve['run'] or plot['run']):
        print("Creates and plots Poincare map --- off")
        return

    # Solve
    e_s = np.array([])

    inp_file = from_file["inp_file"]
    skip_rows = int(from_file["skip_rows"])
    delimiter = from_file["delimiter"]
    
    if inp_file is None:
        e = hand_data["e"]
        e_s =np.append(e_s, e)
    else:
        with open(inp_file, 'r') as inp:
            for line in inp.readlines()[skip_rows :]:
                if delimiter is None:
                    e = float(line.split()[0])
                else:
                    e = float(line.split(delimiter)[0])
                e_s =np.append(e_s, e)

    # Common params           
    h1    = solve["h1"]
    h2    = solve["h2"]
    step  = solve["step"]
    io_key= str(h1)+'_'+str(h2)+'_'+str(step)
    n_rot = solve["n_rot"]
    save_dir = solve["save_dir"]
    
    color = plot['color']
    xlim  = plot["xlim"]
    ylim  = plot["ylim"]
        

    # Check output dir
    file_ext = '.dat' 
    if not(os.path.exists(save_dir)):
        key = True
        while key:
            ans = input("No path %s. Do you want to create path? (y/n) \n" %save_dir)

            if (ans == "y"):
                subprocess.run("mkdir -p %s" %save_dir, shell=True)  
                key = not(key)
            elif(ans == "n"):
                print("Exit...")
                key = not(key)
                return
        
    for e in e_s:
        name = 'e'+str(e)    
        problem = Sitnikov(e, h1, n_rot=n_rot, atol=atol, rtol=rtol, method=method)
        hs = np.arange(h1, h2, step)
        
        if solve['run']:
            print('Solve')
            with multiprocessing.Pool(6) as pool:
                Zs_dZs = list(tqdm(pool.imap(problem.solve_phase_portrait, hs), total=len(hs)))
        
            for i, Z_dZ in enumerate(Zs_dZs):
                Z = Z_dZ[0]
                dZ = Z_dZ[1]
                    
                with open(Path(save_dir,name+'_'+io_key+'_'+ str(i)+file_ext),'w') as out:
                    print('%10s %10s' %('Z', 'dZ'), file=out)
                    for Zi, dZi in zip(Z, dZ):
                         print('%10.3f %10.3f' %(Zi, dZi), file=out)

        if plot['run']:     
            print('Plot')       
            out_dir = plot['dir_ima']
            if out_dir is None:
                out_dir = '.'
            else:
                if os.path.exists(out_dir):
                    pass
                else:
                    key = True
                    while key:
                        ans = input("No path %s. Do you want to create path? (y/n) \n" %out_dir)

                        if (ans == "y"):
                            subprocess.run("mkdir -p %s" %out_dir, shell=True)  
                            key = not(key)
                        elif (ans == "n"):
                            print("Exit...")
                            key = not(key)
                            return
            files = os.listdir(save_dir)
            plt.figure(dpi=300)
            problem.plot_phase_portrait(save_dir, files, name, io_key, out_dir, xlim=xlim, ylim=ylim, color=color) 
    return
#----------------------------------------------------------------------------------------------------


def run(args):
    
    fname =  args.json_name
    
    # Check correct name of json file 
    if args.get_json:
        if os.path.exists(fname):
            print('json already exists!')
            return
        create_json(fname)
        print('Done!')
        return
    else:
        if os.path.exists(fname):
            with open(fname, 'r') as inp:
                params = json.load(inp)
        else:
            print('json file not found. Check the name or create new file with $python3 my_sitnikov.py --get_json')
            return


    
    # Get integrator parameters
    integrator  = params["integrator"]    

    # Solve Sitnikov problem for one or any data
    SSp = params["Solve Sitnikov problem for one or any data"]
    common = SSp["common_parameters"]
    hand_data   = SSp["hand_data"]
    from_file   = SSp["from_file"]
    SSp_sol(common, hand_data, from_file, integrator)
    
    
    # Creates and plots Poincare map

    p_map = params["Creates and plots Poincare map"]
    common      = p_map["common_parameters"]
    hand_data   = p_map["hand_data"]
    from_file   = p_map["from_file"]
    CPPm(common, hand_data, from_file, integrator)

    return
#----------------------------------------------------------------------------------------------------


        
        
 
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    
    parser.add_argument("--get_json", action='store_true',  help='Create new input file')
    parser.add_argument("--json_name", default='default.json', type=str, help='Input file name')
    
    args = parser.parse_args()
    run(args)

    
