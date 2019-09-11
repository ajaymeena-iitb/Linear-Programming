from gekko import GEKKO
m = GEKKO()
L = 6

# mean values
E_R1 = 0.12
E_R2 = 0.06

# varinace values
VAR_R1 = 0.01
VAR_R2 = 0.04**2/12

# risk in 10^12 change for different values 

# V = 0.1 # for V = 1*10^11
# V = 0.2 # for V = 2*10^11
 V = 0.4 # for V = 4*10^11

# Defining decesion variable

A = m.Var(value = 2*L/3,lb=0,ub=L)

# Adding constrains to model

m.Equation(A*A*VAR_R1 + (L-A)*(L-A)*VAR_R2 <= V)
m.Equation(3*A <= (2*L)) # additional constrain


# Adding Objective function to model
m.Obj(-(E_R1*A+E_R2*(L-A)))

# Solving model
m.solve(disp = False)

################################################### for printing results ###################################################################################

actual_A = A.value[0]

AC = actual_A
actual_VAR = AC*AC*VAR_R1 + (L-AC)*(L-AC)*VAR_R2


print('fraction of amount invested in asset 1 = ', AC/L)
print('fraction of amount invested in asset 2 = ', 1 - AC/L)

print('Expected Return in M$ = ', (E_R1*AC+E_R2*(L-AC)))
print('Risk in M$ =',(AC*AC*VAR_R1 + (L-AC)*(L-AC)*VAR_R2)*(10**6))

###################################################           END      ############################################################################### 


