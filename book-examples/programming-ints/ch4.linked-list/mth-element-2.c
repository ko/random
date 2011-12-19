typedef struct Element {
    int data;
    struct Element * next;
} Element;

Element * findMToLastElement(Element *head, int m) {
    Element *current, *mBehind;
    int i;

    /* Advance current m elements from beginnings,
     * checking for the end of the list
     */
    current = head;
    for (i = 0; i < m; i++) {
        if (current->next) {
            current = current->next;
        } else {
            /* list is too short. lol. */
            return NULL;
        }
    }

    /* Start mBehind at the head and advance pointers in sync
     */
    mBehind = head;
    while (current->next) {
        current = current->next;
        mBehind = mBehind->next;
    }
    
    return mBehind;
}


int main(void) 
{
    return 0;
}
