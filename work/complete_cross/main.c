/*
*  Encryption and decryption example using ARMmbed AES library
*
*	Repository: https://github.com/rlysecky/POM
*/

#include <stdio.h>
#include "/manojwork/work/complete_cross/aes.h"
#include <string.h>
#include <time.h>
#include <stdlib.h>
#include<math.h>

#define LoadCount 1
#define COL 10

void randPermute(unsigned char* arr, int n){
  srand(time(NULL));
  for(int i = n-1; i > 0; i--){
    int j = rand() % (i+1);
    unsigned char tmp = arr[i];
    arr[i] = arr[j];
    arr[j] = tmp;
  }
}


int cmpFunc(const void* a, const void* b){
  return (*(unsigned char*)a - *(unsigned char*)b);
}


void WORKLOAD(unsigned char* inbuf, unsigned char* outbuf){
  for(int i = 0; i < LoadCount ; i++){
    //    randPermute(inbuf, 16);
    //M Sorting only first 4 bytes
    qsort(inbuf, 16, sizeof(unsigned char), cmpFunc);
    //    randPermute(outbuf, 16);
    qsort(inbuf, 16, sizeof(unsigned char), cmpFunc);
  }
}

void matMul(int row, int maxNum) {
  //Create 2 random 2D matrixes
  int a[row][COL], b[COL][row], output[row][row];
  
  //RAndomly seeding each time
  srand(time(0));
  
  for (int i=0; i<row; i++) {
    for(int j=0; j<COL; j++) {
      a[i][j] = rand()%maxNum;
      b[j][i] = rand()%maxNum;
    }
  }
  
  //Matrix multiplication
  for (int i=0; i<row; i++) {
    for (int j=0; j<row; j++) {
      for(int k=0; k<COL; k++){
        output[i][j] += a[i][k] * b[k][j];
      }
    }
  }
}

void WORKLOAD_MATMUL(int loopCount) {
 	for (int i=0; i<loopCount; i++) {
    		matMul(10, 10);
  	}

}

//New workload, kind of like fibonnaci
//creates an array with 10 elements, starting from startNum and then sequentially 
//adding previous number
void fibonnaci(startNum) {
  int fibSeries[3];

  for (int i=0; i<=2; i++) {
    if(i == 0) {
      fibSeries[i] = startNum + 5;
    }
    else if (i==1) {
      fibSeries[i] = fibSeries[i-1] + startNum;
    }
    else {
      fibSeries[i] = fibSeries[i-1] + fibSeries[i-2];
    }
  }

  for (int i=0; i<=2; i++) {
    printf("i=%d, fibSeries= %d\n", i, fibSeries[i]);
  }
}

void WORKLOAD_FIB(void) {
  //Random seeding 
  srand(time(0));
  int startNum = rand()%100;                                                                              
  fibonnaci(startNum);
}
// ######################## //

void printbuf16(unsigned char* buf) {
	for (int i = 0; i < 16; i++)
		printf("%d:%c ", i,buf[i]);
	printf("\n");
}
void printbufhex16(unsigned char* buf) {
	for (int i = 0; i < 16; i++)
		printf("%02x ", buf[i]);
	printf("\n");
}
//unsigned int* target;
#ifdef INECLIPSE
#define \
	POM_ENC(data0,data1, data2, data3, data4, data5, data6, data7, data8, data9, dataa, datab, datac, datad, datae, dataf) \
	({ \
		inbuf[0] = data0; \
		inbuf[1] = data1; \
		inbuf[2] = data2; \
		inbuf[3] = data3; \
		inbuf[4] = data4; \
		inbuf[5] = data5; \
		inbuf[6] = data6; \
		inbuf[7] = data7; \		
		inbuf[8] = data8; \
		inbuf[9] = data9; \
		inbuf[10] = dataa; \
		inbuf[11] = datab; \		
		inbuf[12] = datac; \
		inbuf[13] = datad; \
		inbuf[14] = datae; \
		inbuf[15] = dataf; \
		mbedtls_aes_crypt_ecb(&aes_ctx, MBEDTLS_AES_ENCRYPT, inbuf, outbuf); \
		printf("%d\n", outbuf[0]); \
	})
#else
#define \
	POM_ENC(data0,data1, data2, data3, data4, data5, data6, data7, data8, data9, dataa, datab, datac, datad, datae, dataf) \
	({ \
		inbuf[0] = data0; \
                inbuf[1] = data1; \
		inbuf[2] = data2; \
		inbuf[3] = data3; \
		inbuf[4] = data4; \
		inbuf[5] = data5; \
		inbuf[6] = data6; \
		inbuf[7] = data7; \		
		inbuf[8] = data8; \
		inbuf[9] = data9; \
		inbuf[10] = dataa; \
		inbuf[11] = datab; \		
		inbuf[12] = datac; \
		inbuf[13] = datad; \
		inbuf[14] = datae; \
		inbuf[15] = dataf; \
		WORKLOAD_FIB(); \
		mbedtls_aes_crypt_ecb(&aes_ctx, MBEDTLS_AES_ENCRYPT, inbuf, outbuf); \
		WORKLOAD_FIB(); \
	})
#endif

		//Sort workload
		//WORKLOAD(inbuf, outbuf); \
		//WORKLOAD(inbuf, outbuf); \
		
		//2D matrix multiplication
                //WORKLOAD_MATMUL(1); \
                //WORKLOAD_MATMUL(1); \


#define \
	POM_DEC() \
	({ \
		mbedtls_aes_crypt_ecb(&aes_ctx, MBEDTLS_AES_DECRYPT, outbuf, outbuf); \
	})
		//printf("%d\n", outbuf[0]);
int main(void)
{
	// key buffer (128 bits)
	unsigned char key[16];
	// original data
	unsigned char inbuf[16];
	// encryped data
	unsigned char outbuf[16];
	//	target = (void*)inbuf;
	// declare aes context
	mbedtls_aes_context aes_ctx;

	// fill all 0s to buffers
	memset(key, 0, sizeof(key));
	memset(inbuf, 0, sizeof(inbuf));
	memset(outbuf, 0, sizeof(outbuf));
//
	unsigned char outbuf2[16];
	memset(outbuf2, 0, sizeof(outbuf2));
//	int* i_key = (void*)key;
//	*i_key = 33;

	key[0] = 50;
	// init aes context
	mbedtls_aes_init(&aes_ctx);
	// set key
	//M uses the key for encryption
	mbedtls_aes_setkey_enc(&aes_ctx, key, 128);

	// perform encryption
//	int rtn = mbedtls_aes_crypt_ecb(&aes_ctx, MBEDTLS_AES_ENCRYPT, inbuf, outbuf);
#ifndef INECLIPSE
	m5_checkpoint(0,0);
#endif

	// Debug

	//perform decryption



	POM_ENC(1);
	POM_ENC(2);
	POM_ENC(3);
	POM_ENC(4);
	POM_ENC(5);
	POM_ENC(6);
	POM_ENC(7);
	POM_ENC(8);
	POM_ENC(9);
	POM_ENC(10);
	POM_ENC(11);
	POM_ENC(12);
	POM_ENC(13);
	POM_ENC(14);
	POM_ENC(15);
	POM_ENC(16);
	POM_ENC(17);
	POM_ENC(18);
	POM_ENC(19);
	POM_ENC(20);
	POM_ENC(21);
	POM_ENC(22);
	POM_ENC(23);
	POM_ENC(24);
	POM_ENC(25);
	POM_ENC(26);
	POM_ENC(27);
	POM_ENC(28);
	POM_ENC(29);
	POM_ENC(30);
	POM_ENC(31);
	POM_ENC(32);
	POM_ENC(33);
	POM_ENC(34);
	POM_ENC(35);
	POM_ENC(36);
	POM_ENC(37);
	POM_ENC(38);
	POM_ENC(39);
	POM_ENC(40);
	POM_ENC(41);
	POM_ENC(42);
	POM_ENC(43);
	POM_ENC(44);
	POM_ENC(45);
	POM_ENC(46);
	POM_ENC(47);
	POM_ENC(48);
	POM_ENC(49);
	POM_ENC(50);
	POM_ENC(51);
	POM_ENC(52);
	POM_ENC(53);
	POM_ENC(54);
	POM_ENC(55);
	POM_ENC(56);
	POM_ENC(57);
	POM_ENC(58);
	POM_ENC(59);
	POM_ENC(60);
	POM_ENC(61);
	POM_ENC(62);
	POM_ENC(63);
	POM_ENC(64);
	POM_ENC(65);
	POM_ENC(66);
	POM_ENC(67);
	POM_ENC(68);
	POM_ENC(69);
	POM_ENC(70);
	POM_ENC(71);
	POM_ENC(72);
	POM_ENC(73);
	POM_ENC(74);
	POM_ENC(75);
	POM_ENC(76);
	POM_ENC(77);
	POM_ENC(78);
	POM_ENC(79);
	POM_ENC(80);
	POM_ENC(81);
	POM_ENC(82);
	POM_ENC(83);
	POM_ENC(84);
	POM_ENC(85);
	POM_ENC(86);
	POM_ENC(87);
	POM_ENC(88);
	POM_ENC(89);
	POM_ENC(90);
	POM_ENC(91);
	POM_ENC(92);
	POM_ENC(93);
	POM_ENC(94);
	POM_ENC(95);
	POM_ENC(96);
	POM_ENC(97);
	POM_ENC(98);
	POM_ENC(99);
	POM_ENC(100);
	POM_ENC(101);
	POM_ENC(102);
	POM_ENC(103);
	POM_ENC(104);
	POM_ENC(105);
	POM_ENC(106);
	POM_ENC(107);
	POM_ENC(108);
	POM_ENC(109);
	POM_ENC(110);
	POM_ENC(111);
	POM_ENC(112);
	POM_ENC(113);
	POM_ENC(114);
	POM_ENC(115);
	POM_ENC(116);
	POM_ENC(117);
	POM_ENC(118);
	POM_ENC(119);
	POM_ENC(120);
	POM_ENC(121);
	POM_ENC(122);
	POM_ENC(123);
	POM_ENC(124);
	POM_ENC(125);
	POM_ENC(126);
	POM_ENC(127);
	POM_ENC(128);
	POM_ENC(129);
	POM_ENC(130);
	POM_ENC(131);
	POM_ENC(132);
	POM_ENC(133);
	POM_ENC(134);
	POM_ENC(135);
	POM_ENC(136);
	POM_ENC(137);
	POM_ENC(138);
	POM_ENC(139);
	POM_ENC(140);
	POM_ENC(141);
	POM_ENC(142);
	POM_ENC(143);
	POM_ENC(144);
	POM_ENC(145);
	POM_ENC(146);
	POM_ENC(147);
	POM_ENC(148);
	POM_ENC(149);
	POM_ENC(150);
	POM_ENC(151);
	POM_ENC(152);
	POM_ENC(153);
	POM_ENC(154);
	POM_ENC(155);
	POM_ENC(156);
	POM_ENC(157);
	POM_ENC(158);
	POM_ENC(159);
	POM_ENC(160);
	POM_ENC(161);
	POM_ENC(162);
	POM_ENC(163);
	POM_ENC(164);
	POM_ENC(165);
	POM_ENC(166);
	POM_ENC(167);
	POM_ENC(168);
	POM_ENC(169);
	POM_ENC(170);
	POM_ENC(171);
	POM_ENC(172);
	POM_ENC(173);
	POM_ENC(174);
	POM_ENC(175);
	POM_ENC(176);
	POM_ENC(177);
	POM_ENC(178);
	POM_ENC(179);
	POM_ENC(180);
	POM_ENC(181);
	POM_ENC(182);
	POM_ENC(183);
	POM_ENC(184);
	POM_ENC(185);
	POM_ENC(186);
	POM_ENC(187);
	POM_ENC(188);
	POM_ENC(189);
	POM_ENC(190);
	POM_ENC(191);
	POM_ENC(192);
	POM_ENC(193);
	POM_ENC(194);
	POM_ENC(195);
	POM_ENC(196);
	POM_ENC(197);
	POM_ENC(198);
	POM_ENC(199);
	POM_ENC(200);


#ifndef INECLIPSE
	//	m5_exit(0);
#endif

	return 0;
}
