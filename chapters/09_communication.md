# Communication

This chapter explains how computers exchange data, from a single wire between two machines to the Internet, and how they keep those exchanges private. The same principles apply at every scale.

## A Link Between Two Machines

The simplest network is two computers joined by a serial cable, as described in [Talking to the World](#talking-to-the-world). Each byte sent by one arrives at the other. Even this requires some agreement between the two: the same speed, the same way of marking where one message ends and the next begins, and some way to detect a byte that arrives damaged.

The first computer terminals were teleprinters, typewriters that sent each key press over a wire and printed whatever came back. Their screen-based successors added **escape sequences**: runs of characters, starting with the escape code, that move the cursor, clear the screen or change colours instead of printing. The sequences used by the DEC VT100 terminal of 1978 became a standard that nearly every terminal program still understands. A terminal program on a modern computer is in effect a simulated VT100.

For decades, people connected computers over the telephone network with **modems**, which convert bits into sounds and back. A common use was the **bulletin board system** (BBS): a computer that others could dial into, one or a few callers at a time, to read and post messages, exchange files and play games. Many BBSes now run on the Internet and are reached with telnet or SSH, programs that open a terminal on another computer across a network. They remain a text-based way for a community to meet.

## Packets

A dedicated wire works for two machines, but connecting many machines this way is impractical, so they share connections instead. The idea that made modern networks possible is to divide every message into **packets**: short blocks of data, each preceded by a **header** that gives its source, its destination, its length and a checksum to detect damage. Packets from many conversations can then share the same wires, taking turns, and each finds its own way to its destination.

## Layers

Network software is organized in **layers**. Each layer uses the one below it and offers a simpler service to the one above, in the same way that a program uses the operating system without knowing how the disk works.

| Layer             | Function                      | Examples               |
|-------------------|-------------------------------|------------------------|
| physical and link | move frames to neighbours     | Ethernet, Wi-Fi, radio |
| network           | carry packets across networks | IP                     |
| transport         | deliver data to programs      | TCP, UDP               |
| application       | provide a service to the user | SSH, HTTP, IRC, DNS    |

A message from an application passes down through the layers, each adding its own header. It travels across the network as a **frame** (the link layer's name for a packet), and passes back up through the layers at the other end, each removing its header. As a result, each layer can change independently of the others. The same web page can travel over a cable, over Wi-Fi or over a radio link without any change to the application.

## The Link Layer

**Ethernet** connects machines on a local network by cable. Each network interface has a unique 48-bit **MAC address**, set at the factory. Data travels in frames that carry the sender's and receiver's MAC addresses and a CRC. A **switch** joins several cables and forwards each frame only to the port where its destination is.

Wireless networks such as **Wi-Fi** perform the same function by radio. Low-power radios such as **LoRa** send small messages over many kilometres at low speed. A **mesh** of such radios, in which each one passes on messages for its neighbours, can connect a whole area with no other infrastructure.

## IP: Addresses and Routing

The **Internet Protocol** (IP) gives every machine on a network an **IP address**. The older and still most common form, IPv4, uses 32 bits, written as four bytes in decimal, such as `192.168.1.20`. The newer IPv6 uses 128 bits, enough for every device that will ever exist.

Addresses are organized in networks. Machines on the same local network can reach each other directly. To reach anything else, a machine sends the packet to a **router**, its **gateway**, which forwards it to another router closer to the destination, and so on, hop by hop, until it arrives. No single router knows the whole route. Each knows only which way to send packets for each part of the address space. For this reason the Internet can grow without any one party managing all of it.

Two services make IP easier to use:

- **DHCP** assigns addresses automatically. A new machine asks the local network for an address, and a DHCP server assigns one and tells it which gateway to use.
- **DNS**, the domain name system, translates names such as `machdyne.com` into IP addresses by querying a hierarchy of servers.

## Transport: TCP and UDP

IP delivers packets on a best-effort basis. They may arrive out of order, twice, or not at all. The transport layer determines how this is handled.

**UDP** sends individual messages, called **datagrams**, with no guarantees. It is simple and quick, and it suits uses where a lost message does not matter or will be requested again, such as DNS lookups, time synchronization or live audio.

**TCP** builds a reliable, ordered stream of bytes on top of unreliable packets. It numbers every byte it sends. The receiver acknowledges what it has received, and the sender resends anything not acknowledged in time. The receiver puts everything back in order before passing it to the program. To the program, a TCP connection behaves like a pipe: bytes go in at one end and come out at the other, all of them and in order.

Both TCP and UDP use **port numbers** to distinguish programs on the same machine. A web server listens on port 80 or 443, and an SSH server on port 22. A connection is identified by four numbers: the two IP addresses and the two ports.

## Applications

The application layer provides the services that users and programs need. Many of the oldest application protocols are plain text, which makes them easy to understand and to debug by hand. A web browser requesting a page sends lines such as these:

```text
GET /index.html HTTP/1.1
Host: example.com
```

The request ends with a blank line. The server replies with a status line, some headers, a blank line, and the page itself.

Some common protocols:

- **Telnet** and **SSH** provide a remote terminal. Telnet sends everything, including passwords, as plain text. SSH encrypts it.
- **HTTP** and **HTTPS** carry the web. Modern web pages are often too large for a small computer, but simple pages work well.
- **Gopher** and **Gemini** are much simpler alternatives to the web, built around text documents and menus, and suited to small machines.
- **IRC** is a long-established protocol for text chat in shared channels.
- **Email** is delivered by SMTP and collected by POP or IMAP.

## Keeping Secrets

Packets pass through many machines on their way, and any of them could read or alter the data. **Cryptography** protects against this. It provides three properties:

- **Confidentiality**: only the intended receiver can read the message.
- **Integrity**: any change to the message is detected.
- **Authentication**: the receiver can be certain who sent it.

**Symmetric** encryption uses one secret key both to encrypt and to decrypt. It is fast, but both ends must already share the key, and delivering it to them securely is difficult.

**Public-key** cryptography solves that problem with a pair of keys. The **public key** can be given to anyone, and the matching **private key** is kept secret. The pair makes two things possible. Two machines that have not communicated before can agree on a shared secret over an open network, even while others are listening. In addition, a message can carry a **digital signature**, made with the private key, which anyone with the public key can check and no one without the private key can forge.

Secure protocols combine these methods. When a browser connects to an HTTPS site, or a terminal to an SSH server, the two ends use public-key cryptography to authenticate and to agree on a symmetric key. They then use that key and fast symmetric encryption for the rest of the session. The protocols are called **TLS** and **SSH**.

Authentication raises a question of trust: how to know that a public key belongs to the intended site. The web relies on **certificates**, which are public keys signed by organizations that browsers are configured to trust. SSH usually asks the user to confirm a server's key the first time and remembers it afterwards.

Cryptography also needs good **random numbers**, so that keys cannot be guessed. Computers are deterministic, so they gather randomness from physical noise. Some chips, including the FPGA designs in this book, contain a **true random number generator** that measures the jitter of free-running oscillators.

All of this requires computation. On a small processor, the arithmetic of public-key cryptography can take seconds per connection. FPGA computers have an advantage here: the slow parts can be given their own circuits in the FPGA, which makes them many times faster.

## Networks Without the Internet

The Internet is convenient, but it is not the only means of communication, and it may not always be available.

- A **local network** of a switch and a few cables, or a single serial link, needs nothing from outside.
- **Radio meshes** can carry short messages across a town or a valley without any infrastructure.
- **Store and forward** systems pass messages on whenever a link is available. Bulletin boards once exchanged mail this way, calling each other at night when telephone rates were lower.
- Data can be carried by hand on storage devices, a method known as **sneakernet**. It can still move large amounts of data faster than most networks.

A timeless computer should be useful with no network at all, and able to use whatever network is available when there is one. Plain text, simple protocols and open standards make both possible.

This completes the description of the machine: a processor, memory, devices, an operating system and a network. The next part of the book is about programs.
