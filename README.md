# DS_miniproject_1
### This is an implementation of Ricart-Agrawala algorithm in python with sockets.
Done By Siim-Morten Ojasalu <br>
Introductory video at: https://youtu.be/mao0nRWR4eQ
### Python 3 required
The program is called from the commandline with the command "python3 project1.py n", where n is the amount of threads activated. 
#### For example:
"python3 project1.py 6" will launch the program with 6 threads running.

#### Quick overview
Commands available while the program is running:

<b>$ List</b>: This command lists all the nodes and its states. For instance <br><br>
$ List
<ul>
<li>P1, DO-NOT-WANT
<li>P2, DO-NOT-WANT
<li>P3, DO-NOT-WANT
<li>P4, DO-NOT-WANT
<li>P5, DO-NOT-WANT
<li>P6, DO-NOT-WANT
</ul> <br>

<b>$ time-cs t</b> This command sets the time to the critical section for all processes [10, t], meaning that each process takes its critical section holding time randomly from the interval.<br>
For example: "time-cs 20" sets the interval to be [10,20]<br><br>
<b>$ time-p t</b> This command sets the time-out interval for all processes [5, t], meaning that each process takes its timeout randomly from the interval.<br>
For example: "time-p 20" sets the interval to be [5,20].
