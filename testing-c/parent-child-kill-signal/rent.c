#include <stdio.h>
#include <signal.h>
#include <string.h>
#include <unistd.h>

struct sigaction act;

void signal_handler(int signo)
{
    printf ("signal caught: %d\n", signo);
}

void sigaction_handler(int signo, siginfo_t *info, void *p)
{
    printf ("signal from %lu, caught: %d\n", (unsigned long)info->si_pid, signo);
}

int main(void) 
{
    char command[100] = "./child";
    char * cmd = command;
    FILE * fp = NULL;
   
    memset (&act,  0, sizeof(act));

    if (0) {
        signal(SIGINT, signal_handler);
        signal(SIGABRT, signal_handler);
        signal(SIGKILL, signal_handler);
    } else {
        act.sa_sigaction = sigaction_handler;
        act.sa_flags = SA_SIGINFO;
        sigaction(SIGTERM, &act, NULL);
        sigaction(SIGINT, &act, NULL);
        sigaction(SIGABRT, &act, NULL);
        sigaction(SIGKILL, &act, NULL);
    }

    fp = popen(cmd, "r");
    return pclose(fp);
}
