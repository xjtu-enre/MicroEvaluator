# import argparse
# from function_file import measure_package_metrics, compare_diff, measure_module_metrics
# from detect_algo.detect_root_cause import analyse_data
#
#
# def command(version, ):
#     # parser = argparse.ArgumentParser(description='Measure architecture quality.')
#     # parser.add_argument('-d', '--dep', help='dependency file path')
#     # parser.add_argument('-cmt', '--cmt', help='cmt file path')
#     # parser.add_argument('-mp', '--mpmapping', help='mapping between module and packages')
#     # parser.add_argument('-pp', '--ppmapping', help='mapping between old package name and new package name')
#     # parser.add_argument('-c1', '--com1', help='the folder path of measure result and dep file of the previous version')
#     # parser.add_argument('-c2', '--com2', help='the folder path of measure result and dep file of the later version')
#     # parser.add_argument('-df', '--diff', help='the folder path of diff result')
#     # parser.add_argument('-pro', '--project', help='the folder path of project')
#     #
#     # args = parser.parse_args()
#     # dep_path = args.dep
#     # cmt_path = args.cmt
#     # mpmapping = args.mpmapping
#     # ppmapping = args.ppmapping
#     # com1_path = args.com1
#     # com2_path = args.com2
#     # diff_path = args.diff
#     # project_path = args.project
#     # dep_path = r'D:\codes\test_data\OmniROM_base\base-out(android-11).json'
#     # cmt_path = r'D:\codes\test_data\OmniROM_base\cmt(android-11).csv'
#     # if dep_path and not mpmapping:
#         if measure_package_metrics(dep_path, cmt_path):
#     #         print('Measure finished!!!')
#     #     else:
#     #         print('The file path is not exist!')
#     # if dep_path and mpmapping:
#     #     if measure_module_metrics(dep_path, cmt_path, mpmapping):
#     #         print('Measure finished!!!')
#     #     else:
#     #         print('The file path is not exist!')
#     # # com1_path = r'D:\codes\test_data\OmniROM_base\android-10'
#     # # com2_path = r'D:\codes\test_data\OmniROM_base\android-11'
#     # if com1_path and com2_path:
#     #     if compare_diff(com1_path, com2_path, ppmapping):
#     #         print('Compare finished!!!')
#     #     else:
#     #         print('The file path is not exist!')
#
#     # diff_path = r'C:\Users\20465\Desktop\codes\test_data\microservice\apollo\diff'
#     # project_path = r'C:\Users\20465\Desktop\data\gitcodes\apollo'
#     # if diff_path and project_path:
#     #     if analyse_data(diff_path, project_path):
#     #         print('Analyse finished!!!')
#     #     else:
#     #         print('The file path is not exist!')
#
#
# if __name__ == '__main__':
#     # print(os.getcwd())
#     # print(sys.path)
#     # sys.path.append(os.getcwd())
#     command()