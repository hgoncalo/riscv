num = '0000000010000'
#5-13 = 8
hold_up = num[abs(4-len(num))-1:abs(1-len(num))]
print(hold_up)

target = '10'
ans = "".join(['0'] * 3) + target
print(ans)