#include <stdlib.h>
#include <stdio.h>  // printf
#include <string.h> // memset

typedef struct ListElement {
    int data;
    struct ListElement * next;
} ListElement;

ListElement * head = NULL;

int push(int d) {
    ListElement * e = (ListElement *)malloc(sizeof(ListElement));
    memset(e, 0, sizeof(ListElement));
    e->data = d;
    if (!head) {
        head = e;
        e->next = NULL;
    } else {
        e->next = head;
        head = e; 
    }
    return 0;
}

void pop() {
    head = head->next;
    return;
}

void traverse() {
    ListElement * temp = head;
    while (temp) {
        printf("temp->data: %d\n", temp->data);
        temp = temp->next;
    }
    return;
}

int main(void)
{
    ListElement * temp;
    push(5);
    push(6);
    push(7);
    push(3);
    traverse(); 
    pop();
    push(8);
    printf("\n");
    traverse(); 
    return 0;
}
