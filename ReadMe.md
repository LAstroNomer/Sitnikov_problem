# My solve of Sitnikov problem
***

## Description
***

### What does this script do?
***

1. Solve Sitnikov problem for one or any data
2. Create and plot Poinkare map.

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

We get:
$$
T = 2 \pi$ and $n = 1
$$ 

$$
    \begin{cases} 
    \dot{z} = \nu \\  
    \dot{\nu} =  - \frac{z}{(\rho(t)^2 + z^2)^{3/2}}\\
    \rho(t) = 1 + e \cos(E)\\
    t = E - e \sin(E)
    \end{cases}
$$


And finally we will replace the variables:

$$
    \frac{dE}{dt} = \frac{1}{1 - e\cos(E)} = \frac{1}{r}
$$


<kbd>
Нет страшнее зверя в сибирских лесах, чем разъяренный заяц-мутант.  
  Вы видели, какие у него зубы? О, даже медведь боится этих зубов! А, как известно, 
  медведи больше ничего не боятся.
</kbd>
