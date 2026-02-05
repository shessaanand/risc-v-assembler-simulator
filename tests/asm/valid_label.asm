start:
addi s0,zero,5
loop:
addi s0,s0,-1
beq s0,zero,end
jal zero,loop
end:
beq zero,zero,0

