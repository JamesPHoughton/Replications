# Created by houghton at 10/6/17
Feature: Extreme Conditions Test
  These tests ensure that the model is robust to extreme conditions

    Background: Model Setup
      Given the model 'Capability_Trap.mdl'

  Scenario: Capacity Goes to Zero With No Investment
    When Time Spent Improving is set to 0
    And the model is run
    Then Capabilities is less than .01 at time 5

  Scenario: No Demand
    When Required Output is set to 0
    And the model is run

    Then Required Improvement Effort is less than .01 at time 5
    But Required Improvement Effort is always greater than 0

    And Time Spent Working is less than .01 at time 5
    But Time Spent Working is always greater than 0


