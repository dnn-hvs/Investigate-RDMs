import utils.read_matfiles as utility
import matplotlib.pyplot as plt
import matplotlib.image as image

import numpy as np

fmri_files = ["./target_rdms/target_fmri_92.mat",
              "./target_rdms/target_fmri_118.mat"]
fmri_keys = ["EVC_RDMs", "IT_RDMs"]

meg_files = ["./target_rdms/target_meg_92.mat",
             "./target_rdms/target_meg_118.mat"]
meg_keys = ["MEG_RDMs_early", "MEG_RDMs_late"]


def get_image_num(image_num, image_set):
    if image_set == "92":
        return str(
            image_num) if image_num > 9 else "0"+str(image_num)
    else:
        if image_num < 10:
            return "00"+str(image_num)
        elif image_num < 100:
            return "0"+str(image_num)
        else:
            return str(image_num)


def plot(rdms, ind, image_set, images_dir):
    columns = 2
    rows = 20
    for i in range(1, rows+1, 2):
        fig = plt.figure()
        plt.title("RDM: {0:.4f}".format(rdms[ind[i-1][0]][ind[i-1][1]]))
        fig.add_subplot(1, columns, 1)
        image_name = get_image_num(ind[i-1][0]+1, image_set)
        img = image.imread(images_dir+image_name+".jpg")
        plt.imshow(img)
        plt.xticks([])
        plt.yticks([])

        fig.add_subplot(1, columns, 2)
        image_name = get_image_num(ind[i-1][1]+1, image_set)
        img = image.imread(images_dir+image_name+".jpg")
        plt.imshow(img)
        plt.xticks([])
        plt.yticks([])
        plt.show()


def sim_dissim_indices(rdms):
    row_size, col_size = rdms.shape
    rdms = rdms.reshape(row_size*col_size, )
    min_ind, max_ind = [], []
    sorted_rdms_ind = np.argsort(rdms)
    min_10_ind = sorted_rdms_ind[row_size:row_size+20]
    max_10_ind = sorted_rdms_ind[:row_size*col_size-21:-1]
    min_ind.append([(index//row_size, index % row_size)
                    for index in min_10_ind])
    max_ind.append([(index//row_size, index % row_size)
                    for index in max_10_ind])
    return min_ind[0], max_ind[0]


def _investigate(image_set, rdms, task="fmri"):
    images_dir = "../data/Training_Data/"+image_set + \
        "_Image_Set/"+image_set+"images/image_"
    subject_early_rdm = rdms
    min_ind, max_ind = sim_dissim_indices(subject_early_rdm)
    plot(subject_early_rdm, min_ind, image_set, images_dir)
    plot(subject_early_rdm, max_ind, image_set, images_dir)


def fmri_investigation(file_names=fmri_files,):
    for file_name in file_names:
        print("File Name: ", file_name)
        if "92" in file_name:
            image_set = "92"
        else:
            image_set = "118"
        rdms_dict = utility.load(file_name)
        print(("+"*30+"RDMs : Image Set :: {}"+"+"*30).format(image_set))
        _investigate(image_set, rdms_dict[fmri_keys[0]])
