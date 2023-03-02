"""
Module defining global configs.

Mainly used by the Optimizer class, it defines basic solver parameters, such as
tolerance and time limit.

See also
--------
`Gurobi tolerances and the limitations of double-precision arithmetic <https://www.gurobi.com/documentation/9.5/refman/grb_tolerances_and_the_lim.html>`_.
"""

__author__ = "Alexandre Florio"

#: Strict inequality epsilon used for split decisions (defined in the paper). *(float)*
epsilon = 1e-4

solver_feas_tol = 1e-7 #: Gurobi primal feasibility tolerance (Gurobi default: 1e-6). *(float)*
solver_int_tol = 1e-6  #: Gurobi integer feasibility tolerance (Gurobi default: 1e-5). *(float)*
solver_opt_tol = 1e-7  #: Gurobi dual feasibility tolerance (Gurobi default: 1e-6). *(float)*

time_limit = 60 #: Solver time limit (in seconds) *(int)*

# model parameters
indicator_constraints = True #: Flag to implement linear separator constraints as indicator constraints.
verbose = True               #: Flag to enable verbose output.
