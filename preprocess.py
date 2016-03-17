import lib
from _globals import Config
from sklearn import preprocessing
from sklearn.preprocessing import PolynomialFeatures
import numpy



class Preprocess(object):

    def transform(self, data):
        """
        Method to be overridden in subclasses.
        Should accept a dataset.
        Should return the modified dataset.
        """
        return NotImplementedError


class ScalableInteraction(Preprocess):

    def transform(self, dataset, size=2, interaction_only=True):
        degree = 2  # keep this at 2, so it doesn't get too large.
        dims = len(dataset[0])
        poly = PolynomialFeatures(degree=degree, interaction_only=interaction_only)
        output = []
        for i,row in enumerate(dataset):
            if i % 100 == 0:
                print 'in row', i
            start, stop = 0, size
            #new_row = numpy.array([])
            new_row = []
            while stop <= dims:
                subsection = row[start:stop]
                sub = poly.fit_transform(subsection)
                start += size
                stop += size
                sub = list(sub)
                sub = list(sub[0])
                new_row = new_row + sub
            output.append(new_row)
        return output

    def each_transformation(self, dataset, slice_size=10):
        for size in range(2, 10):  # TODO move this to config file
            print 'in each_transformation. size={}'.format(size)
            yield self.transform(dataset), {'size': size, 'interaction_only': True}


class Interaction(Preprocess):


    def transform(self, dataset, degree=2, interaction_only=True):
        # keep degree at 2, so it doesn't get too large.
        poly = PolynomialFeatures(degree=degree,
                                  interaction_only=interaction_only)
        return poly.fit_transform(dataset)

    def each_transformation(self, dataset):
        yield self.transform(dataset), {'degree': 2, 'interaction_only': True}


class Polynomial(Preprocess):


    def transform(self, dataset, exponent):
        return lib.polynomial(dataset, exponent)


    def each_transformation(self, dataset):
        for exponent in range(Config.Polynomial.START, Config.Polynomial.STOP):
            yield self.transform(dataset, exponent), {'exponent': exponent}



class Scale(Preprocess):


    def transform(self, dataset, scale=True):
        # Define the scale param even though it's not used.
        # That way it's consistent with other Preprocess subclasses.
        return preprocessing.scale(dataset)


    def each_transformation(self, dataset):
        for i in range(1):
            yield self.transform(dataset), {'scale': True}



class Norm(Preprocess):


    def transform(self, dataset, norm):
        return preprocessing.normalize(dataset, norm=norm)


    def each_transformation(self, dataset):
        norms = ['l1', 'l2']
        for n in norms:
            yield self.transform(dataset, norm=n), {'norm': n}
