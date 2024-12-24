/****************************************************************************************************** 
 *
 *  How to compile: cc -o race_demo counter_race_demo.c -lpthread
 ***************************************************************************************************** 
 */
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>  // for usleep (optional)


/* Shared global counter */
long long num = 0;

/* Thread routine: increment num 'count' times */
void* add_repeat(void* arg) {
    long long count = *(long long*)arg;
    for (long long i = 0; i < count; i++) {
        // Optional: add a tiny sleep to provoke context switches
        // usleep(1);
        num++;
    }
    return NULL;
}

int main() {
    /* Print initial value */
    printf("Initial num = %lld\n", num);

    /* We'll increment num a total of 2 * COUNT times */
    long long COUNT = 1000000;  // 1 million
    pthread_t t1, t2;

    /* Create threads */
    pthread_create(&t1, NULL, add_repeat, &COUNT);
    pthread_create(&t2, NULL, add_repeat, &COUNT);

    /* Wait for both threads to finish */
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    /* Print final value */
    printf("Final num = %lld\n", num);

    return 0;
}
