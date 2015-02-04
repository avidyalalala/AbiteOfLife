rootdir=/disk4/nemo/imeWfreq
quick=false

if [ "$quick" = "true" ] ; then
   cp -f $rootdir/config/site.url.quick $rootdir/config/site.url 
else
   cp -f $rootdir/config/site.url.all $rootdir/config/site.url 
fi

da=`date -d yesterday +%Y%m%d` 
daH=`date -d yesterday +%Y-%m-%d`
yy=`date -d yesterday +%Y`
mm=`date -d yesterday +%m`
dd=`date -d yesterday +%d`
log=$rootdir/log/log.download.$daH

#da=20150103
#daH=2015-01-03
#yy=2015
#mm=01
#dd=03
#log=$rootdir/log/log.download.$daH.test.`date +%Y%m%d`

#clean all html/raw/nor/seg data
cat $rootdir/config/host.lst | perl $rootdir/tools/cleanAll.pl $rootdir/config/site.url


echo da=$da  daH=$daH > $log
cat $rootdir/config/site.url >> $log

cat $rootdir/config/host.lst | perl $rootdir/tools/dirmk.pl $rootdir/config/site.url

#delete old html files a week ago
#cat $rootdir/config/host.lst | perl $rootdir/tools/cleanOneDay.pl $rootdir/config/site.url `date -d "7 days ago" +%Y-%m-%d` &

echo step 1: start fetching  `date "+%F %T"` >> $log
python $rootdir/tools/fetcher.py $da $rootdir/config/path_html.lst $rootdir/config/site.url > $rootdir/signals/fetcher.log.$da

if [ "$quick" = "true" ] ; then
    rm -rf $rootdir/lst/$daH
else
    rm -rf $rootdir/lst/$daH
fi
rm -rf $rootdir/lst/0000
mkdir -p $rootdir/lst/$daH
cat $rootdir/config/path_html.lst | perl $rootdir/tools/genHtmlFileList.pl -i $da -j $rootdir/config/site.url > $rootdir/lst/$daH/ori.lst 

cp -f $rootdir/lst/$daH/ori.lst $rootdir/lst/$daH/ori.lst.bak
#perl $rootdir/tools/sampling.pl $rootdir/lst/$daH/ori.lst 5

echo step 2: start spliting HTML pages  `date "+%F %T"` >> $log
#if [ "$quick" = "true" ] ; then
#    cp -f $rootdir/lst/$daH/ori.lst $rootdir/lst/$daH/html.lst
#else
#    perl $rootdir/tools/splitHTML.pl -i $rootdir/lst/$daH/ori.lst
#    cat $rootdir/config/path_html.lst | perl $rootdir/tools/genHtmlFileList.pl -i $daH > $rootdir/lst/$daH/html.lst
#fi
cp -f $rootdir/lst/$daH/ori.lst $rootdir/lst/$daH/html.lst

echo step 3: spliting html lst  by sites  `date "+%F %T"` >> $log
if [ "$quick" = "true" ] ; then
    cp -f $rootdir/lst/$daH/html.lst $rootdir/lst/$daH/html.lst.quick
else
    perl $rootdir/tools/splitHtmlLstbySite.pl -i $rootdir/lst/$daH/html.lst -j $rootdir/config/site.url -o $rootdir/lst/$daH
fi

echo step 4: spliting lst for parsers  `date "+%F %T"` >> $log
for i in $(ls $rootdir/lst/$daH/html.lst.*) ;do
    echo $i
    perl $rootdir/tools/genParserInputList.pl -i $i -k $rootdir/config/path_raw.lst -j $da
done

echo step 5: do parsing  `date "+%F %T"` >> $log
for i in $(cat $rootdir/config/site.url | perl $rootdir/tools/listoutsite.pl); do
   if [ -e $rootdir/shell/parser.$i.sh ];then
       echo $rootdir/shell/parser.$i.sh is OK >> $log
       for j in $(ls $rootdir/lst/$daH/html.lst.${i}.* ) ; do
           echo    ${j}   >> $log
           sh $rootdir/shell/parser.$i.sh ${j} $da >> $rootdir/signals/parser.log.$da.${i} &
       done
   else
      echo $rootdir/shell/parser.$i.sh is missing. lauching baseParser  >> $log
       for j in $(ls $rootdir/lst/$daH/html.lst.${i}.* ) ; do
           echo ${j}   >> $log
           sh $rootdir/shell/parser.quick.sh ${j} $da >> $rootdir/signals/parser.log.$da.${i} &
       done
   fi
   wait
done


echo step 6: split raw text list  `date "+%F %T"` >> $log
sh $rootdir/shell/genFileList.sh  $yy $mm $dd
for i in $(cat $rootdir/config/site.url | perl $rootdir/tools/listoutsite.pl); do
      for j in $(ls $rootdir/lst/$daH/rawText.disk*.lst.${i} ) ; do
           perl $rootdir/tools/splitRawTextList.pl -i ${j} -k 4 &
      done
      wait
done

echo step 7: do normalization  `date "+%F %T"` >> $log
for i in $(cat $rootdir/config/site.url | perl $rootdir/tools/listoutsite.pl); do
     for j in $(ls $rootdir/lst/$daH/rawText.disk*.lst.${i}.? ) ; do
        perl $rootdir/tools/norm.pl -i ${j} -k $da -m $rootdir/config/path_raw.lst  -n $rootdir/config/path_norm.lst &
     done
     wait
done

echo step 8: do segmentation   `date "+%F %T"` >> $log
echo do segmentation > $rootdir/signals/segmentation.log
sh $rootdir/shell/genFileList.sh  $yy $mm $dd
cd /disk4/nemo/imeWfreq/tools/AliWS-1.4.0.0/shell
for i in $(cat $rootdir/config/site.url | perl $rootdir/tools/listoutsite.pl); do
     for j in $(ls $rootdir/lst/$daH/normText.disk*.lst.${i} ) ; do
         for k in $(cat $j ) ; do
            src=$k
            tgt=`perl $rootdir/tools/seg.pl -i ${k} -k $da -m $rootdir/config/path_norm.lst  -n $rootdir/config/path_seg.lst` 
            echo do seg src=$src  tgt=$tgt >> $rootdir/signals/segmentation.log
#echo `pwd` >> $log
	    sh ./seg.sh $src $tgt
	 done
     done
done
cd $OLDPWD




echo done  `date "+%F %T"` >> $log
echo >> $log

echo $daH    html      total  `perl $rootdir/tools/filelistSize.pl -i $rootdir/lst/$daH/ori.lst.bak`>> $log
echo $daH    html      total  `perl $rootdir/tools/filelistSize.pl -i $rootdir/lst/$daH/html.lst`>> $log

for i in $(cat $rootdir/config/site.url | perl $rootdir/tools/listoutsite.pl); do
   if [ -e $rootdir/lst/$daH/html.lst.$i ];then
       echo $daH    html      $i    `perl $rootdir/tools/filelistSize.pl -i  $rootdir/lst/$daH/html.lst.$i`  >> $log
   else
       echo
   fi
done

sh $rootdir/shell/genFileList.sh  $yy $mm $dd
echo >> $log
for i in $(cat $rootdir/config/site.url | perl $rootdir/tools/listoutsite.pl); do
    cat `ls $rootdir/lst/$daH/rawText.*.lst.$i` > $rootdir/lst/$daH/rawText.lst.$i
    cat `ls $rootdir/lst/$daH/normText.*.lst.$i` > $rootdir/lst/$daH/normText.lst.$i
    cat `ls $rootdir/lst/$daH/segText.*.lst.$i` > $rootdir/lst/$daH/segText.lst.$i
    echo >> $log 
    echo $daH  rawText   $i    `perl $rootdir/tools/filelistSize.pl -i  $rootdir/lst/$daH/rawText.lst.$i`  >> $log
    echo $daH  normText $i    `perl $rootdir/tools/filelistSize.pl -i  $rootdir/lst/$daH/normText.lst.$i`  >> $log
    echo $daH  segText   $i    `perl $rootdir/tools/filelistSize.pl -i  $rootdir/lst/$daH/segText.lst.$i`  >> $log
done

    echo >> $log
    cat `ls $rootdir/lst/$daH/rawText.lst.*` > $rootdir/lst/$daH/rawText.lst
    cat `ls $rootdir/lst/$daH/normText.lst.*` > $rootdir/lst/$daH/normText.lst
    cat `ls $rootdir/lst/$daH/segText.lst.*` > $rootdir/lst/$daH/segText.lst
    echo $daH  rawText       `perl $rootdir/tools/filelistSize.pl -i  $rootdir/lst/$daH/rawText.lst`  >> $log
    echo $daH  normText     `perl $rootdir/tools/filelistSize.pl -i  $rootdir/lst/$daH/normText.lst`  >> $log
    echo $daH  segText       `perl $rootdir/tools/filelistSize.pl -i  $rootdir/lst/$daH/segText.lst`  >> $log


cp -r $rootdir/lst/$daH $rootdir/lst/0000
echo copy to cps   `date "+%F %T"` >> $log
perl $rootdir/tools/lst2file.pl -i $rootdir/lst/$daH/segText.lst  -o $rootdir/lst/$daH/cps.all
cp -f $rootdir/lst/$daH/cps.all $rootdir/cps/cps.${da}.`date +%Y%m%d%H%M%S`
echo done `date "+%F %T"`  >> $log
