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


def plot(rdms, ind, image_set, images_dir, task="fmri", full_meg_rdms=None):
    columns = 2 if task == "fmri" else 3
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

        if task != "fmri":
            fig.add_subplot(1, columns, 3)
            plt.plot([x for x in range(20)],
                     full_meg_rdms[:ind[i-1][0], ind[i-1][1]])
            plt.xticks([])
            plt.yticks([])
            plt.show()


def sim_dissim_indices(rdms):
    row_size, col_size = rdms.shape
    rdms = rdms.reshape(row_size*col_size, )
    # print(rdms)
    min, max = [], []
    sorted_rdms_ind = np.argsort(rdms)
    min_10_ind = sorted_rdms_ind[row_size:row_size+20]
    max_10_ind = sorted_rdms_ind[:row_size*col_size-21:-1]
    sorted_rdms_ind = np.argsort(rdms)
    min.append([(index//row_size, index % row_size) for index in min_10_ind])
    max.append([(index//row_size, index % row_size) for index in max_10_ind])
    return min[0], max[0]


def _investigate(image_set, subject, rdms, task="fmri", full_rdms=None):
    print(rdms.shape, full_rdms.shape)
    images_dir = "../data/Training_Data/"+image_set + \
        "_Image_Set/"+image_set+"images/image_"
    if task == "fmri":
        subject_early_rdm = rdms[subject]
        min_ind, max_ind = sim_dissim_indices(subject_early_rdm)
        # plot_image(min_ind, max_ind, image_set, subject_early_rdm)
        plot(subject_early_rdm, min_ind, image_set, images_dir)
        plot(subject_early_rdm, max_ind, image_set, images_dir)
    elif task == "meg_mean":
        subject_early_rdm = rdms[subject]
        min_ind, max_ind = sim_dissim_indices(subject_early_rdm)
        # plot_image(min_ind, max_ind, image_set, subject_early_rdm)
        plot(subject_early_rdm, min_ind, image_set,
             images_dir, task="fmri", full_meg_rdms=None)
        plot(subject_early_rdm, max_ind, image_set,
             images_dir, task="fmri", full_meg_rdms=None)
    else:
        subject_early_rdm = np.amin(rdms, axis=1)[subject]
        min_ind, _ = sim_dissim_indices(subject_early_rdm)
        plot(subject_early_rdm, min_ind, image_set, images_dir)

        subject_late_rdm = np.amax(rdms, axis=1)[subject]
        _, max_ind = sim_dissim_indices(subject_late_rdm)
        plot(subject_late_rdm, max_ind, image_set, images_dir)


def fmri_investigation():
    for file_name in fmri_files:
        if "92" in file_name:
            image_set = "92"
        else:
            image_set = "118"
        rdms_dict = utility.load(file_name)
        print("+"*30+"EVC RDMs"+"+"*30)
        for subject in range(15):
            print("+"*5, "Subject: ", subject, "+"*5)
            _investigate(image_set, subject, rdms_dict[fmri_keys[0]])
        print("+"*30+"IT RDMs"+"+"*30)
        for subject in range(15):
            print("+"*5, "Subject: ", subject, "+"*5)
            _investigate(image_set, subject, rdms_dict[fmri_keys[1]])


def meg_investigation():
    for file_name in meg_files:
        if "92" in file_name:
            image_set = "92"
        else:
            image_set = "118"
        rdms_dict = utility.load(file_name)
        print("+"*30+"MEG Early RDMs"+"+"*30)
        for subject in range(15):
            print("+"*5, "Subject: ", subject, "+"*5)
            _investigate(image_set, subject, np.mean(
                rdms_dict[meg_keys[0]], axis=1), full_rdms=rdms_dict[meg_keys[0]])
        print("+"*30+"MEG Late RDMs"+"+"*30)
        for subject in range(15):
            print("+"*5, "Subject: ", subject, "+"*5)

            _investigate(image_set, subject, np.mean(
                rdms_dict[meg_keys[1]], axis=1), full_rdms=rdms_dict[meg_keys[0]])


def meg_investigation_with_max():
    for file_name in meg_files:
        if "92" in file_name:
            image_set = "92"
        else:
            image_set = "118"
        rdms_dict = utility.load(file_name)
        print("+"*30+"MEG Early RDMs"+"+"*30)
        for subject in range(15):
            print("+"*5, "Subject: ", subject, "+"*5)
            _investigate(image_set, subject,
                         rdms_dict[meg_keys[0]], task="meg", full_rdms=rdms_dict[meg_keys[0]])
        print("+"*30+"MEG Late RDMs"+"+"*30)
        for subject in range(15):
            print("+"*5, "Subject: ", subject, "+"*5)
            _investigate(image_set, subject,
                         rdms_dict[meg_keys[1]], task="meg", full_rdms=rdms_dict[meg_keys[0]])


# fmri_investigation()
