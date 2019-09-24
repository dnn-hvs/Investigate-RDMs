# The purpose of the file is to satisfy bujji chan

import utils.read_matfiles as utility
import matplotlib.pyplot as plt
import matplotlib.image as image
from tqdm import tqdm, trange
import numpy as np
from scipy import io as sio

fmri_files = ["./target_rdms/target_fmri_92.mat",
              "./target_rdms/target_fmri_118.mat"]
fmri_keys = ["EVC_RDMs", "IT_RDMs"]

meg_files = ["./target_rdms/target_meg_92.mat",
             "./target_rdms/target_meg_118.mat"]
meg_keys = ["MEG_RDMs_early", "MEG_RDMs_late"]

corr_pearson = {}


def get_correllation_row(rdm,  name, image_set, image_id=7):
    for subject1 in trange(15):
        corr_pearson['Subject_{}'.format(subject1)] = []
        for subject2 in trange(15):
            row1 = rdm[subject1, image_id, :]
            row2 = rdm[subject2, image_id, :]
            corr_pearson['Subject_{}'.format(subject1)].append(
                np.corrcoef(row1, row2)[0, 1])
    sio.savemat(name + "_{}.mat".format(image_set), corr_pearson)


def get_image_pair_variation(rdm, i=7, j=7, meg=False):
    if not meg:
        tqdm.write(rdm[:, i, j])
    else:
        tqdm.write(np.mean(rdm, axis=1)[:, i, j])


def fmri_investigation_row():
    for file_name in tqdm(fmri_files):
        if "92" in file_name:
            image_set = "92"
        else:
            image_set = "118"
        rdms_dict = utility.load(file_name)
        tqdm.write(
            ("+"*30+"EVC RDMs : Image Set :: {}"+"+"*30).format(image_set))
        for _ in trange(15):
            get_correllation_row(
                rdms_dict[fmri_keys[0]], 'fmri_row_evc', image_set)
        tqdm.write(("+"*30+"IT RDMs : Image Set :: {}"+"+"*30).format(image_set))
        for _ in trange(15):
            get_correllation_row(
                rdms_dict[fmri_keys[1]], 'fmri_row_it', image_set)


def meg_investigation_row():
    for file_name in tqdm(meg_files):
        if "92" in file_name:
            image_set = "92"
        else:
            image_set = "118"
        rdms_dict = utility.load(file_name)
        tqdm.write(("+"*30+"MEG Early RDMs : Image Set :: {}" +
                    "+"*30).format(image_set))
        for _ in range(15):
            get_correllation_row(
                np.mean(rdms_dict[meg_keys[0]], axis=1), 'meg_row_early', image_set)

        tqdm.write(("+"*30+"MEG Late RDMs : Image Set :: {}" +
                    "+"*30).format(image_set))
        for _ in range(15):
            get_correllation_row(
                np.mean(rdms_dict[meg_keys[1]], axis=1), 'meg_row_late', image_set)


if __name__ == '__main__':
    fmri_investigation_row()
    meg_investigation_row()
    a = sio.loadmat('fmri_row_evc_92')
    print(a)
