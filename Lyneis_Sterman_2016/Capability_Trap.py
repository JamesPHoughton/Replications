"""
Python model Capability_Trap.py
Translated using PySD version 0.8.1
"""
from __future__ import division
import numpy as np
from pysd import utils
import xarray as xr

from pysd.py_backend.functions import cache
from pysd.py_backend import functions

_subscript_dict = {}

_namespace = {
    'TIME': 'time',
    'Time': 'time',
    'Required Labor': 'required_labor',
    'Sensitivity of Labor to Capabilities': 'sensitivity_of_labor_to_capabilities',
    'Increase in Time Spent Working': 'increase_in_time_spent_working',
    'Time Spent Improving': 'time_spent_improving',
    'Output': 'output',
    'Change in Time Spent Working': 'change_in_time_spent_working',
    'Increase in Time Spent Improving': 'increase_in_time_spent_improving',
    'Change in Required Improvement Effort': 'change_in_required_improvement_effort',
    'Maximum Workweek': 'maximum_workweek',
    'Ramp in Required Output': 'ramp_in_required_output',
    'Authorized Labor': 'authorized_labor',
    'Ramp in Labor': 'ramp_in_labor',
    'Fraction of Time Spent Improving': 'fraction_of_time_spent_improving',
    'Fractional Change in Labor': 'fractional_change_in_labor',
    'Productivity': 'productivity',
    'Capabilities': 'capabilities',
    'Initial Labor': 'initial_labor',
    'Reference Productivity': 'reference_productivity',
    'Capability Increase': 'capability_increase',
    'Work Week': 'work_week',
    'Fraction of Time Spent Working': 'fraction_of_time_spent_working',
    'Sensitivity of Work Effort to Output': 'sensitivity_of_work_effort_to_output',
    'Time to Change Labor': 'time_to_change_labor',
    'Productivity of Improvement Effort': 'productivity_of_improvement_effort',
    'Sensitivity of Improvement Effort to Output': 'sensitivity_of_improvement_effort_to_output',
    'Time Spent Working': 'time_spent_working',
    'Required Improvement Effort': 'required_improvement_effort',
    'Adjustment for Labor': 'adjustment_for_labor',
    'Attrition': 'attrition',
    'Initial Required Output': 'initial_required_output',
    'Average Duration of Employment': 'average_duration_of_employment',
    'Sensitivity of Labor to Output Shortfall': 'sensitivity_of_labor_to_output_shortfall',
    'Hiring': 'hiring',
    'Required Output': 'required_output',
    'Step in Required Output': 'step_in_required_output',
    'Labor': 'labor',
    'Labor Adjustment Time': 'labor_adjustment_time',
    'Target Labor': 'target_labor',
    'Capability Decrease': 'capability_decrease',
    'Capability Delay Order': 'capability_delay_order',
    'Reference Fraction of Effort to Output': 'reference_fraction_of_effort_to_output',
    'Average Capability Loss Rate': 'average_capability_loss_rate',
    'Initial Capabilities': 'initial_capabilities',
    'Maximum Capabilities': 'maximum_capabilities',
    'Output Shortfall': 'output_shortfall',
    'Standard Workweek': 'standard_workweek',
    'FINAL TIME': 'final_time',
    'INITIAL TIME': 'initial_time',
    'SAVEPER': 'saveper',
    'TIME STEP': 'time_step'
}


@cache('step')
def required_labor():
    """
    Required Labor

    People

    component

    Required labor increases with the output shortfall.  The sensitivity of 
        labor to the shortfall determines how many people are sought in response 
        to a given output gap.  Required labor will also increase to provide 
        resources to boost capabilities, according to the Sensitivity of Labor to 
        Capabilities.
    """
    return labor() * (1 + sensitivity_of_labor_to_output_shortfall() * output_shortfall() +
                      sensitivity_of_labor_to_capabilities())


@cache('run')
def sensitivity_of_labor_to_capabilities():
    """
    Sensitivity of Labor to Capabilities

    Dmnl

    constant

    When positive, this parameter causes the firm to seek additional workers 
        to improve capabilities, even if there is no output shortfall.  The actual 
        workforce will then increase unless constrained by the authorized labor 
        force.  The default value is 0, implying hiring does not respond to 
        capabilities.  The larger the value, the more responsive hiring is to the 
        pressure to improve capabilities.
    """
    return 0


@cache('run')
def increase_in_time_spent_working():
    """
    Increase in Time Spent Working

    Hours/week [-10,10,1]

    constant

    The magnitude of the exogenous increase in work effort, occuring at time 
        zero.
    """
    return 0


@cache('step')
def time_spent_improving():
    """
    Time Spent Improving

    Hours/week

    component

    The time spent on capability development and improvement is given by the 
        required improvement effort or the time available for improvmeent, 
        whichever is less.
    """
    return np.maximum(0,
                      np.minimum(maximum_workweek() - time_spent_working(),
                                 required_improvement_effort()))


@cache('step')
def output():
    """
    Output

    Units/week

    component

    Actual output is the product of the labor force,  work hours per week 
        spent on work effort (vs. improvement), and productivity.
    """
    return labor() * time_spent_working() * productivity()


@cache('step')
def change_in_time_spent_working():
    """
    Change in Time Spent Working

    Hours/week/Year

    component

    The amount of time spent working on average changes in proportion to the 
        output shortfall.  Positive shortfalls lead to an increase in hours per 
        person spent working (vs. improvement and capability development); a 
        negative shortfall (more output than required) leads to a reduction of 
        hours spent working.  The time spent working cannot rise above the maximum 
        workweek, so the rate of increase falls to zero as the time spent working 
        approaches the maximum.  In addition, the time spent working can increase 
        by a fixed amount at time zero (the Increase in Time Spent Working), using 
        the pulse function.
    """
    return time_spent_working() * sensitivity_of_work_effort_to_output() * output_shortfall() * (
        maximum_workweek() - time_spent_working()) / maximum_workweek() + (
            increase_in_time_spent_working() / time_step()) * functions.pulse(0, time_step())


@cache('step')
def increase_in_time_spent_improving():
    """
    Increase in Time Spent Improving

    Hours/week

    component

    If additional time is allocated to working harder (as an exogenous test), 
        the time allocated to working smarter falls by the same amount.
    """
    return -increase_in_time_spent_working()


@cache('step')
def change_in_required_improvement_effort():
    """
    Change in Required Improvement Effort

    Hours/(Year*week)

    component

    The time spent on capability development and improvement increases in 
        proportion to the output shortfall, with a gain determined by the 
        sensitivity of improvement to output.  The increase falls as the time 
        spent improving approaches the maximum workweek.  In addition, the time 
        for improvement can increase exogenously by a certain amount at time zero 
        as a test input (determined by the pulse function).
    """
    return time_spent_improving() * sensitivity_of_improvement_effort_to_output(
    ) * output_shortfall() * (maximum_workweek() - time_spent_improving()) / maximum_workweek() + (
        increase_in_time_spent_improving() / time_step()) * functions.pulse(0, time_step())


@cache('run')
def maximum_workweek():
    """
    Maximum Workweek

    Hours/week [40,100,1]

    constant

    The maximum average workweek for the workforce.
    """
    return 70


@cache('run')
def ramp_in_required_output():
    """
    Ramp in Required Output

    Units/week/Year [0,50,1]

    constant

    The slope of a linear ramp in required output, in units per year/year 
        added to the initial required output rate.
    """
    return 0


@cache('step')
def authorized_labor():
    """
    Authorized Labor

    People

    component

    Authorized Labor can be increased or decreased by a certain amount at time 
        zero, or follow a linear ramp with slope "Ramp in Labor".
    """
    return np.maximum(0,
                      initial_labor() *
                      (1 + functions.step(fractional_change_in_labor(), time_to_change_labor()) +
                       functions.ramp(ramp_in_labor(), 0, 6)))


@cache('run')
def ramp_in_labor():
    """
    Ramp in Labor

    1/Year [-0.5,0.5,0.05]

    constant

    The slope of a linear ramp in authorized labor, as a fraction of the 
        initial labor force.
    """
    return 0


@cache('step')
def fraction_of_time_spent_improving():
    """
    Fraction of Time Spent Improving

    Dmnl

    component

    The fraction of the workweek spent on improvement and capability 
        development (vs. work effort).
    """
    return time_spent_improving() / work_week()


@cache('run')
def fractional_change_in_labor():
    """
    Fractional Change in Labor

    Dmnl [-1,1,0.01]

    constant

    An exogenous fractional change in the authorized labor force, representing 
        the impact of budget cuts in the workforce.
    """
    return 0


@cache('step')
def productivity():
    """
    Productivity

    Units/(Hours*Person)

    component

    For simplicity, productivity (units of output per person-hour of work 
        effort) is proportional to organizational capabilities.  Reference 
        productivity is set to initialize the model in equilibrium.
    """
    return reference_productivity() * capabilities()


@cache('step')
def capabilities():
    """
    Capabilities

    Dmnl

    component

    The capabilities of the organization are a stock, increased by improvement 
        effort and investment in capability development, and decreased as 
        capabilities erode.
    """
    return integ_capabilities()


@cache('run')
def initial_labor():
    """
    Initial Labor

    People

    constant

    The initial labor force.  Set by the user.
    """
    return 100


@cache('step')
def reference_productivity():
    """
    Reference Productivity

    Units/(Hours*Person)

    component

    The initial value of productivity.  Set to initialize the model in 
        equilibrium.
    """
    return initial_initial_required_outputinitial_laborstandard_workweekreference_fraction_of_effort_to_output(
    )


@cache('step')
def capability_increase():
    """
    Capability Increase

    1/Year

    component

    Capabilities increase as the result of effort applied to improvement 
        effort and capability development.  Improvement is determined by the 
        product of the labor force, the average time per person per week spent on 
        improvement and the productivity of improvement effort.  Improvement 
        slows, however, as capabilities approach their maximum value.
    """
    return labor() * time_spent_improving() * productivity_of_improvement_effort() * (
        maximum_capabilities() - capabilities()) / maximum_capabilities()


@cache('step')
def work_week():
    """
    Work Week

    Hours/week

    component

    The total workweek is the sum of the time spent working and time spent 
        improving.
    """
    return time_spent_working() + time_spent_improving()


@cache('step')
def fraction_of_time_spent_working():
    """
    Fraction of Time Spent Working

    Dmnl

    component

    The fraction of the workweek spent on work effort (vs improvement).
    """
    return time_spent_working() / work_week()


@cache('run')
def sensitivity_of_work_effort_to_output():
    """
    Sensitivity of Work Effort to Output

    1/Year [0,10,0.25]

    constant

    The larger the sensitivity, the more responsive work effort will be to the 
        output shortfall.  The default value is zero.
    """
    return 0


@cache('run')
def time_to_change_labor():
    """
    Time to Change Labor

    Year

    constant

    The time at which the change in authorized labor occurs.
    """
    return 0


@cache('step')
def productivity_of_improvement_effort():
    """
    Productivity of Improvement Effort

    (1/(Person*Hours/week))/Year [0,0.01]

    component

    The productivity of improvement effort is the increase in capabilities per 
        person-hour of improvement effort.  It is set so that the simulations 
        begin in equilibrium, with the time spent on improvement given by the 
        standard workweek less the initial time spent working, and with the 
        increase in capabilities offsetting capability erosion.
    """
    return initial_initial_capabilitiesaverage_capability_loss_ratemaximum_capabilitiesmaximum_capabilities1initial_laborstandard_workweek1reference_fraction_of_effort_to_output(
    )


@cache('run')
def sensitivity_of_improvement_effort_to_output():
    """
    Sensitivity of Improvement Effort to Output

    1/Year [0,1,0.1]

    constant

    The larger the sensitivity, the more responsive improvement effort will be 
        to the output shorftall.  The default value is zero.
    """
    return 0


@cache('step')
def time_spent_working():
    """
    Time Spent Working

    Hours/week

    component

    The average number of hours each worker spends each week producing (vs. 
        improvement effort).
    """
    return integ_time_spent_working()


@cache('step')
def required_improvement_effort():
    """
    Required Improvement Effort

    Hours/week

    component

    The number of hours per person per week needed to improve capabilities, 
        based on the cumulative response to the output shortfall.  Actual 
        improvement hours per week depend on the time available after work effort 
        is accounted for.
    """
    return integ_required_improvement_effort()


@cache('step')
def adjustment_for_labor():
    """
    Adjustment for Labor

    People/Year

    component

    Hiring is increased above or below the replacement of those who quit in 
        proportion to the gap between the target and actual workforce.  The labor 
        adjustment time governs how quickly the firm seeks to close that gap.
    """
    return (target_labor() - labor()) / labor_adjustment_time()


@cache('step')
def attrition():
    """
    Attrition

    People/Year

    component

    Workers stay with the firm for a period given by the average duration of 
        employment; the attrition profile is a third order Erlang lag.
    """
    return delay_hiring_average_duration_of_employment_initial_laboraverage_duration_of_employment_3(
    )


@cache('run')
def initial_required_output():
    """
    Initial Required Output

    Units/week

    constant

    The initial value for required output.  100 can be thought of as an index 
        value (100% of the initial level of required output).
    """
    return 100


@cache('run')
def average_duration_of_employment():
    """
    Average Duration of Employment

    Years

    constant

    The average tenure of a worker.
    """
    return 2


@cache('run')
def sensitivity_of_labor_to_output_shortfall():
    """
    Sensitivity of Labor to Output Shortfall

    Dmnl [0,1,0.05]

    constant

    When positive, this parameter causes the firm to seek additional workers 
        to close the gap between required and actual output.  The actual workforce 
        will then increase unless constrained by the authorized labor force.  The 
        default value is 0, implying hiring does not respond to the output 
        shortfall.  The larger the value, the more responsive hiring is to a given 
        output gap.
    """
    return 0


@cache('step')
def hiring():
    """
    Hiring

    People/Year

    component

    Hiring replaces those who leave (attrition) and adjusts the workforce 
        toward the authorized level.  The max function means there is a no layoff 
        policy.
    """
    return np.maximum(0, attrition() + adjustment_for_labor())


@cache('step')
def required_output():
    """
    Required Output

    Units/week

    component

    The required level of output.  Set by the user; begins at the reference 
        value, and can be increased by a certain amount, or follow a linear ramp 
        with a user-determined slope.
    """
    return initial_required_output() * (1 + functions.step(step_in_required_output(), 0)
                                        ) + functions.ramp(ramp_in_required_output(), 0, 6)


@cache('run')
def step_in_required_output():
    """
    Step in Required Output

    Dmnl [0,2,0.01]

    constant

    The fractional step increase in required output.  Set by the user.
    """
    return 0


@cache('step')
def labor():
    """
    Labor

    People

    component

    The labor force.  Increased by hiring and reduced by attrition.
    """
    return integ_labor()


@cache('run')
def labor_adjustment_time():
    """
    Labor Adjustment Time

    Years

    constant

    The average time over which the firm seeks to close the gap between the 
        target and actual labor force.
    """
    return 0.25


@cache('step')
def target_labor():
    """
    Target Labor

    People

    component

    The target used to determine hiring is the required number of workers 
        given the output shortfall or the authorized number (based on budget or 
        other consideration), whichever is less.
    """
    return np.minimum(authorized_labor(), required_labor())


@cache('step')
def capability_decrease():
    """
    Capability Decrease

    1/Year

    component

    Capabilities erode over time after a certain delay, with a mean lag given 
        by the reciprocal of the fractional capability erosion rate. Capability 
        erosion is modeled as an Erlang lag.  The user can specify the order of 
        the delay.
    """
    return delay_capability_increase_1average_capability_loss_rate_capabilitiesaverage_capability_loss_rate_capability_delay_order(
    )


@cache('run')
def capability_delay_order():
    """
    Capability Delay Order

    Dmnl [1,6,1]

    constant

    The order of the delay governing capability erosion.
    """
    return 3


@cache('run')
def reference_fraction_of_effort_to_output():
    """
    Reference Fraction of Effort to Output

    Dmnl [0,1]

    constant

    The initial fraction of the workweek devoted to output.  The remainder is 
        devoted to improvement and investment in capabilities.
    """
    return 0.8


@cache('run')
def average_capability_loss_rate():
    """
    Average Capability Loss Rate

    1/Year

    constant

    The fractional rate at which capabilities erode as personnel turn over and 
        as environmental, technological, competitive and other conditions change.
    """
    return 0.5


@cache('run')
def initial_capabilities():
    """
    Initial Capabilities

    Dmnl

    constant

    The initial level of capabilities, determined by the user.
    """
    return 1


@cache('run')
def maximum_capabilities():
    """
    Maximum Capabilities

    Dmnl

    constant

    The maximum level of capabilities, determined by the user.
    """
    return 10


@cache('step')
def output_shortfall():
    """
    Output Shortfall

    Dmnl

    component

    The gap between required and actual output, as a fraction of required 
        output.
    """
    return (required_output() - output()) / required_output()


@cache('run')
def standard_workweek():
    """
    Standard Workweek

    Hours/week

    constant

    The normal workweek.
    """
    return 40


@cache('run')
def final_time():
    """
    FINAL TIME

    Year

    constant

    The final time for the simulation.
    """
    return 5


@cache('run')
def initial_time():
    """
    INITIAL TIME

    Year

    constant

    The initial time for the simulation.
    """
    return -1


@cache('step')
def saveper():
    """
    SAVEPER

    Year [0,?]

    component

    The frequency with which output is stored.
    """
    return time_step()


@cache('run')
def time_step():
    """
    TIME STEP

    Year [0,?]

    constant

    The time step for the simulation.
    """
    return 0.015625


integ_capabilities = functions.Integ(lambda: capability_increase() - capability_decrease(),
                                     lambda: initial_capabilities())


initial_initial_required_outputinitial_laborstandard_workweekreference_fraction_of_effort_to_output = functions.Initial(lambda: initial_required_output()/(initial_labor()*standard_workweek()*reference_fraction_of_effort_to_output()))


initial_initial_capabilitiesaverage_capability_loss_ratemaximum_capabilitiesmaximum_capabilities1initial_laborstandard_workweek1reference_fraction_of_effort_to_output = functions.Initial(lambda: initial_capabilities()*average_capability_loss_rate()*(maximum_capabilities()/(maximum_capabilities()-1))/(initial_labor()*standard_workweek()*(1-reference_fraction_of_effort_to_output())))

integ_time_spent_working = functions.Integ(
    lambda: change_in_time_spent_working(),
    lambda: standard_workweek() * reference_fraction_of_effort_to_output())

integ_required_improvement_effort = functions.Integ(
    lambda: change_in_required_improvement_effort(),
    lambda: standard_workweek() * (1 - reference_fraction_of_effort_to_output()))

delay_hiring_average_duration_of_employment_initial_laboraverage_duration_of_employment_3 = functions.Delay(
    lambda: hiring(), lambda: average_duration_of_employment(),
    lambda: initial_labor() / average_duration_of_employment(), lambda: 3)

integ_labor = functions.Integ(lambda: hiring() - attrition(), lambda: initial_labor())

delay_capability_increase_1average_capability_loss_rate_capabilitiesaverage_capability_loss_rate_capability_delay_order = functions.Delay(
    lambda: capability_increase(), lambda: 1 / average_capability_loss_rate(),
    lambda: capabilities() * average_capability_loss_rate(), lambda: capability_delay_order())
