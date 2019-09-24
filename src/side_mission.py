# The purpose of the file is to satisfy bujji chan

import utils.read_matfiles as utility
import matplotlib.pyplot as plt
import matplotlib.image as image
from tqdm import tqdm, trange
import numpy as np
from scipy import io as sio
import pandas as pd
import os
from IPython.display import display
fmri_files = ["./target_rdms/target_fmri_92.mat",
              "./target_rdms/target_fmri_118.mat"]
fmri_keys = ["EVC_RDMs", "IT_RDMs"]

meg_files = ["./target_rdms/target_meg_92.mat",
             "./target_rdms/target_meg_118.mat"]
meg_keys = ["MEG_RDMs_early", "MEG_RDMs_late"]

subjects_names = [x for x in range(15)]


def get_image_num(image_num, image_set):
    if image_set == 92:
        return str(
            image_num) if image_num > 9 else "0"+str(image_num)
    else:
        if image_num < 10:
            return "00"+str(image_num)
        elif image_num < 100:
            return "0"+str(image_num)
        else:
            return str(image_num)


def get_correllation_row(rdm, image_set, image_id):
    corr_pearson = {}
    for subject1 in range(15):
        corr_pearson[subject1] = []
        for subject2 in range(15):
            row1 = rdm[subject1, image_id, :]
            row2 = rdm[subject2, image_id, :]
            corr_pearson[subject1].append(
                np.corrcoef(row1, row2)[0, 1])
        corr_pearson[subject1] = np.array(
            corr_pearson[subject1])
    return pd.DataFrame.from_dict(
        corr_pearson, orient='index', columns=subjects_names)


def plot_image(id, image_set):
    temp = 'image_{}'.format(get_image_num(id, image_set))
    path = os.path.join('..', 'data', 'Training_Data',
                        '{}_Image_Set'.format(image_set), '{}images'.format(image_set), temp)
    img = plt.imread(path + '.jpg')
    plt.imshow(img)


def get_image_pair_variation(rdm, i=7, j=7, meg=False):
    if not meg:
        tqdm.write(rdm[:, i, j])
    else:
        tqdm.write(np.mean(rdm, axis=1)[:, i, j])


def investigate(task='fmri', image_set=92, image_id=7):
    plot_image(image_id, image_set)
    if task == 'fmri':
        if image_set == 92:
            rdm = utility.load(fmri_files[0])
        else:
            rdm = utility.load(fmri_files[1])
        display('EVC' + "*"*40)
        display(get_correllation_row(
            rdm[fmri_keys[0]], image_set, image_id))
        display('IT' + "*"*40)
        display(get_correllation_row(
            rdm[fmri_keys[1]], image_set, image_id))
    else:
        if image_set == 92:
            rdm = utility.load(meg_files[0])
        else:
            rdm = utility.load(meg_files[1])
        display('Early' + "*"*40)
        display(get_correllation_row(
            np.mean(rdm[meg_keys[0]], axis=1), image_set, image_id))
        display()
        display('Late' + "*"*40)
        display(get_correllation_row(
            np.mean(rdm[meg_keys[1]], axis=1), image_set, image_id))
