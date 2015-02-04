use strict;
use Encode qw/encode decode/;
use Getopt::Std;
use utf8;
binmode(STDOUT,':encoding(utf8)');

my $usage;
my %opts;
my($k,$v);

$usage="\
$0 -i html.lst.site -k path_raw.lst -j date [-h]\
";

%opts=(  #"p"=>6,
);

getopt('hi:k:j:',\%opts);

die $usage if (defined($opts{h}));
die $usage if !(defined($opts{i}));
die $usage if !(defined($opts{j}));
die $usage if !(defined($opts{k}));

my @ta = ();
my $ts = undef;

my $sitename = undef;
($sitename) = ( $opts{i} =~ m/html\.lst\.(.+)/ );

#read html.lst.site
my @html = ();
open(IN,$opts{i}) or die "can not open $opts{i}\n";
@html = <IN>;
chomp @html;
close(IN);

#read path
my @path = ();
my @fh = ();
my $cnt = 0;

my $time = 4;

open(IN,$opts{k}) or die "can not open $opts{k}\n";
while(<IN>)
{
    chomp;
    for(my $i=0;$i<$time;$i++)
    {
        push @path,$_;
        open($fh[$cnt],">",$opts{i}.".$cnt") or die "can not open $opts{i}.$cnt\n";
        $cnt++;
    }
}
close(IN);

$cnt = 0;
my $size = @path;
foreach $ts(@html)
{
   my $index = $cnt%$size;
   my $outstr = $ts."\t".$path[$index]."/".$sitename."/".$opts{j};
   print { $fh[$index]} "$outstr\n";
   $cnt++;
}
