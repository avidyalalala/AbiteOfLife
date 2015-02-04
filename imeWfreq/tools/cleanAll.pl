#cat host.lst | perl cleanAll.pl site.url

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
    print "rm -rf /$_/textDB/html\n";
    system("rm -rf /$_/textDB/html");
    foreach $ts(@site)
    {
        print "rm -rf /$_/textDB/rawText/$ts\n";
        system("rm -rf /$_/textDB/rawText/$ts");
        print "rm -rf /$_/textDB/normText/$ts\n";
        system("rm -rf /$_/textDB/normText/$ts");
        print "rm -rf /$_/textDB/segText/$ts\n";
        system("rm -rf /$_/textDB/segText/$ts");
    }
}
