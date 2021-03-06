import os
import numpy as np


def write_cut(cut_filename, cut, basename=None):
    if basename is None:
        basename = os.path.basename(os.path.splitext(cut_filename)[0])

    unique_cells = np.unique(cut)

    if 0 not in unique_cells:
        # if it happens that there is no zero cell, add it anyways
        unique_cells = np.insert(unique_cells, 0, 0)  # object, index, value to insert

    n_clusters = len(np.unique(cut))
    n_spikes = len(cut)

    write_list = []  # the list of values to write

    tab = '    '  # the spaces didn't line up with my tab so I just created a string with enough spaces
    empty_space = '               '  # some of the empty spaces don't line up to x tabs

    # we add 1 to n_clusters because zero is the garbage cell that no one uses
    write_list.append('n_clusters: %d\n' % (n_clusters))
    write_list.append('n_channels: 4\n')
    write_list.append('n_params: 2\n')
    write_list.append('times_used_in_Vt:%s' % ((tab + '0') * 4 + '\n'))

    zero_string = (tab + '0') * 8 + '\n'

    for cell_i in np.arange(n_clusters):
        write_list.append(' cluster: %d center:%s' % (cell_i, zero_string))
        write_list.append('%smin:%s' % (empty_space, zero_string))
        write_list.append('%smax:%s' % (empty_space, zero_string))
    write_list.append('\nExact_cut_for: %s spikes: %d\n' % (basename, n_spikes))

    # now the cut file lists 25 values per row
    n_rows = int(np.floor(n_spikes / 25))  # number of full rows

    remaining = int(n_spikes - n_rows * 25)
    cut_string = ('%3u' * 25 + '\n') * n_rows + '%3u' * remaining

    write_list.append(cut_string % (tuple(cut)))

    with open(cut_filename, 'w') as f:
        f.writelines(write_list)


def write_clu(clu_filename, data):
    # the .clu files and the .cut files are different since the .clu files are the .cut files (with no manual sorting)
    # without the headers, and the values go from 1 -> N instead of 0 -> N, (1-based numbering instead of 0-based). Thus
    # we add 1 to the .cut data to get the .clu data

    data = np.asarray(data).astype(int)  # ensuring that the data is the integer data-type

    data += 1  # making the data 1-based instead of 0-based

    # calculating the number of clusters
    n_clust = len(np.unique(data))

    # ensuring that the cluster number is the 1st value
    data = np.concatenate(([n_clust], data))

    # saving the data as a column (delimter='\n') and integer format.
    np.savetxt(clu_filename, data, fmt='%d', delimiter='\n')
