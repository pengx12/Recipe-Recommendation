#!/usr/bin/env python3
# -*- coding: utf-8 -*-



from . import Nutrition_Extraction
import numpy as np
import ast

def constraint_EER(my_nutrition, age, weight, height, gender, activity_level, standard):
    allow = 0.35
    #print(standard)
    #print(my_nutrition)
    #print('\n')
    if_satisfied = True
    n_nutrition= len(my_nutrition)
    for i in range(5):
#    for i in range(n_nutrition):
        if my_nutrition[i] < standard[i]*(1-allow) or my_nutrition[i] > standard[i]*(1+allow):
            if_satisfied = False
            break

    return if_satisfied


def nutritional_constraints(yum_list, age, weight, height, gender, activity_level,fitness_goal):
    #yum_list=[]
    standard = Nutrition_Extraction(height, weight, age, gender, fitness_goal, activity_level)
    standard = [standard[i]/2.7 for i in range(len(standard))]
    nutrition_list=['ENERC_KJ', 'PROCNT', 'CHOCDF', 'FIBTG', 'FAT', 'CA', 'FE', 'MG', 'P', 'K',\
                    'NA', 'ZN', 'MN', 'SE', 'VITA_RAE', 'TOCPHA', 'VITC', 'RIBF', 'NIA', 'VITB6A', 'BITB12'
                    ,'CHOLN', 'VITK', 'FOL']

    N=len(yum_list)
    satisfied_list=[]
    flag=0
    for i in range(N):
        for j in range(i+1, N):
            if flag==1:
                flag=0
                break
            for k in range(j+1, N):
                    my_nutrition = [x + y + z for x, y, z in zip(yum_list[i][1], yum_list[j][1], yum_list[k][1])]
                    if_satisfy = constraint_EER(my_nutrition, age, weight, height, gender, activity_level, standard)
                    if if_satisfy == True:
                        satisfied_list.append([yum_list[i][0], yum_list[j][0], yum_list[k][0]])
                        flag=1
                        if len(satisfied_list)>=3:
                            return satisfied_list
                        break
    #print(satisfied_list)
    print('Found Matches ', len(satisfied_list))
    return satisfied_list


#nutritional_constraints(yum1, 12, 65, 1.8, 'female', 'Active')