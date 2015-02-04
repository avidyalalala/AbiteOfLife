#cat host.lst | perl dirmk.pl site.url

my @site = ();
open(IN,$ARGV[0]);
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
    foreach $ts(@site)
    {
        system("mkdir -p /$_/textDB/html");
        system("mkdir -p /$_/textDB/rawText/$ts");
        system("mkdir -p /$_/textDB/normText/$ts");
        system("mkdir -p /$_/textDB/segText/$ts");
    }
}
