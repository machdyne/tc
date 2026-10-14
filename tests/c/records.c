#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct note {
    char text[32];
    struct note *next;
};

/* Put a new note at the front of the list, and return the new front. */
struct note *add(struct note *list, const char *text)
{
    struct note *n = malloc(sizeof *n);
    if (n == NULL)
        return list;
    strncpy(n->text, text, sizeof n->text - 1);
    n->text[sizeof n->text - 1] = '\0';
    n->next = list;
    return n;
}

int main(void)
{
    struct note *list = NULL;
    list = add(list, "buy seeds");
    list = add(list, "fix the pump");

    for (struct note *n = list; n != NULL; n = n->next)
        printf("- %s\n", n->text);

    while (list != NULL) {      /* give the memory back */
        struct note *next = list->next;
        free(list);
        list = next;
    }
    return 0;
}
