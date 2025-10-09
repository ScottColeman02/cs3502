#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>
#include <string.h>
#include <errno.h>

//Shared data structure
typedef struct {
	int account_id;
	double balance;
	int transaction_count;
} Account;

//Global accounts array (shared resource)
Account accounts[5];

//Thread function
void* teller_thread(void* arg) {
	int teller_id = *(int*)arg;  //Cast void* to int* to dereference

	unsigned int seed = time(NULL) + pthread_self();

	int random_account = rand_r(&seed) % 5;

	printf("Account %d Balance: %f\n",random_account,accounts[random_account].balance);
	//Perform mutliple transactions
	for(int i = 0 ; i < 3 ; i++) {
		//Select random account
		//Perform deposit or withdrawal
		// THIS WILL HAVE RACE CONDITIONS!
		double deposit = 67.00;
		accounts[random_account].balance += deposit;
		accounts[random_account].transaction_count++;

		printf("Teller %d: Depositing %f\n", teller_id,deposit);

		double withdraw = 5.00;
		accounts[random_account].balance -= withdraw;
		accounts[random_account].transaction_count++;

		printf("Teller %d: Withdrawing %f\n", teller_id, withdraw);
	}

	printf("Account %d Balance: %f\n",random_account,accounts[random_account].balance);
	printf("\n");
	return NULL;
}

int main(){
	//Creating threads
	pthread_t threads[3];
	int thread_ids[3];

	for (int i=0;i<5;i++){
		accounts[i].balance += 100.00;
		accounts[i].transaction_count = 0;
	}

	for (int i = 0; i < 3; i++) {
		thread_ids[i] = i;
		pthread_create(&threads[i] ,NULL, teller_thread, &thread_ids[i]);
	}

	//Wait for all threads to complete
	for (int i=0;i < 3;i++) {
		pthread_join(threads[i],NULL);
	}

	return 0;
}

