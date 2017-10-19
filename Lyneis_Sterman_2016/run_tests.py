import pysd
print(pysd.__version__)

pysd.testing.behavior_test('bounded_rationality.feature')
print('\n')
pysd.testing.behavior_test('extreme_conditions_test.feature')