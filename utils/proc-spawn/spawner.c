#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <stdint.h>
#include <errno.h>
#include <ctype.h>
#include <string.h>
#include <assert.h>

#define OUT_MAX                 1024 
#define LINE_MAX                256
#define CMD_MAX                 256
#define TIMEOUT_AFTER_30_SEC    (30*1000)

#define handle_error_en(en, msg) \
    do { errno = en; perror(msg); exit(EXIT_FAILURE); } while (0)

#define handle_error(msg) \
    do { perror(msg); exit(EXIT_FAILURE); } while (0)

// TODO array for 1:1 lock to struct thread_info
pthread_mutex_t     g_lock_tnum = PTHREAD_MUTEX_INITIALIZER;

int g_tnum;

struct thread_info {
    pthread_t       tid;
    int             tnum;
    char            *cmd;
    uint32_t        timeout;
    FILE            *fp;
    char            *out;
    pthread_mutex_t out_lock;
};

static void * thread_start(void *arg) {
    struct thread_info *tinfo = arg;
    char *cmd;
    char *outp;
    char *end;
    char line[LINE_MAX];
    int s;

    cmd = strdup(tinfo->cmd);
    assert(cmd);

    printf("tnum=%d,cmd=%s\n", tinfo->tnum, tinfo->cmd);

    tinfo->fp = popen(cmd, "r");
    assert(tinfo->fp);

    outp = tinfo->out;
    end = outp + OUT_MAX;
    while (fgets(line , LINE_MAX, tinfo->fp) != NULL) {
        pthread_mutex_lock(&tinfo->out_lock);
        outp += snprintf(outp, end - outp, "%s", line);
        pthread_mutex_unlock(&tinfo->out_lock);
    }

    s = pclose(tinfo->fp);
    if (s != 0) 
        handle_error_en(s, "pclose");

    return;
}

void spawn_thread(struct thread_info tinfo) {
    int s;
    pthread_attr_t attr;

    s = pthread_attr_init(&attr);
    if (s != 0)
        handle_error_en(s, "pthread_attr_init");

    // optionally dictate stack size for threads
    
    s = pthread_create(&tinfo.tid, &attr, &thread_start, &tinfo);
    if (s != 0) 
        handle_error_en(s, "pthread_create"); 
}

void check_thread(struct thread_info tinfo) {
    pthread_mutex_lock(&tinfo.out_lock);
    printf("%s: %s\n", __FUNCTION__, tinfo.out);
    pthread_mutex_unlock(&tinfo.out_lock);
}

// Testing
int main() {

    // cmd setup
    char *cmd = calloc(CMD_MAX,sizeof(char));
    assert(cmd);
    cmd = strncpy(cmd, "ls -1", CMD_MAX);
    int tnum;

    // thread setup
    int num_threads;
    struct thread_info *tinfo;

    num_threads = 3;
    tinfo = calloc(num_threads, sizeof(struct thread_info));
    assert(tinfo);

    // thread_info setup
    pthread_mutex_lock(&g_lock_tnum);
    tinfo[g_tnum].tnum = g_tnum++;
    tnum = g_tnum;
    pthread_mutex_unlock(&g_lock_tnum);
    tinfo[tnum].cmd = strdup(cmd);
    assert(tinfo[tnum].cmd);
    tinfo[tnum].timeout = TIMEOUT_AFTER_30_SEC;
    pthread_mutex_init(&tinfo[tnum].out_lock, NULL);
    pthread_mutex_lock(&tinfo[tnum].out_lock);
    tinfo[tnum].out = calloc(OUT_MAX,sizeof(char));
    pthread_mutex_unlock(&tinfo[tnum].out_lock);

    // finally spawn
    spawn_thread(tinfo[tnum]);
    sleep(3);

    // check results
    check_thread(tinfo[tnum]);
}
