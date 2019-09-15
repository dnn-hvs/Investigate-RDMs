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


def plot_meg(updated_subject_rdms, ind, image_set, images_dir, rdms, subject):
    rows = 20
    full_subj_rdms = rdms[subject]  # 20 x 92 x 92 or 20 x 118 x 118
    new_person_rdm = np.mean(rdms, axis=0)  # 20 x 92 x 92 or 20 x 118 x 118
    print(full_subj_rdms.shape, new_person_rdm.shape)
    for i in range(1, rows+1, 2):
        f, (a1, a2, a3, a4) = plt.subplots(1, 4, figsize=(15, 5))
        f.suptitle("RDM: {0:.4f}".format(
            updated_subject_rdms[ind[i-1][0]][ind[i-1][1]]))
        image_name = get_image_num(ind[i-1][0]+1, image_set)
        img = image.imread(images_dir+image_name+".jpg")
        a1.imshow(img)
        a1.set_xticklabels([])
        a1.set_yticklabels([])

        image_name = get_image_num(ind[i-1][1]+1, image_set)
        img = image.imread(images_dir+image_name+".jpg")
        a2.imshow(img)
        a2.set_xticklabels([])
        a2.set_yticklabels([])

        a3.set_title("Subject: " + str(subject))
        a3.plot([x for x in range(20)],
                full_subj_rdms[:, ind[i-1][0], ind[i-1][1]])

        a4.set_title("Mean of all Subjects")

        a4.plot([x for x in range(20)],
                new_person_rdm[:, ind[i-1][0], ind[i-1][1]])
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


def _investigate(image_set, subject, rdms, task="fmri"):
    images_dir = "../data/Training_Data/"+image_set + \
        "_Image_Set/"+image_set+"images/image_"
    if task == "fmri":
        subject_early_rdm = rdms[subject]
        min_ind, max_ind = sim_dissim_indices(subject_early_rdm)
        # plot_image(min_ind, max_ind, image_set, subject_early_rdm)
        plot(subject_early_rdm, min_ind, image_set, images_dir)
        plot(subject_early_rdm, max_ind, image_set, images_dir)
    elif task == "meg_mean":

        subject_rdm = np.mean(rdms, axis=1)[subject]
        min_ind, max_ind = sim_dissim_indices(subject_rdm)
        # plot_image(min_ind, max_ind, image_set, subject_early_rdm)
        plot_meg(subject_rdm, min_ind,
                 image_set, images_dir, rdms, subject)
        plot_meg(subject_rdm, max_ind,
                 image_set, images_dir, rdms, subject)

    else:
        subject_early_rdm = np.amin(rdms, axis=1)[subject]
        min_ind, _ = sim_dissim_indices(subject_early_rdm)
        plot_meg(subject_early_rdm, min_ind,
                 image_set, images_dir, rdms, subject)

        subject_late_rdm = np.amax(rdms, axis=1)[subject]
        _, max_ind = sim_dissim_indices(subject_late_rdm)
        plot_meg(subject_late_rdm, max_ind,
                 image_set, images_dir, rdms, subject)


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
            _investigate(image_set, subject,
                         rdms_dict[meg_keys[0]], task="meg_mean")
            break
        print("+"*30+"MEG Late RDMs"+"+"*30)
        for subject in range(15):
            print("+"*5, "Subject: ", subject, "+"*5)

            _investigate(image_set, subject,
                         rdms_dict[meg_keys[1]], task="meg_mean")
            break


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
                         rdms_dict[meg_keys[0]], task="meg")
        print("+"*30+"MEG Late RDMs"+"+"*30)
        for subject in range(15):
            print("+"*5, "Subject: ", subject, "+"*5)
            _investigate(image_set, subject,
                         rdms_dict[meg_keys[1]], task="meg")


# fmri_investigation()
