#include <string.h>
#include <stdlib.h>
#include <stdio.h>

typedef struct Element {
    int data;
    struct Element * next;
} Element;


int push(Element **head, int data);
int traverse(Element *head);
int traverse_reverse(Element *head);
int find_mth(Element *head, int m);

int push(Element **head, int data) 
{
    if (!head)
        return -1;
    Element * new = (Element *)malloc(sizeof(Element));
    new->data = data;
    new->next = *head;
    *head = new;
    return 0;
}

int traverse(Element *head)
{
    if (!head)
        return -1;
    Element * temp = NULL;
    printf("[begin traverse]\n");
    for (temp = head; temp != NULL; temp = temp->next) {
        printf("temp->data: %d\n", temp->data);
    }
    printf("[end traverse]\n");
}

int traverse_reverse(Element *head)
{
    int eax = 0;
    if (head) {
        eax = traverse_reverse(head->next);
        printf("in reverse: %d, eax: %d\n", head->data, eax);
        eax++;
    } else {
    }
    return eax;
}

int find_mth(Element *head, int m)
{
    int eax = 0;
    if (head) {
        eax = find_mth(head->next, m);
        if (eax == m)
            printf("(m=%d) in reverse: %d, eax: %d\n", m, head->data, eax);
        eax++;
    } else {
    }
    return eax;
}
int main(void)
{
    Element * head = NULL;
    push(&head, 1);
    push(&head, 2);
    push(&head, 3);
    push(&head, 4);
    push(&head, 5);
    traverse(head);
    traverse_reverse(head);
    find_mth(head, 3);
    return 0;
}
