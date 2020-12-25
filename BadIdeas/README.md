# BadIdeas Overview
This is a repo for trying weird things.

## BlackBoxy
A test at writing some code that hides what it does, but is generally very simple.

## Nested 
A more complicated evolution from the first project, I try to use as many terrible or
sketchy ideas I've heard of to accomplish a weird goal. That goal is generally to make
a single program with hidden functionality and the ability to start as a seeming single
or pair of files and pop out into a full software package. 

Programs that do complex things tend to leave behind debris, and usually require many 
other resources like temporary files and packages or libraries be present. But somehow Malware is delivered in a single executable? Interesting. I'm not writing malware, but
this ability to pack so much into so little is very intriguing.

## SpyWare
The way linux lays out memory and resources through the file system is really elegant and interesting to me. I've always found the exploits and attacks that manage to read memory of other processes to be really cool. This is my poor attempt at making some code that tries to explore this problem. 

Running the following, you might be able to peek a glimpse of the private keys being used for a current ssh session if one is establish and your terminal has run a sudo command previously: 
`./finder ssh intrude | grep 'ssh-rsa'`
