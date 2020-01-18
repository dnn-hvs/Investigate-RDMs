from categories_mapping import image_set_92
import glob
import os
import numpy as np
import utils.read_matfiles as utility
from scipy import io
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from tqdm import tqdm
from tabulate import tabulate
from config import Config
keys = {
    "fmri": ["EVC_RDMs", "IT_RDMs"],
    "meg": ["MEG_RDMs_early", "MEG_RDMs_late"]
}


number_of_catg = 8
number_of_sub = 15


def plot_rdm(rdm1, rdm2, subject, labels, path, task):

    subplot_2 = [121, 122]
    fig = plt.figure(figsize=(20, 16))
    ax1 = fig.add_subplot(subplot_2[0])
    im1 = ax1.imshow(rdm1, interpolation='None', cmap='bwr',)
    ax1.set_title(f'{keys[task][0]}')
    ax1.set_yticks(np.arange(len(labels)))
    ax1.set_yticklabels(labels)
    # divider = make_axes_locatable(ax1)
    # cax = divider.append_axes('right', size='5%', pad=0.05)
    # fig.colorbar(im1, cax=cax, orientation='vertical')

    ax2 = fig.add_subplot(subplot_2[1])
    im2 = ax2.imshow(rdm2, interpolation='None', cmap='bwr',)
    ax2.set_title(f'{keys[task][1]}')
    ax2.set_yticks(np.arange(len(labels)))
    ax2.set_yticklabels(labels)

    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.31, 0.01, 0.37])
    fig.colorbar(im2, cax=cbar_ax)

    # divider = make_axes_locatable()
    # cax = divider.append_axes('right', size='2%', pad=0.0)
    # fig.colorbar(im2, cax=cax, orientation='vertical')

    plt.title(
        f'Subject: {subject}', x=-25, y=-0.2, fontsize=20)
    plt.savefig(os.path.join(path, "Subject_"+str(subject)+".png"))
    plt.close()


def get_labels_and_mapping(image_set):
    new_image_idx = 0
    old_new_idx_map = {}
    labels = []
    data_path = '../CategorisedData/'+str(image_set)+'images'

    # walk through the images in each category
    for cat_num in range(1, number_of_catg+1):
        image_list = glob.glob(os.path.join(data_path, str(cat_num), "*.jpg"))
        image_list.sort()
        for image_name in image_list:
            image_number = image_name.split("_")[-1].split(".")[0]
            old_image_idx = int(image_number) - 1

            # create a mapper for new indices of images vs old indices
            old_new_idx_map[new_image_idx] = old_image_idx
            labels = labels + [image_set_92[cat_num]]
            new_image_idx += 1

    return labels, old_new_idx_map


def rearrange(task, image_set):
    # load target_rdm
    rdms_dict = utility.load(
        './target_rdms/target_'+task+'_'+str(image_set)+'.mat')
    _, old_new_idx_map = get_labels_and_mapping(image_set)
    new_rdms = {
        keys[task][0]: np.zeros((number_of_sub, image_set, image_set)),
        keys[task][1]: np.zeros(
            (number_of_sub, image_set, image_set))

    }
    for key in keys[task]:
        for subj in range(number_of_sub):
            for i in range(image_set):
                for j in range(image_set):
                    if task == "meg":
                        rdm = np.mean(rdms_dict[key][subj], axis=0)
                        new_rdms[key][subj][i, j] = rdm[old_new_idx_map[i],
                                                        old_new_idx_map[j]]
                    else:
                        new_rdms[key][subj][i, j] = rdms_dict[key][subj][old_new_idx_map[i],
                                                                         old_new_idx_map[j]]

    path = "./rearranged_rdms/"
    if not os.path.exists(path):
        os.mkdir(path)
    key = keys[task][0]
    print(new_rdms[key].shape, new_rdms[key].shape, path +
          "rearranged_"+task+"_"+str(image_set)+".mat")
    io.savemat(path+"rearranged_"+task+"_"+str(image_set)+".mat", new_rdms)


def create_category_rdms(task, image_set):
    # load target_rdm
    rdms_dict = io.loadmat(
        "./rearranged_rdms/rearranged_"+task+"_"+str(image_set)+".mat")
    new_rdms = {
        keys[task][0]: np.zeros((number_of_sub, number_of_catg, number_of_catg)),
        keys[task][1]: np.zeros(
            (number_of_sub, number_of_catg, number_of_catg))

    }
    labels, old_new_idx_map = get_labels_and_mapping(image_set)
    prev_label = labels[0]
    last_ind = []
    for i, label in enumerate(labels):
        if prev_label != label:
            if len(last_ind) == 0:
                last_ind = last_ind + [(0, i-1)]
            else:
                last_ind = last_ind + [(last_ind[-1][1]+1, i-1)]
        prev_label = label
    last_ind = last_ind + [(last_ind[-1][1]+1, image_set-1)]

    for key in keys[task]:
        for subj in range(number_of_sub):
            for cat_num1 in range(number_of_catg):
                for cat_num2 in range(number_of_catg):
                    new_rdms[key][subj][cat_num1, cat_num2] = np.mean(
                        rdms_dict[key][subj][last_ind[cat_num1]
                                             [0]:last_ind[cat_num1][1]+1, last_ind[cat_num2]
                                             [0]:last_ind[cat_num2][1]+1])

    path = "./categorised_rdms/"
    if not os.path.exists(path):
        os.mkdir(path)
    io.savemat(path+"categorised_"+task+"_"+str(image_set)+".mat", new_rdms)


def visualise_category_rdms(task, image_set):
    rdms_dict = io.loadmat(
        "./categorised_rdms/categorised_"+task+"_"+str(image_set)+".mat")
    # print(rdms_dict[keys[task][0]].shape)
    key1, key2 = keys[task][0], keys[task][1]
    labels = list(image_set_92.values())
    for subject in range(15):
        path = os.path.join("./visualise_category_rdms", task, str(image_set))
        if not os.path.exists(path):
            os.makedirs(path)

        plot_rdm(rdms_dict[key1][subject],
                 rdms_dict[key2][subject], subject+1, labels, path, task)
    plot_rdm(np.mean(rdms_dict[key1], axis=0), np.mean(
        rdms_dict[key2], axis=0), "avg", labels, path, task)


def visualise_rdms(task, image_set):
    rdms_dict = io.loadmat(
        "./rearranged_rdms/rearranged_"+task+"_"+str(image_set)+".mat")
    # print(rdms_dict[keys[task][0]].shape)
    key1, key2 = keys[task][0], keys[task][1]
    for subject in range(15):
        path = os.path.join("./visualise_rdms", task, str(image_set))
        if not os.path.exists(path):
            os.makedirs(path)
        labels, _ = get_labels_and_mapping(image_set)
        plot_rdm(rdms_dict[key1][subject],
                 rdms_dict[key2][subject], subject+1, labels, path, task)
    plot_rdm(np.mean(rdms_dict[key1], axis=0), np.mean(
        rdms_dict[key2], axis=0), "avg", labels, path, task)


def calculate_category_index(task, image_set, file_path):
    rdms_dict = io.loadmat(
        "./categorised_rdms/categorised_"+task+"_"+str(image_set)+".mat")
    # print(rdms_dict[keys[task][0]].shape)
    category_ind = {
        keys[task][0]: [],
        keys[task][1]: []
    }
    for key in keys[task]:
        # average wiwthin and between category distances across all subjects
        rdm = np.mean(rdms_dict[key], axis=0)
        for cat_num1 in range(number_of_catg):
            val = 0
            for cat_num2 in range(number_of_catg):
                # Sum of Difference between the btween-category and within category TODO
                val += rdm[cat_num1, cat_num2] - rdm[cat_num1, cat_num1]
            category_ind[key] = category_ind[key] + [val]

    with open(file_path, "a") as new_file:
        new_file.write("Task: "+task.upper() +
                       " :: Image Set: " + str(image_set)+"\n")
        for key in keys[task]:

            new_file.write("*"*15+key + "*"*15+"\n")
            new_file.write(
                tabulate(zip(image_set_92.values(), category_ind[key])))
            new_file.write("\n\n")


def main(config):
    tasks = ["fmri", "meg"]
    image_sets = [92]

    for task in tasks:
        for image_set in image_sets:
            print("task:", task, "image_set:", image_set)
            if config.rearrange:
                rearrange(task, image_set)
                return
            if config.visualise_rearrange:
                visualise_rdms(task, image_set)
                return
            if config.category_rdms:
                create_category_rdms(task, image_set)
                return
            if config.visualise_categories:
                visualise_category_rdms(task, image_set)
                return
            if config.calculate_ci:
                calculate_category_index(
                    task, image_set, config.category_index_path)
                return


if __name__ == "__main__":
    config = Config().init()
    main(config)
