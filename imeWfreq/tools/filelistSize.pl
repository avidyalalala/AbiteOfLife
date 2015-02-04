use strict;
use Encode qw/encode decode/;
use Getopt::Std;
use utf8;
binmode(STDOUT,':encoding(utf8)');

my $usage;
my %opts;
my($k,$v);

$usage="\
$0 -i html.lst [-h]\
";

%opts=(  #"p"=>6,
);

getopt('hi:',\%opts);

die $usage if (defined($opts{h}));
die $usage if !(defined($opts{i}));

my @ta = ();
my $ts = undef;

my @html = ();
open(IN,$opts{i}) or die "can not open $opts{i}\n";    
@html = <IN>;
chomp @html;
close(IN);

my $cnt=0;
my $total=0;
foreach $ts(@html)
{
    $cnt++;
    #print "$cnt\t$ts\n" if 0 == $cnt%1000;

    if (-e $ts)
    {
        my @args = stat ("$ts");
        my $size = $args[7];
	$total += $size;
    }
}
my $K = 1024;
my $M = 1024 * $K;
my $G = 1024 * $M;
my $T = 1024 * $G;

my $a = 0;

$b = $T;
$a = int($total/$b);
print "${a}T " if $a > 0;
$total -= ($a*$b);

$b = $G;
$a = int($total/$b);
print "${a}G " if $a > 0;
$total -= ($a*$b);

$b = $M;
$a = int($total/$b);
print "${a}M " if $a > 0;
$total -= ($a*$b);

$b = $K;
$a = int($total/$b);
print "${a}K " if $a > 0;
$total -= ($a*$b);

print "\n";
