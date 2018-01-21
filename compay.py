#!/usr/bin/python

h = raw_input('Enter Hours:')
r = raw_input('Enter Rate:')

def compay(h,r): 
    h = float(h)
    r = float(r)
    ot = h - 40
    if h <= 40:
        pay = h * r
    else:
        r_pay = 40 * r
        ot_pay = ot * (r + r/2)
        pay = r_pay + ot_pay
    return pay

pay = compay(h,r)
print pay
