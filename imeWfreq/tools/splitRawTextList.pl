use strict;
use Encode qw/encode decode/;
use Getopt::Std;
use utf8;
binmode(STDOUT,':encoding(utf8)');

my $usage;
my %opts;
my($k,$v);

$usage="\
$0 -i rawText.host.lst.site -k timeOfNumber [-h]\
";

%opts=(  #"p"=>6,
);

getopt('hi:k:',\%opts);

die $usage if (defined($opts{h}));
die $usage if !(defined($opts{i}));
die $usage if !(defined($opts{k}));

my @ta = ();
my $ts = undef;


#read rawText.lst.site
my @rawList = ();
open(IN,$opts{i}) or die "can not open $opts{i}\n";
@rawList = <IN>;
chomp @rawList;
close(IN);

my $sitename = undef;
#($sitename) = ( $opts{i} =~ m/.+textDB\/rawText\/(.+)/ );



my $time = $opts{k};
my $cnt = 0;
my @fh = ();
    for(my $i=0;$i<$time;$i++)
    {
        open($fh[$cnt],">",$opts{i}.".$cnt") or die "can not open $opts{i}.$cnt\n";
        $cnt++;
    }

$cnt = 0;
foreach $ts(@rawList)
{
   my $index = $cnt%$time;
   my $outstr = "$ts";
# my $outstr = $ts."\t".$opts{j}."/".$sitename;
   print { $fh[$index]} "$outstr\n";
   $cnt++;
}
