import glob
import gzip

# write out when a Chromosome is complete
def write_out(tmp_list):
    txt = ''.join(tmp_list)
    open('ALL.vcf','a').write(txt)

#find all vcfs
vcfs = sorted(glob.glob("*.gz"))

tmp_list = [] # tempororaily store lines
tmp_list_2 = []
chr = ''
save_flag = 0  # save flag determine which tmp_list to save lines,0 - not determined, 1 - tmp_list, 2 - tmp_list_2
for vcf in vcfs: #go over each vcf file
    print vcf
    with gzip.open(vcf, "rb") as f:
        save_flag = 0 # reset save_flag to 0
        for line in f: # go over each line
            if line[0] != '#': # find no # line
                if save_flag == 0: # if not determined which tmp_list to save
                    tmp = line.split()
                    if tmp[0] != chr: # if it is new chr name, try to write out
                        if tmp_list != []:
                            write_out(tmp_list)
                            print 'write',chr
                        tmp_list = [] # write last chr data, empty tmp_list for new chr
                        chr = tmp[0]
                        save_flag = 1 # lines save to tmp_list
                    else: # if the same chr, save to another tmp_list_2
                        save_flag = 2
                        tmp_list_2 = []
                if save_flag == 1: # save lines
                    tmp_list.append(line)
                elif save_flag == 2:
                    tmp_list_2.append(line)
#        print chr,len(tmp_list),len(tmp_list_2)
        if tmp_list_2:
            #after save lines, combine tmp_list_2 to tmp_list
            last_pos = int(tmp_list[-1].split()[1])  # last position of tmp_list
            first_pos = int(tmp_list_2[0].split()[1]) # first position of tmp_list_2
            print chr,last_pos,first_pos,first_pos-last_pos
            if first_pos > last_pos: # if first_pos bigger than last_pos, add tmp_list_2 to tmp_list
                tmp_list += tmp_list_2
                print 'no overlap'
            else: # if first_pos smaller than last_pos, find a middle position to combine
                i = -1 # tmp_list index from last one
                j = 0 # tmp_list_2 index from first one
                while 1:
                    i -= 1 # cut one from tmp_list then check
                    last_pos = int(tmp_list[i].split()[1])
                    if first_pos > last_pos:
                        print last_pos,first_pos
                        tmp_list = tmp_list[:(i+1)] + tmp_list_2[j:]
                        break
                    j += 1 # cut one from tmp_list_2 then check
                    first_pos = int(tmp_list_2[j].split()[1])
                    if first_pos > last_pos:
                        print last_pos,first_pos
                        tmp_list = tmp_list[:(i+1)] + tmp_list_2[j:]
                        break
            tmp_list_2 = []
# after read all files, write out last chr 
print 'write',chr
write_out(tmp_list)

