use strict;
use Encode qw/encode decode/;
use Getopt::Std;
use utf8;
binmode(STDOUT,':encoding(utf8)');

my $usage;
my %opts;
my($k,$v);

$usage="\
$0 -i normList -k date -m pathNorm  -n pathSeg [-h]\
";

%opts=(  #"p"=>6,
);

getopt('hi:k:m:n:',\%opts);

die $usage if (defined($opts{h}));
die $usage if !(defined($opts{i}));
die $usage if !(defined($opts{k}));
die $usage if !(defined($opts{m}));
die $usage if !(defined($opts{n}));

my @ta = ();
my $ts = undef;

my $fn = $opts{i};
($fn) = ( $opts{i}  =~ m/(rawText\.disk\d+\.lst\..*)/);
my $disk;
($disk) = ( $opts{i} =~ m/\/(disk\d+)\/textDB\// );

my $site;
($site) = ( $opts{i} =~ m/rawText\.disk\d+\.lst\.(.+)\.\d+/  );

#print "fn=$fn  disk=$disk  site=$site\n";

my %map= ();
open(A,$opts{m}) or die "can not open $opts{m}\n";
open(B,$opts{n}) or die "can not open $opts{n}\n";
while(<A>)
{ 
    chomp;
    ($k) = ($_ =~ m/\/(disk\d+)\// );

    $ts = <B>;
    chomp $ts;
    ($v) = ($ts =~ m/\/(disk\d+)\// );

    $map{$k} = $v;
}
close(A);
close(B);

my $dir="/$map{$disk}/textDB/segText/$site/$opts{k}";
#print "mkdir -p $dir\n";
system("mkdir -p $dir");

#$fn = $dir."/".$fn;
$fn = $dir;
print "$fn\n";
