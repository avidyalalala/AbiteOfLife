while(<STDIN>)
{
   chomp;
   @_ = split /\s+/,$_;
   print "@_[0]\n";
}
