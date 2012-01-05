#include <string.h> 
#include <stdio.h>  
#include <stdlib.h> 

typedef struct Element {
    int data;
    struct Element * next;
} Element;

int push(Element **stack, void *data);
int pop(Element **stack, void **data);
int createStack(Element **stack);
int deleteStack(Element **stack);

int createStack(Element **stack)
{
    *stack = NULL;
    return 0;
}

int deleteStack(Element **stack)
{
    Element *e;
    while (*stack) {
        e = (*stack)->next;
        free(*stack);
        *stack = e;
    }
    return 0;
}

int push(Element **stack, void *data) 
{
    Element *e = malloc(sizeof(Element));
    if (!e) {
        printf("failure\n");
        return -1;
    }
    e->data = data;
    e->next = *stack;
    *stack = e;
    return 0;
}

int pop(Element **stack, void **data) 
{
    Element *e;
    e = *stack;
    if (!e) {
        return -1;
    }
    *data = e->data;
    *stack = e->next;
    free(e);
    return 0;
}

int main(void) 
{
    return 0;
}
