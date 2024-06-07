from GNN_engine import get_recommendations, eval_recommendations_time
import os
import dataset_utilities as du

import config as cf

import csv



def main(type):
    '''
    - type 1 preparing data for training
        input: folder of XES models to train the system
        output: a single file with all classes and their operation
    - type 2: run the recommender on the knowledge base
        input: the train files and the list of test XES traces
        output: recommendations as string
    - type 3: run the recommender with increased training set
        input: MER folder and test models
        output: session-based recommendations
    '''
    if type == "1":
        du.parse_xes_traces(cf.XES_TRAIN_SRC, cf.XES_TRAIN_DST, True)
        du.encoding_training_data_dump(cf.XES_TRAIN_DST+cf.KB_TRAIN)
        return
    elif type == "2":
        du.parse_xes_traces(cf.XES_TEST_SRC, cf.XES_TEST_DST, False)
        preprocessed_train = du.load_preprocessed_data(cf.DUMP_TRAIN)
        train_data = du.load_file(cf.XES_TRAIN_DST + cf.KB_TRAIN)
        for file in os.listdir(cf.XES_TEST_DST):
            get_recommendations(train_preprocessed=preprocessed_train, train_data=train_data, test_context=cf.XES_TEST_DST+file,
                                  n_items = 5)
        return
    elif type == "3":
        du.parse_xes_traces(cf.XES_SESSION_TRAIN_SRC, cf.XES_SESSION_TRAIN_DST, True)
        du.create_path_if_not_exists(cf.XES_SESSION_TRAIN_DST)
        preprocessed_train,train_data = du.encoding_training_data_dump(cf.XES_SESSION_TRAIN_DST + cf.KB_TRAIN)
        for file in os.listdir(cf.XES_TEST_DST):
            get_recommendations(train_preprocessed=preprocessed_train, train_data=train_data, test_context=cf.XES_TEST_DST+file,
                                  n_items = 10)

    elif type == "4":

        du.create_cross_validation_folders(cf.XES_TRAIN_SRC,cf.CROSS_ROOT_STD, 5)
        du.create_path_if_not_exists(cf.RESULTS_CROSS_FOLD)
        results_csv_path = f'{cf.RESULTS_CROSS_FOLD}/results_context_{cf.CONTEXT_RATIO}_cutoff_{cf.CUT_OFF}.csv'

        #Open the CSV file in append mode, so we don't overwrite existing data
        with open(results_csv_path, mode='w', newline='') as file:
            # Create a CSV writer object
            csv_writer = csv.writer(file)

            # Optionally, write headers if the file is newly created or empty
            # Uncomment the next line if you want to write headers
            csv_writer.writerow(['Fold', 'Avg Precision', 'Avg Recall', 'Avg F1'])

            for fold in os.listdir(cf.CROSS_ROOT_STD):

                # Construct paths
                in_fold_train, in_fold_test, out_fold_train, out_fold_test, out_fold_gt = du.building_paths(fold)

                # Preprocess and encode data
                #du.parse_xes_traces(in_fold_test, out_fold_test, False)
                #du.parse_xes_traces(in_fold_train, out_fold_train, True)
                du.combine_files(in_fold_train, out_fold_train)

                preprocessed_train, train_data = du.encoding_training_data_dump(cf.CROSS_ROOT_STD + fold + cf.CROSS_KB_SRC)

                # Initialize metrics accumulators
                total_precision = 0
                total_recall = 0
                total_f1 = 0
                file_count = 0
                total_pr_time = 0.0
                total_rec_time = 0.0

                # Iterate through each test file
                for file in os.listdir(out_fold_test):


                    du.split_file_by_ratio(out_fold_test + file, cf.CONTEXT_RATIO, out_fold_gt + file)

                    pr, rec, f1, pr_time, rec_time = eval_recommendations_time(train_preprocessed=preprocessed_train, train_data=train_data,
                                                       test_context=out_fold_test + file, gt_context=out_fold_gt + file,
                                                       n_items=cf.CUT_OFF)

                    # Accumulate metrics
                    total_precision += pr
                    total_recall += rec
                    total_f1 += f1
                    total_pr_time += pr_time
                    total_rec_time += rec_time
                    file_count += 1

                # Calculate and write average metrics for the fold to the CSV file
                if file_count > 0:
                    avg_precision = total_precision / file_count
                    avg_recall = total_recall / file_count
                    avg_f1 = total_f1 / file_count
                    avg_pr_time = total_pr_time / file_count
                    avg_rec_time = total_rec_time / file_count

                    # Write the fold and its average metrics to the CSV file
                    csv_writer.writerow([fold, avg_precision, avg_recall, avg_f1,avg_pr_time,avg_rec_time])
                else:
                    print(f"Fold {fold}: No files to process.")
    elif type == "5":
         du.parse_xes_traces('hepsy_d00_xes_pm/', 'hepsy_parsed_manual/', False)
         #du.merge_folders(folder1='hepsy_parsed_manual/', folder2='XES-MORGAN-LLM-GPT4/',
                                  #  result_folder='mixed_dataset_08_ratio', ratio=0.8)

    return


def rq3_experiment():

    #du.parse_xes_traces('04 - Dataset-Industrial/XES-PM', '04 - Dataset-Industrial/XES-MORGAN/', False)
    du.aggregate_cluster_files('mixed_dataset_08_ratio/', '04 - Dataset-Industrial/train_mixed/', 'train_mixed_08.txt')



    du.create_path_if_not_exists(cf.RESULTS_CROSS_FOLD)
    results_csv_path = f'{cf.RESULTS_CROSS_FOLD}/results_context_{cf.CONTEXT_RATIO}_cutoff_{cf.CUT_OFF}.csv'

    # Open the CSV file in append mode, so we don't overwrite existing data
    with open(results_csv_path, mode='w', newline='') as file:
        # Create a CSV writer object
        csv_writer = csv.writer(file)

        # Optionally, write headers if the file is newly created or empty
        # Uncomment the next line if you want to write headers
        csv_writer.writerow(['Fold', 'Avg Precision', 'Avg Recall', 'Avg F1', 'Avg pr time', 'Avg rec time'])


        out_fold_test =  '04 - Dataset-Industrial/XES-MORGAN/'
        out_fold_gt = '04 - Dataset-Industrial/GT-PM/'
        # preprocessed_train, train_data = du.encoding_training_data_dump(cf.CROSS_ROOT_STD + fold + cf.CROSS_KB_SRC)
        preprocessed_train, train_data = du.encoding_training_data_dump(
            '04 - Dataset-Industrial/train_mixed/train_mixed_08.txt')


        # Initialize metrics accumulators
        total_precision = 0
        total_recall = 0
        total_f1 = 0
        file_count = 0
        total_pr_time = 0.0
        total_rec_time = 0.0

        # Iterate through each test file
        for file in os.listdir(out_fold_test):
            #du.split_file_by_ratio(out_fold_test + file, cf.CONTEXT_RATIO, out_fold_gt + file)

            pr, rec, f1, pr_time, rec_time = eval_recommendations_time(
                train_preprocessed=preprocessed_train,
                train_data=train_data,
                test_context=out_fold_test + file,
                gt_context=out_fold_gt + file,
                n_items=cf.CUT_OFF)

            # Accumulate metrics
            total_precision += pr
            total_recall += rec
            total_f1 += f1
            total_pr_time += pr_time
            total_rec_time += rec_time
            file_count += 1

        # Calculate and write average metrics for the fold to the CSV file
        if file_count > 0:
            avg_precision = total_precision / file_count
            avg_recall = total_recall / file_count
            avg_f1 = total_f1 / file_count
            avg_pr_time = total_pr_time / file_count
            avg_rec_time = total_rec_time / file_count

            # Write the fold and its average metrics to the CSV file
            csv_writer.writerow([avg_precision, avg_recall, avg_f1, avg_pr_time, avg_rec_time])
        else:
            print(f" No files to process.")



def running_ase_experiment():
    list_co = [3,5,10]
    list_cr = [0.2,0.5,0.8]

    for cr in list_cr:
        for co in list_co:
            du.create_cross_validation_folders(cf.XES_TRAIN_SRC, cf.CROSS_ROOT_STD, 5)
            du.create_path_if_not_exists(cf.RESULTS_CROSS_FOLD)
            results_csv_path = f'{cf.RESULTS_CROSS_FOLD}/results_context_{cr}_cutoff_{co}.csv'

            # Open the CSV file in append mode, so we don't overwrite existing data
            with open(results_csv_path, mode='w', newline='') as file:
                # Create a CSV writer object
                csv_writer = csv.writer(file)

                # Optionally, write headers if the file is newly created or empty
                # Uncomment the next line if you want to write headers
                csv_writer.writerow(['Fold', 'Avg Precision', 'Avg Recall', 'Avg F1', 'Avg pr time', 'Avg rec time'])

                for fold in os.listdir(cf.CROSS_ROOT_STD):

                    # Construct paths
                    in_fold_train, in_fold_test, out_fold_train, out_fold_test, out_fold_gt = du.building_paths(fold)

                    # Preprocess and encode data
                    # du.parse_xes_traces(in_fold_test, out_fold_test, False)
                    # du.parse_xes_traces(in_fold_train, out_fold_train, True)
                    du.combine_files(in_fold_train, out_fold_train)

                    preprocessed_train, train_data = du.encoding_training_data_dump(cf.CROSS_ROOT_STD + fold + cf.CROSS_KB_SRC)
                    #preprocessed_train, train_data = du.encoding_training_data_dump('04 - Dataset-Industrial/train_manual/train.txt')
                    # Initialize metrics accumulators
                    total_precision = 0
                    total_recall = 0
                    total_f1 = 0
                    file_count = 0
                    total_pr_time = 0.0
                    total_rec_time = 0.0

                    # Iterate through each test file
                    for file in os.listdir(out_fold_test):
                        du.split_file_by_ratio(out_fold_test + file, cr, out_fold_gt + file)

                        pr, rec, f1, pr_time, rec_time = eval_recommendations_time(train_preprocessed=preprocessed_train,
                                                                                   train_data=train_data,
                                                                                   test_context=out_fold_test + file,
                                                                                   gt_context=out_fold_gt + file,
                                                                                   n_items=co)

                        # Accumulate metrics
                        total_precision += pr
                        total_recall += rec
                        total_f1 += f1
                        total_pr_time += pr_time
                        total_rec_time += rec_time
                        file_count += 1

                    # Calculate and write average metrics for the fold to the CSV file
                    if file_count > 0:
                        avg_precision = total_precision / file_count
                        avg_recall = total_recall / file_count
                        avg_f1 = total_f1 / file_count
                        avg_pr_time = total_pr_time / file_count
                        avg_rec_time = total_rec_time / file_count

                        # Write the fold and its average metrics to the CSV file
                        csv_writer.writerow([fold, avg_precision, avg_recall, avg_f1, avg_pr_time, avg_rec_time])
                    else:
                        print(f"Fold {fold}: No files to process.")

if __name__ == "__main__":
    #du.parse_xes_traces('d1_random_dataset/', 'd1_random_dataset_parsed/', False)
    running_ase_experiment()
    #du.parse_xes_traces('04 - Dataset-Industrial/XES-PM', '04 - Dataset-Industrial/XES-MORGAN/', False)
    #rq3_experiment()
    # print("Select configuration:\n1.train \n2.recommendation from KB \n3.recommendation from last session \n4.cross fold validation")
    # conf = input("Insert configuration: ")
    # main(conf)

    # list_co = [3,5,10]
    # list_cr = [0.2,0.5,0.8]
    # for cr in list_cr:
    #     for co in list_co:
    #         du.csv_to_latex(f'results_class_five_fold_mixed/results_context_{cr}_cutoff_{co}.csv', f'latex_results/results_class_mixed_context_{cr}_cutoff_{co}.tex')
    # #du.create_cross_validation_folders(cf.XES_TRAIN_SRC, cf.CROSS_ROOT_STD, 5)




