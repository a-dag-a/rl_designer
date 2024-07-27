- [ ] Should the agent create a small signal circuit first?
- [ ] A second module will do 'synthesis' to convert the small-signal paramaters into actual transistor sizes


- Execute with ngspice 
Linux: `ngspice -b netlists\template__CS_Amp.cir`
- In Windows (if we do not want to add to path), setup a shortcut to the ngspice executable in the top folder
Windows: `.\ngspice.exe.lnk -b $pwd\netlists\template__CS_Amp.cir`

- Add a run description comment at the first line of the netlist template
----------------------------------------------------


# Thoughts on how best to cast impedance matching as a RL problem
1. We can discretize the movements along the Smith chart, and set a penalty on the number of distinct turns in the trajectory (since this will increase the order of the matchng network)

2. The discretization scheme will have to be some kind of nonlinear mapping, since it must discretize the path segments taken on the smith chart

3. At each turn of the game, the available actions must be:
- R (series resistance, +0.1 ohms)
- X (series reactance, +/- 0.1 ohms)
- G (shunt conductance, +0.1 mhos)
- B (shunt susceptance, +/- 0.1 mhos)
The increments chosen can be in steps of 0.1 (normalize to 50 ohms). Thus, these are steps on the grid traditionally drawn over most Smith charts. The increments can be positive or negative for reactive elements, while negative resistors are forbidden.
Note that the impedance will never stay on the 'impedance' grid as soon as we use a shunt element. So it is necessary to use a 'radius' or a basin near the desired macth point so as to conclude the game. 

4. Penalizing network order. This can be easily evaluated by:
- checking the simplified netlist
- checking the number of 'turns' in the matching trajectory.

5. While penalizing network order may lead to narrowband L match solutions, we can later more interesting terms to the cost funcitons to create wideband networks (for instance) (eg. by penalizing the integral of 'Q' along the trajectory, we can force the agent to generate a low-Q, wideband solution)

6. Using this to explore the LNA matching problem (generalizing to a general two port netowrk for matching), with the total power depending on the 'D' of the two port ABCD matrix. The optimum impedance match will occur at C = conjugate(D*Y_L). The reward function can be the power transferred to the load.
7. THe above probelm can also be generalized to PA load pull problems as well


--------------------------------------------------------------
The role of the agent here shall be to create a matching network that delivers as wideband an impedance match as possible using passive elements.


Concreteley, the agent acts directly on the netlist. 
So in the first version, we'll have an agent that only does ladder-type networks. SO all the functions that maniputlate the netlist stay in agent.py. This keeps the rest of the framework general, so that we can easily test out other agents.


Goal:
- Bandwidth
- Insertion loss

Actions:
- R,C,L either in shunt or series. These are all one-parameter elements
- After each such 'action' the agent can call ngspice for an evaluation of the reward
Rewards:



Elements to code:
- Agent
- Netlist generation function: Accepts an action token from the agent, and translates it to a netlist
- Environment


# Post processing the ngspice output
```
sed -i 's/ \+/,/g' tmp_spice/all.dat # substitues all (grousp of) spaces with a comma
sed -i 's/^,//g' tmp_spice/all.dat # removes the first comma in each line
```

Pipe it all together:
`sed 's/ \+/,/g' tmp_spice/all.dat | sed 's/^,//g' > tmp_spice/all.csv`

# View matching as a path planning problem on the Smith chart
The actual component values are not themselves important (unless they are infeasible values), so they should just be computed from the arcs that constitute the path

# gymnasium environment 
See https://medium.com/@ym1942/create-a-gymnasium-custom-environment-part-1-04ccc280eea9