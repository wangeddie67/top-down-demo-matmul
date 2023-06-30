
GCC_CMD=gcc -g -Wall
OBJDUMP_CMD=objdump -dS -M attr
PMUTOOL_CMD=sudo ../../tools/pmu-tools/toplev -v --all --core C2 --no-desc -x, 
TASKSET_CMD=taskset -c 2

all: naive o2 bigtlb op vec avx avx512 op2

naive:
	$(GCC_CMD) -o matmul matmul.c
	$(OBJDUMP_CMD) matmul > matmul.diss
	$(PMUTOOL_CMD) -o matmul.csv     $(TASKSET_CMD) ./matmul

o2:
	$(GCC_CMD) -O2 -o matmul_o2 matmul.c
	$(OBJDUMP_CMD) matmul_o2 > matmul_o2.diss
	$(PMUTOOL_CMD) -o matmul_o2.csv  $(TASKSET_CMD) ./matmul_o2

bigtlb:
	$(GCC_CMD) -O2 -o matmul_bigtlb matmul_bigpage.c
	#$(GCC_CMD) -O2 -ftree-vectorize -march=cascadelake -o matmul_op matmul_op.c
	$(OBJDUMP_CMD) matmul_bigtlb > matmul_bigtlb.diss
	$(PMUTOOL_CMD) -o matmul_bigtlb.csv  $(TASKSET_CMD) ./matmul_bigtlb

op:
	$(GCC_CMD) -O2 -o matmul_op matmul_mkn.c
	$(OBJDUMP_CMD) matmul_op > matmul_op.diss
	$(PMUTOOL_CMD) -o matmul_op.csv  $(TASKSET_CMD) ./matmul_op

vec:
	$(GCC_CMD) -O2 -ftree-vectorize -o matmul_vec matmul_mkn.c
	$(OBJDUMP_CMD) matmul_vec > matmul_vec.diss
	$(PMUTOOL_CMD) -o matmul_vec.csv $(TASKSET_CMD) ./matmul_vec

avx:
	$(GCC_CMD) -O2 -ftree-vectorize -mavx2 -o matmul_avx matmul_mkn.c
	$(OBJDUMP_CMD) matmul_avx > matmul_avx.diss
	$(PMUTOOL_CMD) -o matmul_avx.csv $(TASKSET_CMD) ./matmul_avx

avx512:
	$(GCC_CMD) -O2 -ftree-vectorize -mavx512f -o matmul_avx512 matmul_mkn.c
	$(OBJDUMP_CMD) matmul_avx512 > matmul_avx512.diss
	$(PMUTOOL_CMD) -o matmul_avx512.csv $(TASKSET_CMD) ./matmul_avx512

fma:
	$(GCC_CMD) -O2 -ftree-vectorize -mavx512ifma -mfma -o matmul_fma matmul_mkn.c
	$(OBJDUMP_CMD) matmul_fma > matmul_fma.diss
	$(PMUTOOL_CMD) -o matmul_fma.csv $(TASKSET_CMD) ./matmul_fma

op2:
	$(GCC_CMD) -O2 -ftree-vectorize -mavx512f -o matmul_op2 matmul_op2.c
	$(OBJDUMP_CMD) matmul_op2 > matmul_op2.diss
	$(PMUTOOL_CMD) -o matmul_op2.csv $(TASKSET_CMD) ./matmul_op2

clean:
	rm -rf *.csv *.diss
	rm -rf matmul matmul_avx matmul_avx512 matmul_bigtlb matmul_op2 \
        matmul_fma matmul_fma_op2 matmul_mkn matmul_o2 matmul_op matmul_vec

