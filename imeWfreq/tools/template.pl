use strict;
use Encode qw/encode decode/;
use Getopt::Std;
use utf8;
binmode(STDOUT,':encoding(utf8)');

my $usage;
my %opts;
my($k,$v);

$usage="\
$0 -n freq [-h]\
";

%opts=(  #"p"=>6,
);

getopt('hn:',\%opts);

die $usage if (defined($opts{h}));
die $usage if !(defined($opts{n}));

my @ta = ();
my $ts = undef;
while(<STDIN>)
{
    chomp;
    $ts = decode("utf-8",$_);
    @ta = split /\s+/,$ts;
    print "$ta[0]\n" if $ta[1] >= $opts{n};
}

    
