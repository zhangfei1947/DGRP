import glob, json, re

path2 = '/mnt/scratch/zhangf37/PROJECT/20190813_DGRP/02.fastp_qc/'
path3 = '/mnt/scratch/zhangf37/PROJECT/20190813_DGRP/03.bwa_mapping/'

jsons = glob.glob(path2+'*.json')
stats = glob.glob(path3+'*.stat')
dic_j_s = {}

for j in jsons:
    name = j.split('/')[-1]
    name = '.'.join(name.split('.')[:-1])
    x = open(j,'r').read()
    y = json.loads(x)
    if name in dic_j_s:
        print dic_j_s[name]
    dic_j_s[name] = []
    dic_j_s[name].append(y['summary']['before_filtering']['total_reads'])
    dic_j_s[name].append(y['summary']['before_filtering']['total_bases'])
    dic_j_s[name].append(y['summary']['before_filtering']['q20_rate'])
    dic_j_s[name].append(y['summary']['before_filtering']['q30_rate'])
    dic_j_s[name].append(y['summary']['after_filtering']['total_reads'])
    dic_j_s[name].append(y['summary']['after_filtering']['total_bases'])
    dic_j_s[name].append(y['summary']['after_filtering']['q20_rate'])
    dic_j_s[name].append(y['summary']['after_filtering']['q30_rate'])

for s in stats:
    name = s.split('/')[-1]
    name = '.'.join(name.split('.')[:-1])
    x = open(s,'r').readlines()
    dic_j_s[name].append(x[5].split()[0])
    dic_j_s[name].append(x[2].split()[0])
    dic_j_s[name].append(x[0].split()[0])
    s = re.search('\((.+?) : N/A\)',x[4]).group(1)
    dic_j_s[name].append(x[4].split()[0]+'('+s+')')
    s = re.search('\((.+?) : N/A\)',x[8]).group(1)
    dic_j_s[name].append(x[8].split()[0]+'('+s+')')
    dic_j_s[name].append(x[10].split()[0])

out_txt = '\t'.join(['SampleName', 'RawReads', 'RawBases', 'RawQ20Rate', 'RawQ30Rate', 'CleanReads', 'CleanBases', 'CleanQ20Rate', 'CleanQ30Rate', 'PairedReads', 'Supplementary', 'TotalReads', 'TotalMapping', 'PairedMapping', 'SingletonsMapping'])+'\n'

for k,v in dic_j_s.items():
    v = map(str,v)
    out_txt += k+'\t'+'\t'.join(v)+'\n'

open('QC_Mapping.stat.xls','w').write(out_txt)
