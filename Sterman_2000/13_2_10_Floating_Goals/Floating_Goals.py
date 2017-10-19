"""
Python model Floating_Goals.py
Translated using PySD version 0.7.12
"""
from __future__ import division
import numpy as np
from pysd import utils
import xarray as xr

from pysd.py_backend.functions import cache
from pysd import functions

_subscript_dict = {}

_namespace = {
    'TIME': 'time',
    'Time': 'time',
    'Desired State of the System': 'desired_state_of_the_system',
    'Goal Adjustment Time': 'goal_adjustment_time',
    'Initial Goal': 'initial_goal',
    'Initial State of the System': 'initial_state_of_the_system',
    'Net Change in Goal': 'net_change_in_goal',
    'Net Change in State': 'net_change_in_state',
    'State Adjustment Time': 'state_adjustment_time',
    'State of the System': 'state_of_the_system',
    'FINAL TIME': 'final_time',
    'INITIAL TIME': 'initial_time',
    'SAVEPER': 'saveper',
    'TIME STEP': 'time_step'}


@cache('step')
def desired_state_of_the_system():
    """
    Desired State of the System




    """
    return integ_desired_state_of_the_system()


@cache('run')
def goal_adjustment_time():
    """
    Goal Adjustment Time




    """
    return 1


@cache('run')
def initial_goal():
    """
    Initial Goal




    """
    return 0


@cache('run')
def initial_state_of_the_system():
    """
    Initial State of the System




    """
    return 0


@cache('step')
def net_change_in_goal():
    """
    Net Change in Goal




    """
    return (state_of_the_system() - desired_state_of_the_system()) / goal_adjustment_time()


@cache('step')
def net_change_in_state():
    """
    Net Change in State




    """
    return (desired_state_of_the_system() - state_of_the_system()) / state_adjustment_time()


@cache('run')
def state_adjustment_time():
    """
    State Adjustment Time

    [0,?]


    """
    return 1


@cache('step')
def state_of_the_system():
    """
    State of the System




    """
    return integ_state_of_the_system()


@cache('run')
def final_time():
    """
    FINAL TIME

    Month

    The final time for the simulation.
    """
    return 10


@cache('run')
def initial_time():
    """
    INITIAL TIME

    Month

    The initial time for the simulation.
    """
    return 0


@cache('step')
def saveper():
    """
    SAVEPER

    Month [0,?]

    The frequency with which output is stored.
    """
    return time_step()


@cache('run')
def time_step():
    """
    TIME STEP

    Month [0,?]

    The time step for the simulation.
    """
    return 0.03125


integ_desired_state_of_the_system = functions.Integ(lambda: net_change_in_goal(),
                                                    lambda: initial_goal())

integ_state_of_the_system = functions.Integ(lambda: net_change_in_state(),
                                            lambda: initial_state_of_the_system())
