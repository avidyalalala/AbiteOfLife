rootdir=/disk4/nemo/imeWfreq
cat $rootdir/config/host.lst | perl $rootdir/tools/genList.pl $rootdir/config/site.url $rootdir/lst $1 $2 $3
