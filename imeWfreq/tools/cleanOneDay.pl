#cat host.lst | perl cleanAll.pl site.url date

my @site = ();
open(IN,$ARGV[0]) or die "can not open ARGV[0]\n";
while(<IN>)
{
    chomp;
    @_ = split /\s+/,$_;
    push @site,@_[0];
}
close(IN);


while(<STDIN>)
{
    chomp;
#    foreach $ts(@site)
	print "rm -rf /$_/textDB/html/$ARGV[1]\n";
        system("rm -rf /$_/textDB/html/$ARGV[1]") or print "error: can not rm\n";
        #system("rm -rf /$_/textDB/rawText/$ts/$ARGV[1]");
        #system("rm -rf /$_/textDB/normText/$ts/$ARGV[1]");
        #system("rm -rf /$_/textDB/segText/$ts/$ARGV[1]");
}
