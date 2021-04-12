#! /usr/bin/env python3

# -*- coding: utf-8 -*-
# Auto Generate G-Code for milling holes for L zero corner bump stop (grbl 1.1 control)
# Programmer: Troy Franks
# Email: outlaws42@tutanota.com
version = '2021-03-22'

# Requires tmod library. This is a collection of my functions, it will be included with this script
# All other imports are standard with python 3.

# User script imports
from tmod import save_file_list

# python built in imports
import sys
import os
from datetime import datetime

# Variable set information
# Cut information
HoleDia = 1.0
toolDia = .250 # Diameter of the tool in inches
rFeed = 15. # Feedrate for radius moves in inches/min
feed = 60. # Feedrate for horizontal moves in inches/min
zFeed = 5. # Feedrate for z moves in inches/min
depth = 1.3 # Depth of cut
thickness = 1.5 # Material Thickness
status = 'Unproven' # Proven or Unproven
outputFile = f"Hole-Feed{feed}-{HoleDia}X{depth}-{status}.gcode"

# Header information description
x_zero = 'CENTER OF HOLE'
y_zero = 'CENTER OF HOLE'
z_zero = 'TOP OF WORK PIECE'
material = f'{thickness}" MDF'
tool = f'{toolDia}" ENDMILL'

def header(x_zero,y_zero,z_zero,material,tool,status):
  dateset = datetime.now().strftime("%Y/%m/%d, %H:%M")
  filename = os.path.basename(sys.argv[0])
  output = (
    f"%\n"
    f"(MILL HOLES)\n"
    f"(WRITEN FOR GRBL CONTROL)\n"
    f"(THIS PROGRAM WAS GENERATED BY {filename})\n"
    f"(DATE: {dateset})\n\n" 
    f"( *** {status.upper()} PROGRAM *** )\n\n"
    f"(MAKE SURE TO SET G28 WITH G28.1 RETRACTED TO TOP POSITION )\n\n"
    f"( SETUP INFORMATION )\n"
    f"( ZERO SET INFORMATION )\n"
    f"(X0 = {x_zero})\n"
    f"(Y0 = {y_zero})\n"
    f"(Z0 = {z_zero})\n\n"
    f"(MATERIAL TYPE= {material})\n"
    f"(TOOL= {tool})\n\n"
    )
  return output

def initialization():
  output = (
    f"G20 (SET CODE TO INCH)\n"
    f"G17 (XY PLANE SELECTION)\n"
    f"G28 G91 Z0 (SEND TO RETURN POS.)\n"
    f"G90 (ABSOLUTE POSITON)\n"
    f"G54 (WORK CORD)\n"
    f"G94 (INCHES PER MINUTE)\n"
    f"M08 (SPINDLE COOLANT, DUST COLLECTION)\n"
    f"M03 S3500\n"
    f"G04 U10.0\n"

  )
  return output

def start():
  output = (
    f"G0 Z1.0\n"
  )
  return output

def operation(holeDia,toolDia,feed,zFeed,rFeed,holeDepth):
  y_move = '%.3f' % round(((holeDia/2)-(toolDia/2)), 3)
  x_move = '%.3f' % round(((holeDia/2)-(toolDia/2)), 3)
  r_move = '%.3f' % round(((holeDia/2)-(toolDia/2)), 3)
  zStep = 0
  zPos = zStep
  depth = holeDepth + .001
  passes = 1
  codePass = []
  while zStep <= depth:
    output = (
      f"\n(PASSES {passes})\n"
      f"G01 G90 X0 Y{y_move} F{feed}\n"
      f"G01 Z-{zPos} F{zFeed}\n"
      f"G03 X-{x_move} Y0 R{r_move} F{rFeed}\n"
      f"G03 X0 Y-{y_move} R{r_move} F{rFeed}\n"
      f"G03 X{x_move} Y0 R{r_move} F{rFeed}\n"
      f"G03 X0 Y{y_move} R{r_move} F{rFeed}\n"
    )
    zStep += .04
    zPos = '%.3f' % round(zStep, 3) # Round to 3 decimal places
    passes += 1
    codePass.append(output)
  codeOutput = ''.join(codePass)
  return codeOutput


def end():
  output = (
    f"G28 G91 Z0\n"
    f"M05\n"
    f"M09 (SPINDLE COOLANT, DUST COLLECTION OFF)\n"
    f"G0 G90 X0 Y0\n"
    f"M2\n"
    f"M30\n"
    f"%"
    )
  return output   

setHeader = header(x_zero,y_zero,z_zero,material,tool,status)
setInitialization = initialization()
setStart = start()
setOperation = operation(HoleDia,toolDia,feed,zFeed,rFeed,depth)
setEnd = end()
programCNC = [setHeader, setInitialization, setStart, setOperation, setEnd]
save_file_list(outputFile,programCNC,'relative')