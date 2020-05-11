import glob
import gzip

def write_out(tmp_list):
    txt = ''.join(tmp_list)
    open('head.vcf','a').write(txt)

vcfs = sorted(glob.glob("*.gz"))

tmp_list = []
chr = ''
write_flag = 0
for vcf in vcfs:
    print vcf
    with gzip.open(vcf, "rb") as f:
        for line in f:
            if line[0] != '#':
                if write_flag == 0:
                    tmp = line.split()
                    if tmp[0] != chr:
                        write_flag = 1
                        if tmp_list != []:
                            write_out(tmp_list)
                            print 'write',chr
                        tmp_list = []
                    else:
                        if int(tmp[1]) <= pos:
                            print int(tmp[1])
                        else:
                            write_flag = 1
                if write_flag == 1:
                    tmp_list.append(line)
    write_flag = 0
    tmp = tmp_list[-1].split()
    chr = tmp[0]
    last_pos = int(tmp[1])
    pos = last_pos
    while (last_pos - pos < 1000):
        tmp_list = tmp_list[:-30]
        pos = int(tmp_list[-1].split()[1])
    print chr,pos
print 'write',chr
write_out(tmp_list)

