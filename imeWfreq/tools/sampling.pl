# perl sampling.pl html.lst 100

my @lst = ();

open(IN,$ARGV[0]) or die "can not open $ARGV[0]\n";
@lst = <IN>;
chomp @lst;
close(IN);


open(OUT,">",$ARGV[0]) or die "can not write to $ARGV[0]\n";
my $ts;
my $cnt=0;
foreach $ts(@lst)
{
    $cnt++;

    print OUT "$ts\n" if $cnt%$ARGV[1] == 0;
}
close(OUT);
