#run in linux terminal by java -jar Mars4_5.jar nc filename.asm(take inputs from console)

#system calls by MARS simulator:
#http://courses.missouristate.edu/kenvollmar/mars/help/syscallhelp.html
.data
	next_line: .asciiz "\n"
	inp_statement: .asciiz "Enter No. of integers to be taken as input: "
	inp_int_statement: .asciiz "Enter starting address of inputs(in decimal format): "
	out_int_statement: .asciiz "Enter starting address of outputs (in decimal format): "
	enter_int: .asciiz "Enter the integer: "	
.text
#input: N= how many numbers to sort should be entered from terminal. 
#It is stored in $t1
jal print_inp_statement	
jal input_int 
move $t1,$t4			

#input: X=The Starting address of input numbers (each 32bits) should be entered from
# terminal in decimal format. It is stored in $t2
jal print_inp_int_statement
jal input_int
move $t2,$t4

#input:Y= The Starting address of output numbers(each 32bits) should be entered
# from terminal in decimal. It is stored in $t3
jal print_out_int_statement
jal input_int
move $t3,$t4 

#input: The numbers to be sorted are now entered from terminal.
# They are stored in memory array whose starting address is given by $t2
move $t8,$t2
move $s7,$zero	#i = 0
loop1:  beq $s7,$t1,loop1end
	jal print_enter_int
	jal input_int
	sw $t4,0($t2)
	addi $t2,$t2,4
      	addi $s7,$s7,1
        j loop1      
loop1end: move $t2,$t8       
#############################################################
#Do not change any code above this line
#Occupied registers $t1,$t2,$t3. Don't use them in your sort function.
#############################################################
#function: should be written by students(sorting function)
#The below function adds 10 to the numbers. You have to replace this with
#your code
subi $t5,$t1,1    #the condition of the first loop is that the iterator should be less than n-1(here $t1=n)
move $s7,$zero    #initializing iterator to be 0
move $t8,$t2      #storing input address
loop2: 
beq $s7,$t5,loop2end   # first loop is initiated
sub $t7,$t5,$s7        # the condition for the second loop is that the iterator should be less than n-i-1 where i is the iterator of the outer loop
move $s6,$zero         # initializing iterator of inner loop to be 0
move $t2,$t8           # storing the original input address in $t2 for the next iteration
loop3:
beq $s6,$t7,loop3end   # checking the condition for inner loop
lw $s4,0($t2)          # the condition to be checked is arr[j]>arr[j+1] so loading arr[j] in this step
lw $s5,4($t2)          # loading arr[j+1] in this step
bgt $s4,$s5,swap       # if condition which checks the above mentioned condition
addi $t2,$t2,4         # incrementing j
addi $s6,$s6,1         # incrementing the iterator of the inner loop
j loop3                # jump statement to jump back to the start of inner loop
swap:
move $t6,$s4           # moving arr[j] to a temporary register for swapping if the condition arr[j]>arr[j+1] is satisfied 
move $s4,$s5           # moving arr[j+1] to arr[j]
move $s5,$t6           # moving value of arr[j] which was stored in a temporary register into arr[j+1] and hence swapping is completed
sw $s4,0($t2)          # storing the value of arr[j] in the memory
sw $s5,4($t2)          # storing the value of arr[j+1] in the memory
addi $t2,$t2,4         # incrementing j
addi $s6,$s6,1         # incrementing the iterator of inner loop
j loop3                # jump statement to jump back to the start of inner loop
loop3end:
addi $s7,$s7,1         # incrementing the iterator of the outer loop
j loop2                # jump statement to jump back to the start of outer loop
loop2end:
move $t2,$t8           # moving the original input address into $t2
move $t6,$t3           # storing the original output address
move $s6,$zero         # initializing the iterator of the next loop to be 0 
loop4:                 # this loop copies the result into the output address
beq $s6,$t1,loop4end   # the condition for this loop is that the iterator should be less than n
lw $t5,0($t2)          # storing the first element of input array in a temporary register
sw $t5,0($t3)          # storing that element in the memory at the given output address
addi $t3,$t3,4         # to store into the next element of output array
addi $t2,$t2,4         # to get the next element of input array
addi $s6,$s6,1         # incrementing the iterator
j loop4                # jump statement to jump to the start of this loop
loop4end:
move $t3,$t6           # moving the original output address into $t3
#endfunction
#############################################################
#You need not change any code below this line

#print sorted numbers
move $s7,$zero	#i = 0
loop: beq $s7,$t1,end
      lw $t4,0($t3)
      jal print_int
      jal print_line
      addi $t3,$t3,4
      addi $s7,$s7,1
      j loop 
end:
  li $v0,10
      syscall
#input from command line(takes input and stores it in $t6)
input_int: li $v0,5
	   syscall
	   move $t4,$v0
	   jr $ra
#print integer(prints the value of $t6 )
print_int: li $v0,1	
	   move $a0,$t4
	   syscall
	   jr $ra
#print nextline
print_line:li $v0,4
	   la $a0,next_line
	   syscall
	   jr $ra

#print number of inputs statement
print_inp_statement: li $v0,4
		la $a0,inp_statement
		syscall 
		jr $ra
#print input address statement
print_inp_int_statement: li $v0,4
		la $a0,inp_int_statement
		syscall 
		jr $ra
#print output address statement
print_out_int_statement: li $v0,4
		la $a0,out_int_statement
		syscall 
		jr $ra
#print enter integer statement
print_enter_int: li $v0,4
		la $a0,enter_int
		syscall 
		jr $ra
