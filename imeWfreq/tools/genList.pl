#cat host.lst | perl dirmk.pl site.url OUTDIR yyyy mm dd

my $da="$ARGV[2]$ARGV[3]$ARGV[4]";
my $daH="$ARGV[2]-$ARGV[3]-$ARGV[4]";

my @site = ();
open(IN,$ARGV[0]);
while(<IN>)
{
    chomp;
    @_ = split /\s+/,$_;
    push @site,@_[0];
}
close(IN);

my @type = ("rawText","normText","segText");
my %fileH = ();
while(<STDIN>)
{
    chomp;
    foreach $ts(@site)
    {
	my $a;
	foreach $a(@type)
	{
	    if (-e "/$_/textDB/$a/$ts/$da")
	    {
	        print "/$_/textDB/$a/$ts/$da\n";
		my $fn = "$a.$_.lst.$ts";
		if (-e "$ARGV[1]/$daH" )
		{
		    open(OUT,">","$ARGV[1]/$daH/$fn") or die "can not open $ARGV[1]/$daH/$fn to write\n";

                    if (opendir(DIR,"/$_/textDB/$a/$ts/$da"))
		    {
		        my $str;
		        while($str = readdir DIR)
			{
			    if (-f "/$_/textDB/$a/$ts/$da/$str" )
			    {
			        print OUT "/$_/textDB/$a/$ts/$da/$str\n";
			    }
			}
		    }

		    close(OUT);
		}
		else
		{
                   die "No such dir: $ARGV[1]/$da\n";
		}
	    }
	    else
	    {
	    }
	}
    }
}
