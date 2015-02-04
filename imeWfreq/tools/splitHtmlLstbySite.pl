use strict;
use Encode qw/encode decode/;
use Getopt::Std;
use utf8;
binmode(STDOUT,':encoding(utf8)');

my $usage;
my %opts;
my($k,$v);

$usage="\
$0 -i html.lst -j site.url -o dir [-h]\
";

%opts=(  #"p"=>6,
);

getopt('hi:j:o:',\%opts);

die $usage if (defined($opts{h}));
die $usage if !(defined($opts{i}));
die $usage if !(defined($opts{j}));
die $usage if !(defined($opts{o}));

my @ta = ();
my $ts = undef;

my @html = ();
open(IN,$opts{i}) or die "can not open $opts{i}\n";
@html = <IN>;
chomp @html;
close(IN);

my %site = ();
open(IN,$opts{j}) or die "can not open $opts{j}\n";
while(<IN>)
{
    chomp;
    @_ = split /\s+/,$_;
    $site{@_[0]} = @_[1];
}

sub splitOneSite($);

my $onesite = undef;
foreach $onesite(keys %site)
{
    splitOneSite($onesite);
}

sub splitOneSite($)
{
    my $name = undef;
    ($name) = @_;
    print "..spliting $name\n";

    open(OUT,">",$opts{o}."/html.lst.$name") or die "can not open list file for $name\n";

    my $htmlfn;
    my $cnt=0;
    foreach $htmlfn(@html)
    {
	$cnt++;
	print "$cnt\t$htmlfn\n" if 0 == $cnt%1000000;
        #$ts = `head -2 $htmlfn`;
#       open(IN,$htmlfn) or die "can not open $htmlfn\n";
#	$ts=<IN>;
#	$ts=<IN>;
        if ( $htmlfn =~ m/\/$name\//  )
	{
            print OUT "$htmlfn\n";
	}
#	close(IN);
    }

    close(OUT);
}

