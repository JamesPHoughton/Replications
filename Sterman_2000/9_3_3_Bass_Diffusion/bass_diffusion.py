"""
Python model bass_diffusion.py
Translated using PySD version 0.7.7
"""
from __future__ import division
import numpy as np
from pysd import utils
import xarray as xr

from pysd.functions import cache
from pysd import functions
from pysd import model

_subscript_dict = {}

_namespace = {
    'TIME': 'time',
    'Time': 'time',
    'Adopters A': 'adopters_a',
    'Adoption Fraction i': 'adoption_fraction_i',
    'Adoption from Advertising': 'adoption_from_advertising',
    'Adoption from Word of Mouth': 'adoption_from_word_of_mouth',
    'Adoption Rate AR': 'adoption_rate_ar',
    'Advertising Effectiveness a': 'advertising_effectiveness_a',
    'Contact Rate c': 'contact_rate_c',
    'Potential Adopters P': 'potential_adopters_p',
    'Total Population N': 'total_population_n',
    'FINAL TIME': 'final_time',
    'INITIAL TIME': 'initial_time',
    'SAVEPER': 'saveper',
    'TIME STEP': 'time_step'
}


@cache('step')
def adopters_a():
    """
    Adopters A

    Individuals


    """
    return integ_adopters_a()


@cache('run')
def adoption_fraction_i():
    """
    Adoption Fraction i

    Individuals/Individual

    Likelihood of adoption from word of mouth, given exposure.
    """
    return 0.1


@cache('step')
def adoption_from_advertising():
    """
    Adoption from Advertising

    Individuals/Day


    """
    return advertising_effectiveness_a() * potential_adopters_p()


@cache('step')
def adoption_from_word_of_mouth():
    """
    Adoption from Word of Mouth

    Individuals/Day


    """
    return contact_rate_c() * adoption_fraction_i() * potential_adopters_p() * adopters_a(
    ) / total_population_n()


@cache('step')
def adoption_rate_ar():
    """
    Adoption Rate AR

    Individuals/Day


    """
    return adoption_from_advertising() + adoption_from_word_of_mouth()


@cache('run')
def advertising_effectiveness_a():
    """
    Advertising Effectiveness a

    Individuals/Individual/Day


    """
    return 0.001


@cache('run')
def contact_rate_c():
    """
    Contact Rate c

    Individuals/Individual/Day


    """
    return 5


@cache('step')
def potential_adopters_p():
    """
    Potential Adopters P

    Individuals


    """
    return integ_potential_adopters_p()


@cache('run')
def total_population_n():
    """
    Total Population N

    Individuals


    """
    return 1000


@cache('run')
def final_time():
    """
    FINAL TIME

    Day

    The final time for the simulation.
    """
    return 100


@cache('run')
def initial_time():
    """
    INITIAL TIME

    Day

    The initial time for the simulation.
    """
    return 0


@cache('step')
def saveper():
    """
    SAVEPER

    Day [0,?]

    The frequency with which output is stored.
    """
    return time_step()


@cache('run')
def time_step():
    """
    TIME STEP

    Day [0,?]

    The time step for the simulation.
    """
    return 1


integ_adopters_a = functions.Integ(lambda: adoption_rate_ar(), lambda: 0)

integ_potential_adopters_p = functions.Integ(lambda: -adoption_rate_ar(), lambda: 500)
