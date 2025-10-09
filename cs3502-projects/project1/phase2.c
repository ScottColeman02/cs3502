#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>
#include <string.h>
#include <errno.h>

typedef struct {
	int account_id;
	double balance;
	int transaction_count;
	pthread_mutex_t lock;
} Account;

Account accounts[5];

//Protected deposit
void safeDeposit(int account_id, double amount) {
	pthread_mutex_lock(&accounts[account_id].lock);
	accounts[account_id].balance += amount;
	accounts[account_id].transaction_count++;
	pthread_mutex_unlock(&accounts[account_id].lock);
}

//Protected withdrawal
void withdrawal(int account_id, double amount) {
	pthread_mutex_lock(&accounts[account_id].lock);
	accounts[account_id].balance -= amount;
	accounts[account_id].transaction_count--;
	pthread_mutex_unlock(&accounts[account_id].lock);
}


//Thread function
void* teller_thread(void* arg) {
	int teller_id = *(int*)arg;

	unsigned int seed = time(NULL) + pthread_self();

	int random_account = rand_r(&seed) % 5;

	printf("Account %d Balance: %f\n", random_account, accounts[random_account].balance);


	double deposit = 67.00;
	printf("Teller %d: Depositing %f\n", teller_id,deposit);
	safeDeposit(random_account, deposit);

	printf("Teller %d: Withdrawing  %f\n", teller_id,5.00);
	withdrawal(random_account, 5.00);

	printf("Account %d Balance: %f\n", random_account, accounts[random_account].balance);
	printf("\n");
	return NULL;
}

int main(){

	//Initialize mutexes before creating threads
	for (int i=0; i<5;i++) {
		pthread_mutex_init(&accounts[i].lock, NULL);
		accounts[i].balance = 100.00;
		accounts[i].transaction_count = 0;
	}


	pthread_t threads[3];
	int thread_ids[3];

	//Create threads
	for (int i=0; i<3; i++) {
		thread_ids[i] = i;
		pthread_create(&threads[i], NULL, teller_thread, &thread_ids[i]);
	}

	//Wait for all threads to complete
	for (int i=0; i<3; i++) {
		pthread_join(threads[i], NULL);
	}

	//Destroy mutex locks
	for (int i=0; i<5; i++) {
		pthread_mutex_destroy(&accounts[i].lock);
	}
	return 0;
}
