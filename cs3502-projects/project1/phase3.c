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

Account accounts[2];

void transfer(int from_id, int to_id, double amount,int teller_id);

void* teller0_thread(void* arg) {
	int teller_id = *(int*)arg;  //Cast void* to int* to dereference

	//Create deadlock!!!!!
	transfer(0, 1, 67.00, teller_id);
	return NULL;
}

void* teller1_thread(void* arg) {
        int teller_id = *(int*)arg;  //Cast void* to int* to dereference

        //Create deadlock!!!!!
        transfer(1, 0, 67.00, teller_id);
        return NULL;
}


void transfer(int from_id, int to_id, double amount,int teller_id) {
	printf("Account %d Balance: %f\n",from_id, accounts[from_id].balance);
	printf("Account %d Balance: %f\n",to_id, accounts[to_id].balance);
	printf("\n");

	printf("Teller %d: Attempting transfer from %d, to %d\n",teller_id, from_id, to_id);

	pthread_mutex_lock(&accounts[from_id].lock);
	printf("Teller %d: Locked account %d\n", teller_id, from_id);

	usleep(100);

	printf("Teller %d: Waiting for account %d\n", teller_id, to_id);
	pthread_mutex_lock(&accounts[to_id].lock);

	//Reaching this point means no deadlock
	accounts[from_id].balance -= amount;
	accounts[to_id].balance += amount;
	printf("Funds successfully transfered, printing final balances.\n");

	printf("Account %d Balance: %f\n",from_id, accounts[from_id].balance);
        printf("Account %d Balance: %f\n",to_id, accounts[to_id].balance);
        printf("\n");

	pthread_mutex_unlock(&accounts[to_id].lock);
	pthread_mutex_unlock(&accounts[from_id].lock);
}


int main(){
	//Initialize mutexes before creating threads
        for (int i=0; i<2;i++) {
                pthread_mutex_init(&accounts[i].lock, NULL);
                accounts[i].balance = 500.00;
                accounts[i].transaction_count = 0;
        }

	//Creating threads
        pthread_t threads[2];
        int thread_ids[2];

	thread_ids[0] = 0;
	pthread_create(&threads[0], NULL, teller0_thread, &thread_ids[0]);

	thread_ids[1] = 1;
        pthread_create(&threads[1], NULL, teller1_thread, &thread_ids[1]);

	/*for (int i=0; i<2; i++) {
                thread_ids[i] = i;
                pthread_create(&threads[i], NULL, teller_thread, &thread_ids[i]);
        }*/

	//Wait for all threads to complete
        for (int i=0; i<2; i++) {
                pthread_join(threads[i], NULL);
        }

        //Destroy mutex locks
        for (int i=0; i<2; i++) {
                pthread_mutex_destroy(&accounts[i].lock);
        }


	return 0;
}
