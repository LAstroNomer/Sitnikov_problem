# My solution of Sitnikov problem
***

## Description
***

### What does this script do?
***

1. Solves Sitnikov problem for one or any data
2. Creates and plots Poincare map.

All results are output in physical quantities $t$, $\frac{dZ(t)}{dt}$, $Z(t)$. Details and dimensions are described in the paragraph below. 

### Equation of motion

***

The Sitnikov problem is a particular case of 3-body problem. We have two bodies with masses $m_1 = m_2 = m$. They move on elliptic orbits around common center of mass by Kepler law. Third body moves perpendicular to the plane of their orbits through the center of mass. The mass of third body equals zero. This situation is depicted in the figure below.
<p align="center">
<img  src="https://github.com/LAstroNomer/Sitnikov_problem/blob/master/Sitnikov_Problem_Konfiguration.jpeg"  width="350" />
</p>

We take the axis of application ($z$) along the movement of the third body. The equation of motion is:

$$
    \frac{d^2z}{dt^2} = -  \frac{2 G M z}{(\rho(t)^2 + z^2)^{3/2}}
$$

$$
    \rho(t) = a(1 + e \cos(E(t)))
$$

where $E$ we get from Kepler equation: $M(t) = n \cdot t = E - e \sin(E)$. Next, we rewrite the equation in the form of a system:

$$
    \begin{cases} 
    \dot{z} = \nu \\  
    \dot{\nu} =  - \frac{2 G M z}{(\rho(t)^2 + z^2)^{3/2}} 
    \end{cases}
$$

Changing the system of units:

$$
A_{total} = a+a = 1
$$

$$
GM_{total} = 2Gm = 1
$$

We get: $T = 2 \pi$ and $n = 1$ 

$$
    \begin{cases} 
    \dot{z} = \nu \\  
    \dot{\nu} =  - \frac{z}{(\rho(t)^2 + z^2)^{3/2}}\\
    \rho(t) = 0.5(1 + e \cos(E))\\
    t = E - e \sin(E)
    \end{cases}
$$


And finally we will replace the variables:

$$
    \frac{dE}{dt} = \frac{1}{1 - e\cos(E)} = \frac{1}{2\rho}
$$

$$
    \begin{cases} 
    \frac{dz}{dE} = 2 \rho \nu\\
    \frac{d\nu}{dE} = - \frac{2 \rho z}{(z^2 + \rho^2)^{3/2}}
    \end{cases}
$$

This system we solve in our algorithm. When we output the results, we go back from E to t.

### How to use
***
1. Create new input file with **$python3 run.py --get_json** or **$python3 run.py --get_json --json_name FILE.json**
2. Edit **default.json** or **FILE.json** (see details below)
3. Run script: **$python3 run.py [--json_name FILE.json]**

### Input parameters
***
File json includes all the parameters that you can use to regulate the process of the script. All parameters are divided into blocks.

**1. Solve Sitnikov problem for one or any data** Use this part if you want to get solution for one or any initial data. **Note** that the solution is displayed on a uniform time grid, which is set in 1.1. 

**1.1 common_parameters**. In this part you set common parameters. They will be applied the same way for both 1.2 and 1.3
Name | Description | Type | Default |
---  | ---         | ---  | ---     |
run  | The main key. Responsible for starting point 1. If false, the entire block will be skipped   | bool | false |
tmax | Maximum time value| float| 10 $\cdot 2 \pi \approx 62.8...$|
step | Step along the time axis | float| 0.1|
result_dir| The path to the folder for uploading the results of the script. By default, the same folder | string or null| null|


**1.2 hand_data**. Use this part if you want to get solution for one pair of initial data. All this parameters will be ignore, if you use the parameters in part 1.2
Name | Description | Type | Default |
---  | ---         | ---  | ---     |
h    | Initial height of third body above the plane.        | float |   1.0|
e    | Eccentricity of an elliptical orbit| float 0 $\le$ e < 1 | 0.0|

**1.3 from_file**. Use this part if you want to get solution for any dots of initial data. The input file must be in text format. It should have two columns for $e$ and $h$ respectively.

Name | Description | Type | Default |
---  | ---         | ---  | ---     |
data_file    | Path to input file. If value is 'null' all this block will be ignore.         | string or null|   null|
skip_rows| The count of lines that should be skipped | integer | 0|
delimiter| The symbol used to separate the columns. If you use spaces or tabs, then do not change this parameter | string or null| null

