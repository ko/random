#include <string.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    struct Node *next;
    struct Node *prev;
    struct Node *child;
    int value;
} Node;

/* idea:    for (ptr = head; ptr != NULL; ptr = ptr->next)
 *              if ptr->child != NULL
 *                  for (ptr2 = ptr->child; ptr2 != NULL; ptr2 = ptr2->next)
 *                  ptr2->next = ptr->next
 *                  ptr->next = ptr->child
 */

/* idea:    for (ptr = head; ptr != NULL; ptr = ptr->next) 
 *              if ptr->child != NULL
 *                  tail->next = ptr->child
 *                  for (ptr2 = ptr->child; ptr2 != NULL; ptr2 = ptr2->next)
 *                  tail = ptr2
 *
 *  params: *head   :: need to know where to start, yo
 *          **tail  :: we need to modify the pointer to the tail
 */ 
int flattenMe(Node *head, Node **tail)
{
    Node * ptr = NULL;
    Node *ptr2 = NULL;
    for (ptr = head; ptr != NULL; ptr = ptr->next) {
        if (ptr->child) {
            tail->next = ptr->child;
            for (ptr2 = ptr->child; ptr2->next != NULL; ptr2 = ptr2->next);
            *tail = ptr2;
        }
    }
    return 0;
}

int main(void)
{

    return 0;
}
