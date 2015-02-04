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
my %fea=();
foreach $ts(@html)
{
    $cnt++;
    print "$cnt\t$ts\n" if 0 == $cnt%10000;

    open(IN,$ts) or die "can not open $ts\n" or die "can not open $ts\n";
    while(<IN>)
    {
	chomp;
	$k = undef;
	($k) = ( $_ =~ m/PageMeta\.NormalizedUrl=\d+\:(.+)/);
	next if length($k) < 1;
	@_ = split /\//,$k;
	$k = @_[0]."//".@_[1].@_[2];
	if (exists $fea{$k})
	{
	    $fea{$k}++;
	}
	else
	{
	    $fea{$k} = 1;
	}
    }
    close(IN);
}

#print join("\n",keys %fea),"\n";
foreach $ts(keys %fea)
{
    print "$ts\t$fea{$ts}\n";
}

