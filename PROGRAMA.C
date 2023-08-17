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
	literal	A;
	int	B,	D,	H;
	int	C;
	


	T0 = B+1;
	B = T0;
	T1 = B+2;
	B = T1;
	T2 = B+3;
	B = T2;
	D = B;
	C = 5;
	T3 = B<5; 
	while(T3) {
		T4 = C+2;
		C = T4;
		printf(C);
		T5 = B+1;
		B = T5;
	}
}
