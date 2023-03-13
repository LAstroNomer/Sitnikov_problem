# My solution of Sitnikov problem
***

## Description
***

### What does this script do?
***

1. Solve Sitnikov problem for one or any data
2. Create and plot Poincare map.

### Equation of motion

***

The Sitnikov problem is a particular case of 3-body problem. We have two body with masses $m_1 = m_2 = m$. They move on elliptic orbits around common center of mass by Kepler law. Therd body moves perpendicular to the plane of their orbits throught the center of mass. The mass of therd body we accept equals to zero. This situation is depicted in the figure below.
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

This system we solve in our algorithm.

### How to use
***
1. Create new input file with **$python3 run.py --get_json** or **$python3 run.py --get_json --json_name FILE.json**
2. Edit **default.json** or **FILE.json** (see details below)
3. Run script: **$python3 run.py [--json_name FILE.json]**

### Input parameters
***
File json includes all the parameters that you can use to regulate the process of the script. All parameters are divided into blocks.

**1. Solve Sitnikov problem for one or any data** Use this part if you want to get solution for one or any initial data.

**1.1 hand_data**. Use this part if you want to get solution for one pair of initial data. All this parameters will be ignore, if you use the parameters in part 1.2
Name | Description | Type | Example |
---  | ---         | ---  | ---     |
h    | Initial height of third body above the plane.        | float |   1.0|
e    | 
 
