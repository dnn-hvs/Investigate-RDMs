import argparse
import os
import shutil
import numpy as np


class Config(object):
    def __init__(self):
        self.parser = argparse.ArgumentParser()

        self.parser.add_argument('--rearrange', action="store_true",
                                 help="Rearranges the origina Algonauts rdms based on categories"
                                 )

        self.parser.add_argument('--visualise_rearrange', action="store_true",
                                 help="Saves plots of the RDMs in visualise rdms directory"
                                 )

        self.parser.add_argument('--category_rdms', action="store_true",
                                 help="Creates category RDMs. Converts 92x92 to 8x8"
                                 )
        self.parser.add_argument('--visualise_categories', action="store_true",
                                 help="Visualises category RDMs"
                                 )
        self.parser.add_argument('--calculate_ci', action="store_true",
                                 help="Calculates the Category Index"
                                 )

    def parse(self, args=''):
        if args == '':
            opt = self.parser.parse_args()
        else:
            opt = self.parser.parse_args(args)
        if opt.calculate_ci:
            self.category_index_path = "./category_index.txt"
            if os.path.exists(self.category_index_path):
                os.remove(self.category_index_path)

        return opt

    def init(self, args=''):
        opt = self.parse(args)
        return opt
