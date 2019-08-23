correct = 'correct'
phonetic_correct = 'phonetic_correct'
typo = 'typo'
phonetic_typo = 'phonetic_typo'
phonetic_distance = 'phonetic_distance'

print(f'No Spacing:')
print(f'{correct}|{phonetic_correct}|{typo}|{phonetic_typo}|{phonetic_distance}|\n')
# No Spacing:
# correct|phonetic_correct|typo|phonetic_typo|phonetic_distance|

print(f'Right Aligned:')
print(f'{correct:>10}|{phonetic_correct:>20}|{typo:>10}|{phonetic_typo:>20}|{phonetic_distance:>20}|\n')
# Right Aligned:
#    correct|    phonetic_correct|      typo|       phonetic_typo|   phonetic_distance|

print(f'Left Aligned:')
print(f'{correct:<10}|{phonetic_correct:<20}|{typo:<10}|{phonetic_typo:<20}|{phonetic_distance:<20}|\n') 
# Left Aligned:
# correct   |phonetic_correct    |typo      |phonetic_typo       |phonetic_distance   |

print(f'Centre Aligned:')
print(f'{correct:^10}|{phonetic_correct:^20}|{typo:^10}|{phonetic_typo:^20}|{phonetic_distance:^20}|') 
# Centre Aligned:
#  correct  |  phonetic_correct  |   typo   |   phonetic_typo    | phonetic_distance  |

print(f'mine')
resstr = (f'{correct:<10}'
          f'{phonetic_correct:<20}'
        )
print(resstr)
