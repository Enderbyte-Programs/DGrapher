//This is a base program for executing more PCMON things

#include <stdio.h>
#include <string.h>
#include <malloc.h>
#include <stdlib.h>

void printhelp() {
    printf("Here is a list of commands: \n");
    printf("dgraph: View disk write graph\nmgraph: View memory graph\ncpugraph: View CPU graph\ntgraph: Graph CPU temperature\nlff [optional directory]: View largest files\npinggraph <ip-or-url>: View a graph of a ping time to an ip or URL\n");
    printf("pmgraph <pid>: view memory graph for process pid\npcpugraph <pid>: View CPU graph for process pid\n");
}

char* compileargs(char* args[]) {
    char* result = (char*)malloc(100);
    strcat(result,args[1]);
    strcat(result," ");
    strcat(result,args[2]);
    return result;
}

int lexec(char* args[]) {
    return system(compileargs(args));
}

int main(int argc, char* argv[]) {
    printf("Welcome to PCmon by Enderbyte Programs v0.8.6 (c) 2022-2023\n");
    if (argc == 1) {
        printhelp();
        return 1;
    } else {
        if (strcmp(argv[1],"dgraph")==0) {
            return system("dgraph");
        } else if (strcmp(argv[1],"mgraph")==0) {
            return system("mgraph");
        } else if (strcmp(argv[1],"cpugraph")==0) {
            return system("cpugraph");
        } else if (strcmp(argv[1],"tgraph")==0) {
            return system("tgraph");
        
        } else if (strcmp(argv[1],"help")==0) {
            printhelp();
            return 0;
        
        } else {
            if (argc == 2) {
                printf("The command you tried to run needs more arguments. For a commands list, run pcmon help\n");
            }else {
                return lexec(argv);
            }
        }
    }
}
