import numpy as np
from tabulate import tabulate

class DomainRandomizer:

    distribution_fun_dict = {
        'uniform': np.random.uniform,
        'normal': np.random.normal,
        'choice': np.random.choice,
        }

    def __init__(self, seed=0):
        self.parameter_distributions = {}   # parameters name, distribution, and arguments
        self.sampled_parameters = {}        # parameters just sampled

        # reset seed
        np.random.seed(seed)

    def add(self, parameter_name, distribution, distribution_args):
        """
        Adds a parameter to randomize.
        @ parameter_name: str, name of the parameter
        @ distribution: ['uniform', 'normal', 'choice'], distribution of the parameter
        @ distribution_args: dict([arg=value, ...]), parameters of the chosen distribution (see numpy.random)
        """
        # check parameter types
        if type(parameter_name) != str:
            raise TypeError("Parameter \'name\' should be string.")
        if distribution not in DomainRandomizer.distribution_fun_dict.keys():
            raise KeyError("Implemented \'distribution\'(s) are in DomainRandomizer.distribution_fun_dict.keys()")
        if type(distribution_args) != dict:
            raise TypeError("Distribution \'args\' should be provided as a dict.")
        
        # add parameter
        if parameter_name not in self.parameter_distributions.keys():
            self.parameter_distributions[parameter_name] = {}
            self.parameter_distributions[parameter_name]['distribution'] = DomainRandomizer.distribution_fun_dict[distribution]
            self.parameter_distributions[parameter_name]['args'] = distribution_args
        else:
            raise Exception("Parameter %s already added to randomizer" % parameter_name)

    def sample(self):
        """
        Samples parameters' values from their associated distributions.

        Returns: dict, sampled parameters
        """
        for key, item in self.parameter_distributions.items():
            self.sampled_parameters[key] = item['distribution'](**item['args']) # unrol dictionary item['args']
        
        return self.sampled_parameters
    

    def summary(self):
        """
        Prints a summary of the parameters, distributions, and distribution arguments.
        """
        # table header
        table_rows = [['Parameter', 'Distribution', 'Arguments']]

        for param_name, item in self.parameter_distributions.items():
            # extract distribution name
            distribution_name = item['distribution'].__name__

            # create distribution arguments string
            arguments_string = ' '
            for arg_name, value in item['args'].items():
                arguments_string += arg_name + '=' + str(value) + ' '
            
            # append row 
            table_rows.append([param_name, distribution_name, arguments_string])
        
        # tabulate table rows
        table = tabulate(tabular_data=table_rows,  headers='firstrow', tablefmt='fancy_grid')

        print(table)