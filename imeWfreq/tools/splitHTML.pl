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
my @res = ();
foreach $ts(@html)
{
    $cnt++;
    print "$cnt\t$ts\n" if 0 == $cnt%1000;

    open(IN,$ts) or die "can not open $ts\n" or die "can not open $ts\n";
    @_ = <IN>;
    @res = split /\[add\]\nPageMeta\.NormalizedUrl=/,join("",@_);
    close(IN);
   
    my $size = @res;
    next if 1 == $size;

#open(OUT,">",$ts) or die "can not open $ts for write\n";
#print OUT "[add]\nPageMeta.NormalizedUrl=$res[0]";
#close(OUT);

    for(my $i=1;$i<$size;$i++)
    {
        open(OUT,">",$ts."$i") or die "can not open $ts for write\n";
        print OUT "[add]\nPageMeta.NormalizedUrl=$res[$i]";
	close(OUT);
    }
}


