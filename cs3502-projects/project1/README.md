# CS3502 P1: Multi-Threaded Programming
Banking simulation that demonstrates two threading concepts including race conditions and deadlocks. In addition
to this resolutions are implemented to solve these issues.

#Phase 1
Creates 5 banks accounts that the teller threads then operate on. 3 teller threads are made, each performing 3 
transactions. Because the accounts are a global resource and mutex locks are not used, race conditions occur.

#Phase 2 
Follows a similar structure with added features to prevent race conditions. Transactions are implemented through
functions to allow mutex locks to be added to them. This safer implementation of the methods limits the number
of threads allowed to access the accounts resource at a time to one.

#Phase 3
Takes the banking structure seen in the first two phases, however demonstrates a deadlock. A transfer function is 
defined and threads make use of this in a way that causes and indefinite deadlock. 

#Phase 4
Addresses the deadlock issue in phase 3. Strictly locks the account with the lower id first, as a means of keeping
consistency. 

#Running the programs
To run any of the phases simply type the command ./ followed by the phase
