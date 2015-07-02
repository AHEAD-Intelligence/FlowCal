#!/usr/bin/python
#
# test_io.py - Unit tests for io module
#
# Author: Sebastian M. Castillo-Hair
# Date: 7/1/2015
#
# Requires:
#   * fc.io
#   * numpy
#

import fc.io
import numpy as np
import unittest

channel_names = ['FSC-H', 'SSC-H', 'FL1-H', 'FL2-H', 'FL3-H', 'Time']
filename = 'test/Data.001'

class TestTaborLabFCSDataLoading(unittest.TestCase):
    def setUp(self):
        pass

    def test_loading(self):
        '''
        Testing proper loading from FCS file.
        '''
        d = fc.io.TaborLabFCSData(filename)
        self.assertEqual(d.shape, (20949, 6))
        self.assertEqual(len(d.channel_info), 6)
        self.assertEqual(d.channels, channel_names)

class TestTaborLabFCSDataSlicing(unittest.TestCase):
    def setUp(self):
        self.d = fc.io.TaborLabFCSData(filename)
        self.n_samples = self.d.shape[0]

    def test_1d_slicing_with_scalar(self):
        '''
        Testing the 1D slicing with a scalar of a TaborLabFCSData object.
        '''
        ds = self.d[1]
        self.assertIsInstance(ds, fc.io.TaborLabFCSData)
        self.assertEqual(ds.shape, (6,))
        self.assertEqual(ds.channels, channel_names)
        self.assertEqual(len(ds.channel_info), 6)

    def test_1d_slicing_with_list(self):
        '''
        Testing the 1D slicing with a list of a TaborLabFCSData object.
        '''
        ds = self.d[range(10)]
        self.assertIsInstance(ds, fc.io.TaborLabFCSData)
        self.assertEqual(ds.shape, (10,6))
        self.assertEqual(ds.channels, channel_names)
        self.assertEqual(len(ds.channel_info), 6)

    def test_1d_slicing_with_list(self):
        '''
        Testing the 1D slicing with a list of a TaborLabFCSData object.
        '''
        ds = self.d[range(10)]
        self.assertIsInstance(ds, fc.io.TaborLabFCSData)
        self.assertEqual(ds.shape, (10,6))
        self.assertEqual(ds.channels, channel_names)
        self.assertEqual(len(ds.channel_info), 6)

    def test_slicing_channel_with_int(self):
        '''
        Testing the channel slicing with an int of a TaborLabFCSData object.
        '''
        ds = self.d[:,2]
        self.assertIsInstance(ds, fc.io.TaborLabFCSData)
        self.assertEqual(ds.shape, (self.n_samples,))
        self.assertEqual(ds.channels, [channel_names[2]])
        self.assertEqual(len(ds.channel_info), 1)

    def test_slicing_channel_with_string(self):
        '''
        Testing the channel slicing with a string of a TaborLabFCSData object.
        '''
        ds = self.d[:,'SSC-H']
        self.assertIsInstance(ds, fc.io.TaborLabFCSData)
        self.assertEqual(ds.shape, (self.n_samples,))
        self.assertEqual(ds.channels, ['SSC-H'])
        self.assertEqual(len(ds.channel_info), 1)

    def test_slicing_channel_with_int_array(self):
        '''
        Testing the channel slicing with an int array of a TaborLabFCSData 
        object.
        '''
        ds = self.d[:,[1,3]]
        self.assertIsInstance(ds, fc.io.TaborLabFCSData)
        self.assertEqual(ds.shape, (self.n_samples,2))
        self.assertEqual(ds.channels, [channel_names[1], channel_names[3]])
        self.assertEqual(len(ds.channel_info), 2)

    def test_slicing_channel_with_string_array(self):
        '''
        Testing the channel slicing with a string array of a TaborLabFCSData 
        object.
        '''
        ds = self.d[:,['FSC-H', 'FL3-H']]
        self.assertIsInstance(ds, fc.io.TaborLabFCSData)
        self.assertEqual(ds.shape, (self.n_samples,2))
        self.assertEqual(ds.channels, ['FSC-H', 'FL3-H'])
        self.assertEqual(len(ds.channel_info), 2)

    def test_slicing_sample(self):
        '''
        Testing the sample slicing of a TaborLabFCSData object.
        '''
        ds = self.d[:1000]
        self.assertIsInstance(ds, fc.io.TaborLabFCSData)
        self.assertEqual(ds.shape, (1000,6))
        self.assertEqual(ds.channels, channel_names)
        self.assertEqual(len(ds.channel_info), 6)

    def test_2d_slicing(self):
        '''
        Testing 2D slicing of a TaborLabFCSData object.
        '''
        ds = self.d[:1000,['SSC-H', 'FL3-H']]
        self.assertIsInstance(ds, fc.io.TaborLabFCSData)
        self.assertEqual(ds.shape, (1000,2))
        self.assertEqual(ds.channels, ['SSC-H', 'FL3-H'])
        self.assertEqual(len(ds.channel_info), 2)

class TestTaborLabFCSDataOperations(unittest.TestCase):
    def setUp(self):
        self.d = fc.io.TaborLabFCSData(filename)
        self.n_samples = self.d.shape[0]

    def test_sum_integer(self):
        '''
        Testing that the sum of a TaborLabFCSData object returns a 
        TaborLabFCSData object.
        '''
        ds = self.d + 3
        self.assertIsInstance(ds, fc.io.TaborLabFCSData)
        self.assertEqual(ds[254,3] - self.d[254,3], 3)
        
    def test_sqrt(self):
        '''
        Testing that the square root of a TaborLabFCSData object returns a 
        TaborLabFCSData object.
        '''
        ds = np.sqrt(self.d)
        self.assertIsInstance(ds, fc.io.TaborLabFCSData)
        self.assertEqual(ds[254,3], np.sqrt(self.d[254,3]))

    def test_sum(self):
        '''
        Testing that the sum of a TaborLabFCSData object returns an scalar.
        '''
        s = np.sum(self.d)
        self.assertIsInstance(s, np.uint64)

    def test_mean(self):
        '''
        Testing that the mean of a TaborLabFCSData object returns an scalar.
        '''
        m = np.mean(self.d)
        self.assertIsInstance(m, float)

    def test_std(self):
        '''
        Testing that the std of a TaborLabFCSData object returns an scalar.
        '''
        s = np.std(self.d)
        self.assertIsInstance(s, float)

    def test_mean_axis(self):
        '''
        Testing that the mean along the axis 0 of a TaborLabFCSData object 
        returns a TaborLabFCSData object.
        '''
        m = np.mean(self.d, axis = 0)
        self.assertIsInstance(m, fc.io.TaborLabFCSData)
        self.assertEqual(m.shape, (6,))
        
if __name__ == '__main__':
    unittest.main()
