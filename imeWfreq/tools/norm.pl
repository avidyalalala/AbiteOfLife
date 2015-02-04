use strict;
use Encode qw/encode decode/;
use Getopt::Std;
use utf8;
binmode(STDOUT,':encoding(utf8)');

my $usage;
my %opts;
my($k,$v);

$usage="\
$0 -i rawList -k date -m pathRaw  -n pahtNorm [-h]\
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
($disk) = ( $opts{i} =~ m/rawText\.(disk\d+)\.lst\./  );

my $site;
($site) = ( $opts{i} =~ m/rawText\.disk\d+\.lst\.(.+)\.\d+/  );

print "fn=$fn  disk=$disk  site=$site\n";

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

my $dir="/$map{$disk}/textDB/normText/$site/$opts{k}";
print "mkdir -p $dir\n";
system("mkdir -p $dir");

$fn = $dir."/".$fn;
my @lst = ();
open(OUT,">:encoding(utf-8)",$fn) or die "can not open $fn to write\n";
open(IN,$opts{i}) or die "can not open $opts{i}\n";
@lst = <IN>;
chomp @lst;
close(IN);

my $coma = "，";
my $pe = "。";
my $tan = "！";
my $que = "？";
my $mao = "：";
my $fen = "；";
my $dun = "、";

foreach $ts(@lst)
{
    open(IN,$ts) or die "can not open $ts\n";
    while(<IN>)
    {
        chomp;
        my $t = decode("utf-8",$_,Encode::FB_QUIET);
	next if length($t) < 5;
	$t =~ s/nbsp/ /g;
	$t =~ s/\#/ /g;
	$t =~ s/\&/ /g;
	$t =~ s/$coma/ /g;
	$t =~ s/$pe/ /g;
	$t =~ s/$tan/ /g;
	$t =~ s/$que/ /g;
	$t =~ s/$mao/ /g;
	$t =~ s/$fen/ /g;
	$t =~ s/$dun/ /g;
	$t =~ s/[a-z]+/ /g;
	$t =~ s/[A-Z]+/ /g;
	$t =~ s/\d+/ /g;
	@_ = split /\s+/,$t;
        print OUT join("\n",@_),"\n";
    }
    close(IN);

}

close(OUT);
    
