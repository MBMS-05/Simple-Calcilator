import numpy as np
import math
import PySimpleGUI as sg
import pandas as pd

# GUI Code 

sg.theme('DarkTeal1')

# Excel read code

EXCEL_FILE = 'SPHERICAL.xlsx'
df = pd.read_excel(EXCEL_FILE)

# Lay out code

layout = [
    [sg.Push(), sg.Text('SPHERICAL MEXE Calculator', font = ("Agency FB", 20)), sg.Push()],
    
    [sg.Text('Forward Kinematics calculator', font = ("Agency FB", 20))],
    
    [sg.Text('Fill out the following fields:', font = ("Agency FB", 15)),
     sg.Push(), sg.Button('Click this before Solving Forward Kinematics',
     font = ("Agency FB", 14), size=(30,0), button_color=('white', 'black')), sg.Push()],
    
    [sg.Text('a1 = ', font = ("Comic Sans MS",10)),sg.InputText('3', key='a1', size=(20,10)),
    sg.Text('T1 = ', font = ("Comic Sans MS",10)),sg.InputText('90', key='T1', size=(20,10)),
    sg.Push(), sg.Button('Jacobian Matrix (J)', font = ("Agency FB", 17), size=(15,0),button_color=('white', 'black')),
    sg.Button('Det(J)', font = ("Agency FB", 17), size=(15,0), button_color=('white', 'black')),
    sg.Button('Inverse of J', font = ("Agency FB", 17), size=(15,0), button_color=('white', 'black')),
    sg.Button('Transpose of J', font = ("Agency FB", 17), size=(15,0), button_color=('white', 'black')),
    sg.Push()],

    [sg.Text('a2 = ', font = ("Comic Sans MS",10)),sg.InputText('2', key='a2', size=(20,10)),
    sg.Text('T2 = ', font = ("Comic Sans MS",10)),sg.InputText('30', key='T2', size=(20,10))],
    
    [sg.Text('a3 = ', font = ("Comic Sans MS",10)),sg.InputText('2', key='a3', size=(20,10)),sg.Text('d3 = ', font = ("Comic Sans MS",10)),sg.InputText('5', key='d3', size=(20,10)),
    sg.Push(), sg.Button('Inverse Kinematics', font = ("Agency FB", 18), size=(35,0), 
    button_color=('white', 'black')), sg.Push()],
    
    [sg.Button('Solve Forward Kinematics', tooltip = 'Go first to "Click this before Solving Forward Kinematics"!', font = ("Agency FB", 15), button_color=('white', 'black')), sg.Push(),
    sg.Push(), sg.Button('Path and Trajectory Planning', font = ("Agency FB", 18), size=(40,0),
    button_color=('white', 'black')), sg.Push()],
    
    [sg.Frame('Position Vector:',[[
        sg.Text('X = ', font = ("Agency FB",10)),sg.InputText(key='X', size=(10,1)),
        sg.Text('Y = ', font = ("Agency FB",10)),sg.InputText(key='Y', size=(10,1)),
        sg.Text('Z = ', font = ("Agency FB",10)),sg.InputText(key='Z', size=(10,1))]])],
    
    [sg.Push(), sg.Frame('H0_3 Transformation Matrix= ',[[sg.Output(size=(60,12))]]),
    sg.Push(),sg.Image('SPHERICAL.gif'), sg.Push()],

    [sg.Submit(font = ("Agency FB", 15)),sg.Exit(font =  ("Agency FB", 15))]
    
    
    
    ]
         

# Window Code
window = sg.Window('Spherical Manipulator',layout, resizable=True)
        
# Variable Codes for disabling button
disable_J = window['Jacobian Matrix (J)']
disable_DetJ = window['Det(J)']
disable_IV = window['Inverse of J']
disable_TJ = window['Transpose of J']
disable_IK = window['Inverse Kinematics']
disable_PT = window['Path and Trajectory Planning']

while True:
    event,values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    
    if event == 'Click this before Solving Forward Kinematics':
        disable_J.update(disabled=True)
        disable_DetJ.update(disabled=True)
        disable_IV.update(disabled=True)
        disable_TJ.update(disabled=True)
        disable_IK.update(disabled=True)
        disable_PT.update(disabled=True)
        
        
    if event == 'Solve Forward Kinematics':
       # Foward Kinematic Codes 
        a1 = float(values['a1']  )
        a2 = float(values['a2'])
        a3 = float(values['a3'])
         
        T1 = float(values['T1'])
        T2 = float(values['T2'])
        d3 = float(values['d3'])
        
        
        T1 = (T1/180.0)*np.pi #Theta 1 in radians
        T2 = (T2/180.0)*np.pi #Theta 2 in radians
        
        
        
        ## D-H Parameter Table (This is the only part  you only edit for every new mechanical manipulator.)
        # Rows = no. of HTM, Colums = no. of parameters
        #Theta, alpha, r, d
        
        DHPT = [[(0.0/180.0)*np.pi+T1,(90.0/180.0)*np.pi,0,a1],
               [(90.0/180.0)*np.pi+T2,(90.0/180.0)*np.pi,0,0],
               [(0.0/180.0)*np.pi,(0.0/180)*np.pi,0,a2+a3+d3]]
            
            
        # np.trigo function (DHPT[row][column])
        i = 0
        H0_1 = [[np.cos(DHPT[i][0]),-np.sin(DHPT[i][0])*np.cos(DHPT[i][1]),np.sin(DHPT[i][0])*np.sin(DHPT[i][1]),DHPT[i][2]*np.cos(DHPT[i][0])],
                [np.sin(DHPT[i][0]),np.cos(DHPT[i][0])*np.cos(DHPT[i][1]),-np.cos(DHPT[i][0])*np.sin(DHPT[i][1]),DHPT[i][2]*np.sin(DHPT[i][0])],
                [0,np.sin(DHPT[i][1]),np.cos(DHPT[i][1]),DHPT[i][3]],
                [0,0,0,1]]
        
        i = 1
        H1_2 = [[np.cos(DHPT[i][0]),-np.sin(DHPT[i][0])*np.cos(DHPT[i][1]),np.sin(DHPT[i][0])*np.sin(DHPT[i][1]),DHPT[i][2]*np.cos(DHPT[i][0])],
                [np.sin(DHPT[i][0]),np.cos(DHPT[i][0])*np.cos(DHPT[i][1]),-np.cos(DHPT[i][0])*np.sin(DHPT[i][1]),DHPT[i][2]*np.sin(DHPT[i][0])],
                [0,np.sin(DHPT[i][1]),np.cos(DHPT[i][1]),DHPT[i][3]],
                [0,0,0,1]]
        
        i = 2
        H2_3 = [[np.cos(DHPT[i][0]),-np.sin(DHPT[i][0])*np.cos(DHPT[i][1]),np.sin(DHPT[i][0])*np.sin(DHPT[i][1]),DHPT[i][2]*np.cos(DHPT[i][0])],
                [np.sin(DHPT[i][0]),np.cos(DHPT[i][0])*np.cos(DHPT[i][1]),-np.cos(DHPT[i][0])*np.sin(DHPT[i][1]),DHPT[i][2]*np.sin(DHPT[i][0])],
                [0,np.sin(DHPT[i][1]),np.cos(DHPT[i][1]),DHPT[i][3]],
                [0,0,0,1]]
            
        # Dot Product of H0_3 = H0_1*H1_2*H2_3
        H0_1 = np.matrix(H0_1)
        H0_2 = np.dot(H0_1,H1_2)
        H0_3 = np.dot(H0_2,H2_3)
            
        # Transformation Matrix of the Manipulator
        print("H0_3=")
        print(np.matrix(H0_3))
        
        X0_3 = H0_3[0,3]
        print("X = ",X0_3)
        
        Y0_3 = H0_3[1,3]
        print("Y = ",Y0_3)
            
        Z0_3 = H0_3[2,3]
        print("Z = ",Z0_3)

        disable_J.update(disabled=False)
        disable_IK.update(disabled=False)
        disable_PT.update(disabled=False)
        
       
    if event == 'Submit':
        df = df.append(values, ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)
        sg.popup('Data saved!') 
        
    if event == 'Jacobian Matrix (J)':
        
        Z_1 = [[0],[0],[1]] # The [0,0,1] vector
        Z_0 = [[0],[0],[0]] # The [0,0,0] vector
        # Row 1 - 3, Column 2
        
        J1 = [[1 ,0,0],[0,1,0],[0,0,1]]
        
        J1a =[[0,0,0],[0,0,0],[0,0,0]]
        
        J1 = np.dot(J1,Z_1)
        #print('J1 = ')
        #print(np.matrix(J1)) 
        
        J1a_1 = H0_3[0:3,3:]
        J1a_1 = np.matrix(J1a_1)
        #print(J1a_1)
        
        J1a = np.dot(J1a,Z_0)
        #print('J1a = ')
        #print(np.matrix(J1a)) 
        
        J1b = J1a_1 - J1a
        #print("j1b = ")
        #print(J1b)
        
        J01 = [[(J1[1,0]*J1b[2,0])-(J1[2,0]*J1b[1,0])],
              [(J1[2,0]*J1b[0,0])-(J1[0,0]*J1b[2,0])],
              [(J1[0,0]*J1b[1,0])-(J1a[1,0]*J1b[0,0])]]
        
        #print("J01 = ")
        #print(np.matrix(J01))
        
        Z_1 = [[1],[0],[0]] # The [1,0,0  ] vector

        # Row 1 - 3, Column 2

        J2 = [[1 ,0,0],[0,1,0],[0,0,1]]
                
        J2 = np.dot(J2,Z_1)
        #print('J2 = ')
        #print(np.matrix(J2)) 
                
        J2a_1 = H0_3[0:3,3:]
        J2a_1 = np.matrix(J2a_1)
        #print(J2a_1)
                
        J2b_1 = H0_2[0:3,3:]
        J2b_1 = np.matrix(J2b_1)
        #print(J2b_1)
                
        J2a = J2a_1 - J2b_1
        #print("j2a = ")
        #print(J2a)

        J02 = [[(J2[1,0]*J2a[2,0])-(J2[2,0]*J2a[1,0])],
                [(J2[2,0]*J2a[0,0])-(J2[0,0]*J2a[2,0])],
                [(J2[0,0]*J2a[1,0])-(J2[1,0]*J2a[0,0])]]
        #print("J02 = ")
        #print(np.matrix(J02)) 


        
        Z_3 = [[0],[0],[1]] # The [0,0,1] vector

        # Row 1 - 3, Column 3
        
        J03 = H0_3[0:3,0:3]
        
        J03 = np.dot(J03,Z_3)
        #print('J03 = ')
        #print(np.matrix(J03))
        
        J4 = [[0],[0],[1]]
        J4 = np.matrix(J4)
        #print("J4 = ")
        #print(J4)
        
        J5 = [[1 ,0,0],[0,1,0],[0,0,1]]
        J6 = [[1 ,0,0],[0,1,0],[0,0,1]]
        
        
        J5 = np.dot(J5,Z_1)
        J5 = np.matrix(J5)
        #print("J5 = ")
        #print(np.matrix(J5)) 
        
        J6 = np.dot(J6,Z_0)
        #print('J6 = ')
        #print(np.matrix(J6)) 
        
        JM1 = np.concatenate((J01,J02,J03),1)
        #print(JM1)
        JM2 = np.concatenate((J4,J5,J6),1)
        #print(JM2)
        
        J = np.concatenate((JM1,JM2),0)
        #print("J = ")
        #print(J)
        
        sg.popup('J = ', J)

        
        disable_J.update(disabled=True)
        disable_DetJ.update(disabled=False)
        disable_IV.update(disabled=False)
        disable_TJ.update(disabled=False) 

    if event == 'Det(J)':
        # singularity = Det(J)
        # np.linalg.det(M)
        # Let JM1 become the 3x3 position matrix for obtaining the Determinant

        DJ = np.linalg.det(JM1)
        #print("DJ = ",DJ)
        sg.popup('DJ = ',DJ)

        if DJ == 0.0 or DJ == -0:
            disable_IV.update(disabled=True)
            sg.popup('Warning: Jacobian Matrix is Non-Invertible!')

    if event == 'Inverse of J':
        # Inv(J)
        try:
            JM1 = np.concatenate((J01,J02,J03),1)
        except:
            JM1 = -1 #NAN
            sg.popup('Warning!')
            sg.popup('Restart the GUI then go first to "Click this before Solving Forward Kinematics"!')
            break
        IJ = np.linalg.inv(JM1)
        #print("IV = ")
        #print(IV)
        sg.popup('IJ = ',IJ)

    if event == 'Transpose of J':
        # Transpose of Jacobian Matrix
        try:
            JM1 = np.concatenate((J01,J02,J03),1)
        except:
            JM1 = -1 #NAN
            sg.popup('Warning!')
            sg.popup('Restart the GUI then go first to "Click this before Solving Forward Kinematics"!')
            break
        
        TJ = np.transpose(JM1)
        #print("TJ = ")
        #print(TJ)
        sg.popup('TJ = ',TJ)


     
window.close()