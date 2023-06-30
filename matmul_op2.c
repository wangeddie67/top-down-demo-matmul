
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>

#define M 2048
#define N 2048
#define K 2048
#define SLICE_N 64
#define SLICE_K 64

int main()
{
  float* left  ;
  float* right ;
  float* result;

  left = (float*)mmap(NULL, M*K*sizeof(float), PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS|MAP_HUGETLB, -1, 0);
  right= (float*)mmap(NULL, K*N*sizeof(float), PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS|MAP_HUGETLB, -1, 0);
  result=(float*)mmap(NULL, M*N*sizeof(float), PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS|MAP_HUGETLB, -1, 0);

  int mi = 0;
  int ni = 0, ni_o = 0;
  int ki = 0, ki_o = 0;

  for (ki_o = 0; ki_o < K; ki_o += SLICE_K) {
    for (ni_o = 0; ni_o < N; ni_o += SLICE_N) {
      for (mi = 0; mi < M; mi ++) {
        for (ki = ki_o; ki < SLICE_K + ki_o; ki ++) {
          for (ni = ni_o; ni < SLICE_N + ni_o; ni ++) {
            result[mi * N + ni] = result[mi * N + ni] + left[mi * K + ki] * right[ki * N + ni];
          }
        }
      }
    }
  }

  return result[0];
}
