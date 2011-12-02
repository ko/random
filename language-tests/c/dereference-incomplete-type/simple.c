typedef struct fourth_two_s  {
    int a;
    int b;
    int c;
    int d;
} fourth_two_t;

typedef struct fourth_one_s  {
    int a;
    int b;
    int c;
    int d;
} fourth_one_t;

#define THIRD_FIELDS         \
    int a;                   \
    int b;                   \
    int c;                   \
    union {                  \
        fourth_one_t one;    \
        fourth_two_t two;    \
    } fourth;                \

typedef struct third_s {
    THIRD_FIELDS
    int z;
} third_t;

typedef struct second_s {
    int a;
    int b;
    struct third_s * third;
    third_t * third_a;
} second_t;

typedef struct first_s {
    int a;
    second_t second; 
} first_t;

int main(void) {
    first_t first = {0};
    third_t third = {0};

    third.a = 3;
    first.second.third = &third;
    first.second.third->fourth.one.a = 5;

    //__asm {INT 3};
    return 0;
}
