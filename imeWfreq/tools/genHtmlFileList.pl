#cat path_html.lst | perl genHtmlFileList.pl -i date -o dir 

use strict;
use Encode qw/encode decode/;
use Getopt::Std;
use utf8;
binmode(STDOUT,':encoding(utf8)');

my $usage;
my %opts;
my($k,$v);

$usage="\
$0 -i 20141212 -j site.url [-h]\
";

%opts=(  #"p"=>6,
);

getopt('hi:j:',\%opts);

die $usage if (defined($opts{h}));
die $usage if !(defined($opts{i}));
die $usage if !(defined($opts{j}));

my $f =undef;
my @ta = ();
my $ts = undef;
#my @hr = ("00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23");

my @hr = ();
open(IN,$opts{j}) or die "can not open $opts{j}\n";
while(<IN>)
{
    chomp;
    @ta = split /\s+/,$_;
    push @hr,$ta[0];
}
close(IN);


while(<STDIN>)
{
    chomp;
 my $a;
 foreach $a(@hr)
 {
    my $str = "$_/$opts{i}/$a";
    if (-e $str)
    {
        warn "reading $str...\n";
	if(opendir(DIR,$str))
	{
	    while($ts = readdir DIR)
	    {
                next if $ts eq "index.txt";
                if (-f "$str/$ts")
		{
		    print "$str/$ts\n"
		}
		elsif (-e "$str/$ts")
		{
                    #print "$str/$f\n";
		}
	    }
	}
    }
 }
}

    
