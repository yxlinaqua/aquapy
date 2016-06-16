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


    def _SNR(self, flux, ivar):
        pass

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