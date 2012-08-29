//g++ -O3 -Wall -o sssh sssh.cpp
#include <cstdlib>
#include <cstdio>
#include <iostream>

using namespace std;
class CommandExec {
public:
    int executor(char *host) {
        // declaration of return value
        int retval;

        // declaration of record
        char record[1024];

        // prints the shell command into record
        sprintf(record,"screen -t %s ssh -A %s", host, host);

        // this executes what record contains
        retval = system(record);

        return retval;
    }
};

int main(int argc,char *argv[]) {
    // create the object
    CommandExec exec;

    // declaration of return value
    int ret;

    if (argc != 2) {
        printf("Command line argument should be only one\n");
        printf("Usage: %s hostname\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    try {
        ret = exec.executor(argv[1]);
    }
    catch ( int e ) {
        cerr << e << endl;
        exit(EXIT_FAILURE);
    }

    // get the status when command is normally ended
    if (WIFEXITED(ret)) {
        WEXITSTATUS(ret);
    }

    return ret;
}
