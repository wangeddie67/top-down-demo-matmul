
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>

#define M 2048
#define N 2048
#define K 2048

int main()
{
  float* left  ;
  float* right ;
  float* result;

  left = (float*)mmap(NULL, M*K*sizeof(float), PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS|MAP_HUGETLB, -1, 0);
  right= (float*)mmap(NULL, K*N*sizeof(float), PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS|MAP_HUGETLB, -1, 0);
  result=(float*)mmap(NULL, M*N*sizeof(float), PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS|MAP_HUGETLB, -1, 0);

  int mi = 0;
  int ni = 0;
  int ki = 0;

  for (mi = 0; mi < M; mi ++)
  {
    for (ki = 0; ki < K; ki ++)
    {
      for (ni = 0; ni < N; ni ++)
      {
        result[mi * N + ni] = result[mi * N + ni] + left[mi * K + ki] * right[ki * N + ni];
      }
    }
  }

  return result[0];
}
