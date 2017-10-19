# Created by houghton at 10/6/17
Feature: The decision rule is boundedly rational
  # Enter feature description here

  Background: Model Setup
    Given the model 'Capability_Trap.mdl'

  Scenario: The Decision Rule is Rational
    When Step in Required Output is set to 1
    And Sensitivity of Work Effort to Output is set to 6
    And the model is run
    Then Output Shortfall is less than .01 at time 5

  Scenario: The Decision Rule is Rational with an infinite Maximum Workweek
    When Maximum Workweek is set to 10000000
    When Step in Required Output is set to 1
    And Sensitivity of Work Effort to Output is set to 6
    And the model is run
    Then Output Shortfall is less than .01 at time 5

  Scenario: The Decision Rule is Rational when capacity is fixed
    When Capabilities is set to 1
    When Step in Required Output is set to 1
    And Sensitivity of Work Effort to Output is set to 6
    And the model is run
    Then Output Shortfall is less than .01 at time 5

  Scenario: The Decision Rule is Rational when Step is Temporary



