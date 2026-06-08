# Mai 2022
# qsort très court

import random
def q_sort(Liste) :
        if len(Liste) > 1 :
                return q_sort([x for x in Liste[1:] if x <= Liste[0]]) \
                + [Liste[0]] + q_sort([x for x in Liste[1:]  if x > Liste[0]])
        return Liste

if __name__ == "__main__" :
    lst=[random.randint(10,100) for _ in range(10)]
    print("Avant : ", lst)
    print("Après : ", q_sort(lst))
