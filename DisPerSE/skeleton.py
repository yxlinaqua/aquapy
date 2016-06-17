# -*- coding: utf-8 -*-
"""

Author
------
Bo Zhang

Email
-----
bozhang@nao.cas.cn

Created on
----------
- Thu Jun  16 14:12:00 2016     init

Modifications
-------------
- Thu Jun  16 14:12:00 2016     init

Aims
----
- read NDskeleton result text file

"""

import numpy as np
from astropy.table import Table


class SkeletonData():
    """ A class to represent NDskeleton results """

    def __init__(self, filepath=None):
        if filepath is None:
            print("@Cham: init SkeletonData instance [empty]...")
        else:
            print("@Cham: init SkeletonData instance [%s]..."%filepath)
        self.filepath = filepath
        self.data_loaded = False
        self.header = ''
        self.ndim = 0
        self.comments = ''
        self.bbox_x0 = np.array([0, 0])*np.nan
        self.bbox_delta = np.array([0, 0])*np.nan
        self.critical_points = []   # list
        self.filaments = []
        self.critical_points_data = []
        self.filaments_data = []


class CriticalPoint():
    """ A class to represent NDskeleton [CRITICAL POINTS] """

    def __init__(self, lines=None):
        # header line for this critical point
        header_line_split = lines[0].split(' ')
        self.type = np.int(header_line_split[0])
        self.pos = np.array([np.int64(pos) for pos in header_line_split[1:-3]])
        self.value = np.float64(header_line_split[-3])
        self.pairID = np.int64(header_line_split[-2])
        self.boundary = np.int64(header_line_split[-1])
        # ndim infered from string length
        self.ndim_infered = len(header_line_split) - 4

        # nfil
        self.nfil = np.int64(lines[1].split(' ')[1])
        assert self.nfil == len(lines) - 2

        # destId & filId
        self.data = np.nan * np.ones((self.nfil, 2), dtype=np.int64)
        self.destId = np.nan * np.ones((self.nfil, 1), dtype=np.int64)
        self.filId = np.nan * np.ones((self.nfil, 1), dtype=np.int64)
        for i in xrange(self.nfil):
            line_split = lines[i + 2].split(' ')
            self.destId[i] = np.int64(line_split[1])
            self.filId[i] = np.int64(line_split[2])
            self.data[i, :] = np.array([self.destId[i], self.filId[i]]).flatten()


class Filament():
    """ A class to represent NDskeleton [FILAMENTS] """

    def __init__(self, lines=None):
        # header line for this filament
        header_line_split = lines[0].split(' ')
        self.cp1 = np.int64(header_line_split[0])
        self.cp2 = np.int64(header_line_split[1])
        self.nsamp = np.int64(header_line_split[2])
        assert self.nsamp == len(lines) - 1

        # ndim infered from string length
        self.ndim_infered = len(lines[1].split(' ')) - 1

        # pos
        self.P = np.nan * np.ones((self.nsamp, self.ndim_infered), dtype=np.float64)
        for i in xrange(self.nsamp):
            line_split = lines[i + 1].split(' ')
            for j in xrange(self.ndim_infered):
                self.P[i, j] = np.float64(line_split[j + 1])


def _find_data_block_position():
    """find the head and tail line for 4 data blocks

    Returns
    -------
    db_pos: numpy.ndarray
        a 4x2 numpy array including the head and tail line
    """
    pass


def _read_data_block_critical_points():
    pass


def _read_data_block_critical_points_data():
    pass


def _read_data_block_filaments():
    pass


def _read_data_block_filaments_data():
    pass


def test_on_data():
    # test data
    test_data_file_path = './DisPerSE/data/N.fits.up.NDskl.a.NDskl'

    # read file
    f = open(test_data_file_path, mode='r')
    lines = f.readlines()
    f.close()
    # cut \n tails
    lines = [_[:-1] for _ in lines]

    # find marks
    keywords = ['BBOX',
                '[CRITICAL POINTS]',
                '[FILAMENTS]',
                '[CRITICAL POINTS DATA]',
                '[FILAMENTS DATA]']
    n_lines = np.zeros((len(keywords), 1), dtype=np.int)
    for i_keyword, keyword in enumerate(keywords):
        for i_line, line in enumerate(lines):
            if line.find(keyword) > -1:
                n_lines[i_keyword] = i_line
                print('@Cham: found keyword ''%s'' in Line %d ...'
                      % (keyword, i_line+1))
                break
    # find n_lines for each of the blocks
    n_lines_blocks = np.zeros((len(keywords), 2), dtype=np.int)
    n_lines_blocks[:, 0] = n_lines.flatten()
    n_lines_blocks[:-1, 1] = n_lines[1:].flatten()
    n_lines_blocks[-1, 1] = len(lines)
    print n_lines_blocks


    # skeldata = []
    # 1. header
    assert lines[0] == 'ANDSKEL'
    header = lines[0]

    # 2. ndim
    ndim = np.int(lines[1])

    # 3. comments
    comments = lines[2:n_lines_blocks[0, 0]]

    # 4. bbox (assumed to be single-line)
    bbox_str_seped = lines[n_lines_blocks[0, 0]].split(' ')
    bbox_x0 = np.array(eval(bbox_str_seped[1]))
    bbox_delta = np.array(eval(bbox_str_seped[2]))

    # 5. critical points
    lines[n_lines_blocks[1, 0]+1:n_lines_blocks[1, 1]]

    # 6. filaments
    lines[n_lines_blocks[2, 0]+1:n_lines_blocks[2, 1]]

    # 7. critical points data
    lines[n_lines_blocks[3, 0]+1:n_lines_blocks[3, 1]]

    # 8. filaments data
    lines[n_lines_blocks[4, 0]+1:n_lines_blocks[4, 1]]


if __name__ == '__main__':
    test_on_data()