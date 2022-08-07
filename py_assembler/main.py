from .parse import parser_as_type

instructions = parser_as_type("""add $t2,$t0,$t1;
or $t2,$t0,$t1;
subi $t2,$t0,#10;
mult $t2,$t0,$s0;
or $t2,$t0,$s4;
j $sp;
ori $t2,$t0,#40;
nor $t2,$t0,$t5;
xor $t2,$t0,$t4;
beq $s3;
div $t2,$t0,$s2;
and $t2,$t0,$s3;
addi $t2,$t0,#20;""")
print([i.op for i in instructions])