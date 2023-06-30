import csv
import tabulate

test_list = ["matmul", "matmul_o2", "matmul_bigtlb", "matmul_op", "matmul_vec", "matmul_avx", "matmul_avx512", "matmul_op2"]
metric_list = ["CORE_CLKS", "IPC", "CPI", "ILP", "Instructions", 
    "Retiring", "Frontend_Bound", "Bad_Speculation", "Backend_Bound",
    "Frontend_Bound.Fetch_Latency", "Frontend_Bound.Fetch_Bandwidth",
    "Backend_Bound.Memory_Bound", "Backend_Bound.Core_Bound",
    'Backend_Bound.Memory_Bound.L1_Bound', 'Backend_Bound.Memory_Bound.L2_Bound', 'Backend_Bound.Memory_Bound.L3_Bound', "Backend_Bound.Memory_Bound.DRAM_Bound",
    'Backend_Bound.Core_Bound.Ports_Utilization', 'Backend_Bound.Core_Bound.Ports_Utilization.Ports_Utilized_0', 'Backend_Bound.Core_Bound.Ports_Utilization.Ports_Utilized_1', 'Backend_Bound.Core_Bound.Ports_Utilization.Ports_Utilized_2', 'Backend_Bound.Core_Bound.Ports_Utilization.Ports_Utilized_3m']
    
        
core_list = ["S0-C2", "S0-C2-T0"]

num_test = len(test_list)
num_metric = len(metric_list)

table_header = [""] + test_list
table_body = [ [metric_list[j]] + ["" for i in range(num_test)] for j in range(num_metric) ]

for case_idx, case in enumerate(test_list):
    with open(case + '.csv') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            if row[0] in core_list and row[1] in metric_list:
                metric_idx = metric_list.index(row[1])
                table_body[metric_idx][case_idx + 1 ] = row[2]
                
print(tabulate.tabulate(table_body, table_header))


