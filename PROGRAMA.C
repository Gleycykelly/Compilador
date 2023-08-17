#include<stdio.h>
typedef char literal[256];
void main(void)
{
	int T0;
	int T1;
	int T2;
	int T3;
	int T4;
	int T5;
	int T6;
	literal	A;
	int	B,	D,	E;
	double	C;
	


	printf("Digite B:");
	scanf('%d', &B);
	printf("Digite A:");
	scanf('%s', A);
	T0 = B>2; 
	if(T0) {
		T1 = B<=4; 
		if(T1) {
			printf("B esta entre 2 e 4");
		}
	}
	T2 = B+1;
	B = T2;
	T3 = B+2;
	B = T3;
	T4 = B+3;
	B = T4;
	D = B;
	C = 5.0;
	T5 = B<5; 
	while(T5) {
		printf(C);
		T6 = B+1;
		B = T6;
	}
	printf("\nB=\n");
	printf(D);
	printf("\n");
	printf(C);
	printf("\n");
	printf(A);
}
