# MPLS

多协议标签交换技术 (Multi Protocol Label Switching, MPLS) 

A frequently mentioned term that causes buzzing in some ears and intrigue in others is MPLS. Multi Protocol

Label Switching is a complex technology whose functioning relies in sharply calibrated mechanisms working

together, resembling the internal mechanics of Swiss watch. In this blog post, I intend to introduce you to

this technology, not reinventing the wheel, but to make it simpler, as building towers with plastic blocks.

 

Before getting into the nitty-gritty of MPLS, let's talk about what it is, from where it came, and why it is so popular.

## MPLS 起源

Everything started in the 90s when Frame Relay, ATM and IP-over-ATM were being employed

by ISPs. The reason was simple: higher throughput and lower latency! Those were early

ages when devices were not exactly overflowing with resources and high bandwidth links like

nowadays, and every inch they could win in favor of improving resource usage was welcome.

ATM’s method of transport was based on virtual circuits that were identified using a pair of simple values

named Virtual Paths (VPs) and Virtual Channels (VCs). Each switch had to check the header of the cell (ATM’s

type of frame with a fixed length) to determine the next hop based on VPI/VCI values. The forwarding decision

process was rather simple: For every port, an ATM switch maintained a table with each row saying: “If a

cell comes in with this particular VPI/VCI combination, rewrite it to the following VPI’/VCI’ combination and

send it out this interface”. It was the task of signalling in ATM to make sure that for a pair of communicating

endpoints, these forwarding tables in adjacent ATM switches would neatly point to each other - the outgoing

VPI/VCI combination of an upstream ATM switch would match the expected incoming VPI/VCI combination

of the adjacent downstream switch along the entire path. Frame Relay used DLCIs (Data Link Connection

Identifiers) instead, which were, as with ATMs VCs, locally significant values for each router. Transport

was possible by matching and rewriting simple values between devices, instead of creating any kind of

mapping or association, or even changing the frame format, simplicity made it very efficient and attractive.

 

IP forwarding on the other hand, required a router to receive the frame, open the IP packet and compare

the destination IP with its routing table, looking for an entry that matched the destination IP in the

longest possible prefix. The first lookup might not have sufficed, though. The routing table entry might

have only contained a next hop IP address without an outgoing interface information, and so the router

would need to perform another lookup, this time for the next hop IP address. This recursion process

could potentially take several iterations until a routing entry would be found that pointed out a specific

interface. Then the router had to consult the ARP (or any other Layer3-to-Layer2 mapping) table to

understand what Layer2 address should be used when forwarding the packet through the immediate

next-hop. Only after all this process, the router was (finally) able to send a packet out. This way of routing

IP packets was also called process switching, and was the basic mode to perform IP routing functions.

 

What was the difference between ATM or Frame Relay, and IP routing? Forwarding simply by doing exact

matching between integers was easier than performing a set of operations for process switching that

were CPU intensive, specifically for IP and its longest prefix matching. In addition to that, IP forwarding

was usually done in software, since constructing a device to perform these actions in hardware instead

was expensive and difficult. For ATM and Frame Relay, their address values were of fixed lengths, able

to be used straight away without any additional computation. This made them considerably easier to

implement in hardware and the overall forwarding process was swift and less painful. Implementation of those

technologies showed in comparison: reduced delay, bottlenecks in the CPU and no long lasting processes.

 

There were attempts to marry IP and ATM, and that's how IP-over-ATM came to the stage. It was ambitious

and promising, but interwaving two protocols that stood in opposed sides of the street (each one had its own

stack) became complex. Sooner than later, scalability constraints and complicated interoperability made it a

challenge, and everything was happening while the time was running away and industry required a solution.

 

Several solutions were conceived by different vendors in the following years,

called multilayer switching, working in a similar way as the predecessor they

were trying to succeed. But, none of them were able to reach that milestone.

In 1997, the IETF decided to start a working group to create an interoperable multilayer

switching standard. It was created making use of a clever idea that looked promising

in the past and was in place in a similar way for previous WAN protocols: labels!

 

MPLS became quickly a must and its adoption was increasing over the time, until now, when it’s the

facto standard for Service Providers. Nowadays, thanks to advances in hardware engineering, there

is really no difference in performance between forwarding based on IP addresses or labels, as it is

all done in hardware, yet the real tangible value lies in what you can build using MPLS and what it is

able to support. Its scalability and interoperability, along with the services and infrastructures you can

run on top of it, like L3VPNs, made it a key tool to drive businesses and networks to a new horizon.

 

And now that we know why MPLS became popular, what about how it works?

MPLS works in a similar way as bookmarks do: It tells routers where exactly in the routing table to

look for an specific prefix. Usually, a router needs to perform a row-by-row lookup in its routing table

for a specific entry so it can forward/route a packet properly but, what if that effort could be prevented

from happening more than needed? What if a bookmark was available? Yes! That’s what MPLS does.

When a router is MPLS-enabled, it will assign a unique number to every prefix in its routing table.

That number will be a key factor to make the communication quicker, as it will identify each prefix

individually. Once the numbers are assigned, they are communicated to its neighbors, like shouting

all over the place. The message would be something like: “The prefix X.X.X.X is in line Y in my routing table, so if you want to use me as a next hop towards X.X.X.X, put a label with the number Y onto that packet so that I can jump onto row Y immediately and forward the packet quicker.”

 

What is the result? All neighbor routers will know that they need only to use that number Y for that prefix,

and packets labeled with Y will be forwarded properly when sent through that router. Forwarding can

happen thanks to the action of passing a integer (called label) between two routers before. In other words:

each router advertises to its neighbors the local label number assigned to each prefix in its routing table.

 

Let’s illustrate that quickly:

![img](mpls.assets/rtaImage.jpeg)

 

As we can observe, in each router the exact same prefix is associated/bound to a different

\- locally significant - label number, and it is advertised to all neighbors indiscriminately.

 

Until now, we have spoken about labels and routers advertising them, without

mentioning how they do it. There are several protocol capable of advertising labels,

but the essential one for this purpose is called LDP (Label Distribution Protocol).

 

LDP allows routers to establish sessions between them, create, advertise and store label bindings, helping

to populate the contents of the LIB (Label Information Base) and LFIB (Label Forwarding Information Base).

 

The rough order of operations is described as follows:

\1. Discovery of routers running LDP (hello messages to 224.0.0.2 address - UDP 646 )

\2. Session establishment (TCP 646)

\3. Label advertisement and reception

\4. Storage of labels in LIB

\5. Build LFIB based on LIB and RIB contents (similar to building FIB from RIB’s information)

\6. Session maintaining (send keepalives, updates, and error messages when needed)

 

Among its functions, building the LFIB and LIB are key pieces to minimize forwarding delay (and to forward in

first place). Let's describe them quickly so we can have a clear picture of them.

 

To define the LIB, we need to remember in which way the labels are advertised, indiscriminately, without

paying attention what prefix and label is being advertised and who is or is not the next hop for it. When a router

binds a prefix with a label number, that association is called local binding for that router. Any binding received

from another router, is called remote binding (because comes from another neighbor, its not local). So, in plain

words, regarding bindings, from any router’s perspective: “what is not mine (local) is remote”.

 

The LIB is a repository whose function is to store destination networks/prefixes and their respective local and

remote bindings created by a router and its neighbors. LIB itself is not the database that is used to perform

forwarding decisions - rather, it is a storage of all known label bindings from the router and its neighbors which

will be later used to pick the proper final candidates and place them into LFIB.

 

When advertisements are done and every router knows and has stored all the labels, forwarding can take

place. What we are missing now is: which label to use in each case? There must be a way for each router to

differentiate them.

 

If we play a little with perspectives, you can place yourself on top of the router and see the labels coming and

going. The label numbers which you receive on the incoming packets are your incoming or ingress labels, and

the label numbers you use to identify the outgoing packets are outgoing or egress labels. This perspective

applies to each and every router individually.

 

Let’s see that in the picture below.

 

![img](mpls.assets/rtaImage.jpeg)

The way forwarding happens involves knowing local and remote bindings and thinking in perspective. Using

LDP, routers advertise their local bindings to their neighbors. All bindings received through LDP will be

stored as remote bindings in the LIB. For example, in the picture above, after R2 advertises the label 568

for 172.31.0.0/24 to R1, R1 will store this binding as a remote binding in its LIB. Later, R1 can use this label

whenever sending packets to 172.31.0.0/24 through R2. Therefore, for a router, its outgoing label is next hop’s

incoming label, and also, your outgoing label is your next hop’s local label.

 

In the same scenario we used before to explain LDP advertisements, some new details are added to see the

big picture. Now we know where the destination network is and the path we will follow: R1 -> R2 -> R3 -> R4.

 

If you place yourself on top of R2, you will see that the local label R2 has advertised for 172.31.0.0/24

earlier (568) is the label R1 uses to send the packets for 172.31.0.0/24 through R2. Since R2 does not have

172.31.0.0/24 directly connected, it has to forward the packets downstream to its own next-hop which is R3.

Because R3 (also called the downstream router) earlier advertised that its own label mapping for 172.31.0.0/24

was 89, R2 (also called the upstream router) will swap the incoming label 568 on top of that packet with the

label 89, and forward the relabeled packet to R3.

 

We can conclude that: downstream routers advertise labels that upstream routers use to send labeled

[packets.In](http://packets.in/) an analogous way as with IP routing, is not efficient to have a huge list of destinations and bindings

and when the time to forward packets comes, jump into it like a kid into a ball pit. To make this task quicker and

efficient, the LFIB is constructed.

 

To build the LFIB it requires the router to collect and combine information from multiple sources/tables. An

entry for a specific network in the LFIB would be created in several steps. First, the router would check its

routing table (RIB) to find the next hop towards that network. Then, it would check in its LIB which one is

the label advertised by that next hop (downstream router) for that prefix. Then, with that information, and its

incoming label for that prefix, the entry is built in the LFIB. The essential parts of the LFIB entry would be:

Incoming label assigned by the router itself, outgoing label learned from the proper next hop, and next hop

information.

 

Now that we have labels, tables, structures and forwarding clear, what are the operations required to move

packets here and there?

 

MPLS works relying in 3 processes when handling packets, as mentioned before, using labels. Those

operations are:

• Label Push or Imposition

• Label Swap

• Label Pop

 

When these operations are performed by a router, it is called LSR

(Label Switching Router). These functions are explained as follows:

 

Label Push: Happens when a packet arrives to a LSR and it pushes or imposes a label on top of

the IP packet, or another label, in case there is a label already on top. One of the situations where

this occurs is when a packet arrives to a MPLS capable network and will be transported through it.

 

Label Swap: This operation is performed if an LSR receives a labeled packet and it will be

forwarded to its next hop as a labeled packet. Since each LSR assigns a locally significant

label number for each destination network or prefix, forwarding them means replacing the

incoming label with the outgoing label advertised by its next hop in the remote binding.

 

Label Pop: Pop operation is implemented by removing the label from the packet,

or in the case the packet possesses more than one label, removing the top

label of the label stack (a label stack is a “pile” of labels on top of a packet).

 

If a PUSH happens when a router receives a packet that will traverse the

MPLS network, and a SWAP occurs in each intermediary hop to accommodate

downstream router label, how does a LSR know when to POP them?

 

To ensure this takes place in the correct moment, there is a mechanism called Penultimate Hop

Popping, and its implemented to pop/remove the label one hop before its destination. It works in a clever way: the LSR having the destination network directly connected or summarized, advertises

a specific label binding for that prefix using the reserved label range. Let’s take a closer look.

 

Among the numbers used for labels, the range from 0 to 15 is reserved, and some of

those numbers are used by the protocol itself to perform operations. Although there are

several label numbers in the reserved range, we will take a look to the most used ones:

 

Label Number 3 or Implicit NULL: This label number is advertised by the ultimate router (the one just

next to the destination) so that the upstream neighbor POPs the label from the packet before sending it.

The purpose is to prevent double lookups in the ultimate LSR. If a labeled packet arrived, the LSR would

have to perform a lookup in the LFIB to realize the label must be removed, and then another one, but this

time in the FIB (regular IP lookup) to find the next hop information and outgoing interface. If the label is

removed by the penultimate hop LSR, the first (and unnecessary) lookup is prevented from happening.

 

![img](mpls.assets/rtaImage.jpeg)

 

Label numbers 0 and 2 (IPv4 and IPv6) or Explicit NULL: Although removing the label one hop before

helps to prevent a second lookup, it also has a downside. QoS information can be poured in the MPLS

header making use of the TC (Traffic Class) bits, but, if the label is removed one hop before, the QoS

information is also lost. This label is used to prevent PHP (Penultimate Hop Popping) behavior from happening.

The explicit NULL label will be advertised by the ultimate LSR (depending on IP version - 0 for IPv4 and

2 for IPv6) and the upstream neighbor will send the packet using that number. Once it is received, the

ultimate LSR will remove the implicit NULL label and check the QoS information to forward it accordingly.

![img](mpls.assets/rtaImage.jpeg)

Label number 1 or Router Alert: This label is used to troubleshoot MPLS as it assures packets are

sent in “safe” mode to guarantee their arrival to their destination. When a LSR receives a packet with

label 1, it will bypass hardware forwarding and will be punted to the CPU (process switched). The label 1 is not shown in the LFIB as it is forwarded by software. The forwarding is slightly different

from the rest of the labels, because label 1 is not removed in each hop it goes through. The LSRs

will swap the labels as commonly done (using contents of LFIB) and then label 1 will be placed on

top of the existing label before forwarding, to guarantee it will be process switched by the next LSR.

 

![img](mpls.assets/rtaImage.jpeg)

 

So far, we spoke about labeled packets but we did not look in detail how exactly an

MPLS label looks like, and where exactly it is placed. Let's have a closer look now:

 

![img](mpls.assets/rtaImage.jpeg)

As depicted above, the MPLS header is 32 bits (4 bytes) long and it is just in the middle between the layer

2 and layer 3 headers when forwarding happens. Taking a closer look we can identify the following fields:

 

Label (20 bits): Identifies the label value used by LSRs to forward the packet through

a MPLS enabled network. The value range for this field is <0 - 1,048,575> (220-1).

 

Traffic Class (3 bits): The traffic class field, formerly known as EXP field, is used to carry traffic class

information so QoS policies can be implemented in the MPLS network by checking the value in the header.

 

Bottom Of Stack (1 bit): MPLS allows multiple labels to be placed onto a packet. They are

then treated as a stack; the bottom label is the one closest to the Layer 3 header, the top label is the one closest to the Layer 2 header, and LSRs always operate on the top label

only (with the exception of Router Alert label). To be able to tell which label is the last one -

the bottom one - the BoS bit will be set to 1 on the bottom label, and to 0 on all other labels.

 

Time to Live (TTL) (8 bits): Analogous to IP forwarding, it is used to keep track of the number of

hops that a labeled packet can take (or the number of routers it can traverse in its journey to its

destination) before being dropped. Used as loop prevention mechanism. Range of values is <0 - 255>

(28-1). Packets are forwarded and one unit it subtracted from the current value at each hop/router,

this operation is repeated until it reaches its destination or the value reaches 0 (and it is dropped).

 

Up to this point, we have discussed about many topics regarding MPLS, a bit of history and several

components that work together to provide a transport method whose applications are a common

and attractive trait nowadays. This blog has been intended to be an introductory lesson in plain

MPLS to understand its inner moving parts. Future blogs will dwell deep into other more complex

scenarios and applications of this protocol to build an infrastructure able to provide a service.

 

Any feedback, comments, questions and corrections are welcome!!

