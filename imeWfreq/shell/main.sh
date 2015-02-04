rootdir=/disk4/nemo/imeWfreq    
da=20141223 #for testing
daH=2014-12-23
echo da=$da daH=$daH testing
log=$rootdir/log/log.download.$daH.test

#echo step 1: start Parsing  `date "+%F %T"`
#for i in $(cat $rootdir/config/site.url | perl $rootdir/tools/listoutsite.pl); do
#   if [ -e $rootdir/shell/parser.$i.sh ];then
#       echo $rootdir/shell/parser.$i.sh is OK 
#       for j in $(ls $rootdir/lst/0000/html.lst.${i}? ) ; do
#           sh $rootdir/shell/parser.$i.sh ${j} &
#       done
#   else
#       echo $rootdir/shell/parser.$i.sh is missing
#   fi
#done



