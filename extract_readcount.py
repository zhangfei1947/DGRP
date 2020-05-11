import numpy as np
infile = 'ALL.vcf'

out_SNP_pos = open('SNP_positions.txt','w')
out_PosAlleleCount = open('Position_Allele_count.txt','a')
SNP_pos = ''
PosAlleleCount = ''

Num_line = 196
idx = {'A':0, 'C':1, 'G':2, 'T':3}
i = 0
with open(infile) as f:
    for line in f:
        i += 1
        tmp = line.rstrip('\n').split('\t')
        if len(tmp[3]) == 1 and len(tmp[4]) == 1:  ###
            SNP_pos += tmp[0] + '\t' + tmp[1] + '\n' 
            Count = [0]*(Num_line*4)
            R = tmp[3]
            S = tmp[4]
            line = -1
            for each in tmp[9:]:
                line += 1
                if each != './.':
                    tmp2 = each.split(':')
                    R_num,S_num = tmp2[1].split(',')
                    Count[idx[R]*Num_line+line] += int(R_num)
                    Count[idx[S]*Num_line+line] += int(S_num)
            PosAlleleCount += ' '.join(map(str,Count))+'\n'
        if i == 10000:
            out_PosAlleleCount.write(PosAlleleCount)
            PosAlleleCount = ''
            i = 0
            print tmp[0],tmp[1]

out_SNP_pos.write(SNP_pos)
out_SNP_pos.close()
out_PosAlleleCount.write(PosAlleleCount)
out_PosAlleleCount.close()

