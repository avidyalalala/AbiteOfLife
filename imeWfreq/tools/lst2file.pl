use strict;
use Encode qw/encode decode/;
use Getopt::Std;
use utf8;
binmode(STDOUT,':encoding(utf8)');

my $usage;
my %opts;
my($k,$v);

$usage="\
$0 -i lstfile  -o outfile [-h]\
";

%opts=(  #"p"=>6,
);

getopt('hi:o:',\%opts);

die $usage if (defined($opts{h}));
die $usage if !(defined($opts{i}));
die $usage if !(defined($opts{o}));

my @ta = ();
my $ts = undef;
open(IN,$opts{i}) or die "can not open $opts{i}\n";
open(OUT,">:encoding(utf-8)",$opts{o}) or die "can not open $opts{o}\n";
while(<IN>)
{
    chomp;
    open(FILE,$_) or die "can not open $_\n";

#@ta = <FILE>;
#print join("",@ta),"\n";
#next;

    @ta = <FILE>;
    $_ = join("1 ",@ta);
    $ts = decode("utf-8",$_);
    print OUT "1 $ts\n";
    
    close(FILE);
}

close(OUT);    
