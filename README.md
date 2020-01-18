# Investigate-RDMs

Here we will invistigate WTH are RDMs

Inorder to investigate further on RDMs we are considering 8 categories "objects-scenes,fruits-veggies,animal-face,animals,monkeyfaces,human,faces,body-part" which are taken from the fMRI winner track paper. The only change is that hands is changed to body parts.

Below functioanlities are implemented in between_within_category.py

- **Rearrange:** This will rearrange the 92 images based on the categories and create new RDMs which are stored in `./rearranged_rdms` folder. Here, in MEG we are calculating RDM by averaging across timepoint for individual subject.

- **Visualise rearranged RDMS:** This will save plots containg the EVC/Early and IT/Late subplots in a single pplot for every subject and also of the averaged RDM across all subjects.

- **Create Category RDMS:** Using the rearranged RDMs, the within and between category distances is calculated and saved at `./categorised_rdms` folder.

- **Visualise Categorised RDMS:** Saves the plots of within and between category distances for EVC/Early and IT/Late subplots in a single pplot for every subject and also of the averaged RDM across all subjects.

- **Calculate Category Index:**
  - Category RDMs are averaged across all subjects.
  - Using this RDM category index is calculated as sum of differences between the between and with category dissimilarity values
